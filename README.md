# ada-chatbot-builder-backend
Create the .env based on the .example
For the secret_key run command on bash and copy
"openssl rand -hex 32"

Initialize python virtual enviornment
"python -m venv .venv"

In the virtual env install all requirements
"pip install -r requirements.txt"

Run the app localy
"uvicorn api.main:app --reload"

To use docker write in terminal
"docker compose up --build"

When running the app, to see it on the browser type http://<host_machine_ip>:8000
