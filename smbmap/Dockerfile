FROM python:3.8-slim 

RUN apt-get update && apt-get install -y libffi-dev libxml2-dev libxslt-dev libssl-dev openssl  git 

# Copy requirements and install 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Start the Application  
EXPOSE 80
COPY ./app /app

RUN cd app/depedency && git clone https://github.com/ShawnDEvans/smbmap.git && cd ../

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]