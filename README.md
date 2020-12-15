# Auto Scan 

AutoScan is a WebApp that uses Flask API and MongoDB. This app launches a Nmap scan and depending on the open ports, the App will start some Auxiliary Module. The results will be shown on the WebApp.

## Interface :  

Start a new scan

![](Images/StartScan.png)

See all the scans

![](Images/Scans.png)

See the results for one scan

![](Images/Result.png)

## Built With :

#### Frontend : 
We created the interface with React Typescript and Material-UI. 
#### API :
The API was created with Flask : 
* flask-restful to encourage best practices
* pymetasploit3 to use Metasploit
* nmap3 to use Nmap 
* marshmallow to check the Input
* flask-pymongo to store the result 
* flask-jwt-extended to create Token
#### Database :
We use MongoDB to stock the results. 

## Install 

```
git clone --branch Docker https://github.com/MariusVinaschi/Auto-Scan.git
cd Auto-Scan 
COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d                                                                   
```

Open your browser and search : http://localhost:3000
