FROM python:3.8-alpine 

# Create Directory 
WORKDIR /api

# Copy requirements and install 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Start the Application  
EXPOSE 80
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
