# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Add /app to the Python path
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install openai PyPDF2 fpdf2
RUN pip install -q langchain==0.0.150 pypdf pandas matplotlib tiktoken textract transformers openai faiss-cpu