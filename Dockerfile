FROM python:3.12-slim

#set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
	apt-get install -y build-essential libpq-dev && \
	rm -rf /var/lib/apt/lists/*

#copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy project files
COPY . .

#expose port for Fastapi
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start FastAPI app with Uvicorn since we Fastapi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


