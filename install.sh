#!/bin/bash
#installing docker
echo "Installing Docker..."
sudo apt-get update -y
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install docker-ce -y
sudo usermod -aG docker $USER
sudo systemctl restart docker
sudo systemctl enable docker

#pulling & running splash image
echo "Pulling & running Splash"
sudo docker pull scrapinghub/splash
sudo docker run -d -p 5023:5023 -p 8050:8050 -p 8051:8051 --name splash scrapinghub/splash --disable-private-mode
sudo apt-get install wget -y
sudo apt-get install python-pip -y

#installing Python modules
echo "Installing Python modules"
sudo pip install -r yCrawler/requirements.txt