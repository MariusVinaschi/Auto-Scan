FROM kalilinux/kali-rolling:latest 

RUN apt -y update && apt -y dist-upgrade && apt clean
RUN apt install -y curl apt-utils nmap python ruby ruby-dev postgresql 
RUN apt install -y metasploit-framework

EXPOSE 55552
EXPOSE 55553

CMD msfrpcd -P 123456 -n -f -a 0.0.0.0  