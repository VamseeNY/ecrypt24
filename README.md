<h1> SafeNetIQ - Encrypton 2024 </h1>
Leveraging powerful GenAI LLM technology for Banking log in security 🔐 


<h2>Installation</h2>

<h3> LLM setup </h3>
- pip install -r requirements.txt
- create .env_file
- set OPENAI_API_KEY = <your key here>
<h3>WebApp Setup</h3>
<h2>Django Setup</h2>
Clone the repository:

    ```bash
    git clone https://github.com/your-username/your_project_name.git
    cd your_project_name
    ```

2. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install Django and DRF:

    ```bash
    pip install -r requirements.txt
    ```

6. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

### Frontend (ReactJS)

1. Navigate back to the root directory:

    ```bash
    cd ..
    ```

2. Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

3. Install dependencies:

    ```bash
    npm install
    ```

## Running the Project

1. Start the Django development server:

    ```bash
    cd backend
    python manage.py runserver
    ```

    The backend server will run on `http://127.0.0.1:8000/`.

2. In a new terminal, navigate to the `frontend` directory and start the React development server:

    ```bash
    cd frontend
    npm start
    ```

    The frontend server will run on `http://localhost:3000/`.

3. Open your web browser and go to `http://localhost:3000/` to view the application.
  

