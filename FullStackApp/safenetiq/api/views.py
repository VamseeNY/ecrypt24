from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserModel, LogInModel
from .serializers import UserSerializer
import os
from os.path import join, dirname
from dotenv import load_dotenv


from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI

from langchain_community.llms import OpenAI
import pandas as pd
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

i=21
x=0
def add_row_to_csv(file_path, row_data):
    # Open the CSV file in append mode
    with open(file_path, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write the new row to the CSV file
        csv_writer.writerow(row_data)


dotenv_path = join(dirname(__file__), '.env_file')
load_dotenv(dotenv_path)


OPENAI_API_KEY =os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0.8, model ='gpt-4', 
                              openai_api_key=OPENAI_API_KEY)
df = pd.read_csv("iitm2.csv")
df = df.drop("Age", axis=1)
def scan(user_id):
    response_schemas = [
        ResponseSchema(name="latest_login", description="The latest login of the user"),
        ResponseSchema(name="risk factor", description="The risk factor of the latest login of the user based on comparsion with previous logins. This could be low medium or high"),
        ResponseSchema(name="explanation", description="explanation of the risk factor of the latest login of the user"),
        ResponseSchema(name="message-if-high", description="If the risk factor is high, Draft a message to the user explaining what contributed to the risk factor and ask them to verify their account using multi factor authentication. if risk factor is medium or low, this should be Null"),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    response_format = output_parser.get_format_instructions()
    pt = PromptTemplate(
            input_variables=["data"],
            partial_variables= {"response_format": response_format},
            template ="""
            You are a bot which finds anamolous user login activity. You are given user login logs which have 
            user_id,Name,Email,Age,Gender,Nationality,Time_of_Login ,Typing_Speed,Time_to_Complete_Captcha,Device,Local_IP,Global_IP,and OS. Print out the anamolous data points, explain why and display a risk factor for them. The risk factor is higher if the distance between the previous location and current location is high.
            ---
            {dataset}
            ---
            {response_format}
            """
            )
    chain1 = LLMChain(llm = llm, prompt=pt, 
                                    output_key="anamolies"
                                )
    out = chain1.run(dataset=df[df.user_id==user_id].to_string())
    print(output_parser.parse(out))
    out = output_parser.parse(out)

    if out["message-if-high"]!= "None":
        print("yes")
        sender_email = "axisbank.hrteam123@gmail.com"
        sender_password = "ozeesbduqyuvdjck"
        receiver_email = "vamsvaid@gmail.com"
        subject = "Alert!"
        message_content = f'{out["message-if-high"]}\n{out["explanation"]}'

        send_email(sender_email, sender_password, receiver_email, subject, message_content)
    return out


def send_email(sender_email, sender_password, receiver_email, subject, message_content):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the message body
    body = MIMEText(message_content, 'plain')
    message.attach(body)

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Change the server and port accordingly
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", str(e))

    finally:
        # Quit the server
        server.quit()


# Create your views here.
@api_view(['POST'])
def registerView(request):
    ser=UserSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        ''' 
        user=UserModel.objects.get(email=request.data['email'])
        csv_file_path = 'iitm2.csv'
        new_row_data = [user.name, user.email,user.age, user.gender, user.nationality]
        
        add_row_to_csv(csv_file_path, new_row_data)
        '''
        return Response(ser.data, status=201)
    return Response(ser.errors, status=400)
@api_view(['POST'])
def loginView(request):
    global i
    global x
    data=request.data
    print(data)
    user=UserModel.objects.get(email=data['email'])
    if user.password!=data['password']:
        return Response({
            "stat":"failed"
        })
    a=LogInModel(user_id=user.id, user_name=user.name,time=data['time'],typing_speed=data['speed'], captcha_complete=data['captcha_complete'], device=data['device'], OS=data['OS'], lat=data['lat'],long=data['long'])
    a.save()
    user=UserModel.objects.get(email=request.data['email'])
    csv_file_path = 'iitm2.csv'
    new_row_data = [user.id+i+x,user.name, user.email,user.age, user.gender, user.nationality,data['time'],data['speed'],data['captcha_complete'], data['device'],data['lat'],data['long'],data['OS']]
    x+=1
    add_row_to_csv(csv_file_path, new_row_data)
    return Response({
        "stat":"success",
        "message":scan(user.id+i+x-1)
    })


