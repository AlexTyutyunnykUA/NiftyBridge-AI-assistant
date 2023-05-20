# Base image
FROM python:3.9

# Set the working directory
WORKDIR /NiftyBridge-AI-assistant

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY main.py .
COPY message.py .
COPY text.pdf .
COPY .env .

# Expose the port
EXPOSE 3000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
