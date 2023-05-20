# FastAPI Application

This is a FastAPI application that interacts with the OpenAI API and performs similarity search on a vectorstore. It
provides an endpoint for sending a message and receiving a response.

## Prerequisites

- Python 3.9 or higher
- OpenAI API key

## Getting Started

1. Clone this repository:

   ```shell
   git clone git@github.com:AlexTyutyunnykUA/NiftyBridge-AI-assistant.git

2. Change to the project directory:
   
   ```shell
   cd NiftyBridge-AI-assistant

3. Install the dependencies:

   ```shell
   pip install -r requirements.txt

4. Set the OpenAI API key as an environment variable:

   ```shell
   export OPENAI_API_KEY=<your_openai_api_key>

## Running the Application

### Using Docker

1. Build the Docker image:

   ```shell
   docker build -t my-fastapi-app .

2. Run a Docker container based on the image:

   ```shell
   docker run -p 3000:3000 --env OPENAI_API_KEY=$OPENAI_API_KEY my-fastapi-app

The application will be accessible at http://localhost:3000/api/send.

### Without Docker

1. Start the application using uvicorn:

   ```shell
   uvicorn main:app --host 0.0.0.0 --port 3000

The application will be accessible at http://localhost:3000/api/send.

## API Documentation

Once the application is running, you can access the Swagger UI documentation at http://localhost:3000/docs to explore
the available endpoints and interact with the API.




   