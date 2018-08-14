# grade-alert


sudo groupadd docker
sudo systemctl start docker

systemctl start docker.service 
systemctl enable docker.service

$ docker build -t grade_alert_image .
$ docker run -v "$(pwd)":/deploy/ grade_alert_image

$ docker run -it <image> /bin/bash
