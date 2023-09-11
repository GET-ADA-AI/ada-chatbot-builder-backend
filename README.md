# ada-chatbot-builder-backend
Create the .env based on the .example
For the secret_key run command on bash and copy
"openssl rand -hex 32"

Initialize python virtual enviornment
"python -m venv .venv"

In the virtual env install all requirements
"pip install -r requirements.txt"

Run the app localy
"uvicorn main:app --reload"
