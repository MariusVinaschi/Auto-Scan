FROM python:3.8-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PIP_NO_CACHE_DIR=off

WORKDIR /app 

RUN apt-get update && apt-get install -y libffi-dev libxml2-dev libxslt-dev libssl-dev openssl git bash 
COPY . .
RUN pip install -r requirements.txt

# Start the Application  
EXPOSE 80

RUN cd models/ && git clone https://github.com/byt3bl33d3r/CrackMapExec.git  && ls && pwd
RUN pwd

CMD ["python","app.py"]