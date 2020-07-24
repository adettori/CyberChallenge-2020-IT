FROM ubuntu:18.04


# lib32z1
RUN apt update 
RUN apt install -y apt-utils xinetd
RUN apt upgrade -y
#RUN apt install -y python3 gcc
RUN apt install -y gcc-multilib

RUN useradd -m ctf
WORKDIR /home/ctf

RUN cp -R /lib* /home/ctf 
RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev 
RUN mknod /home/ctf/dev/null c 1 3 
RUN mknod /home/ctf/dev/zero c 1 5 
#RUN mknod /home/ctf/dev/random c 1 8 
#RUN mknod /home/ctf/dev/urandom c 1 9 
RUN chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin 
RUN cp /bin/sh /home/ctf/bin 
RUN cp /bin/ls /home/ctf/bin 
RUN cp /bin/cat /home/ctf/bin 

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./feedme /home/ctf
COPY ./flag.txt /home/ctf

RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf 
RUN chmod 740 /home/ctf/flag.txt

CMD ["/start.sh"]


