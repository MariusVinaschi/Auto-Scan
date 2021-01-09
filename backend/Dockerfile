FROM python:3.8-alpine 

# Create Direcory 
WORKDIR /api 

# Copy requirements and install 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Nmap 
RUN apk add nmap 
RUN apk add nmap-scripts

# Start the Application  
EXPOSE 5000
COPY . .
CMD ["python", "app.py"]
