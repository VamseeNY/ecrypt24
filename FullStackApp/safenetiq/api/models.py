from django.db import models

# Create your models here.
class UserModel(models.Model):
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=100, default='')
    email=models.EmailField()
    age=models.IntegerField()
    gender=models.CharField(max_length=20)
    nationality=models.CharField(max_length=50)
class LogInModel(models.Model):
    user_id=models.IntegerField(default=0)
    user_name=models.CharField(max_length=50, default='')
    time=models.CharField(max_length=20, default='')
    typing_speed=models.IntegerField()
    captcha_complete=models.FloatField(default=0.00)
    device=models.CharField(max_length=25)
    OS=models.CharField(max_length=25)
    risk_factor=models.FloatField(default=0)
    lat=models.FloatField(default=0)
    long=models.FloatField(default=0)

