# yCrawler
simple youtube crawler (Challenge for an Interview)

## Intsallation:
1- Install docker, wget, python-pip

2- Run scrapinghub/splash container

$ sudo docker run -d -p 5023:5023 -p 8050:8050 -p 8051:8051 --name splash scrapinghub/splash --disable-private-mode

3- Install python requirements

$ sudo pip install -r yCrawler/requirements.txt

4- Run scheduler.py

$ ./scheduler.py -p /home/user/Downloads/yImages -u "https://www.youtube.com/watch?v=qPvPiMbPSTE&list=PLZyvi_9gamL-EE3zQJbU5N3nzJcfNeFHU" -t 300 -D "/home/user/Downloads

(for Ubuntu)

1- Run install.sh

$ ./install.sh



## Usage:
Crawl a YouTube channel or playlist periodically, save video information, save video thumbs and download videos(optional).

Options: "./scheduler.py -p <download path> -u <start url> -t <time in seconds> (Optional: -D <video download path>) (Optional start as deamon: -d)"
