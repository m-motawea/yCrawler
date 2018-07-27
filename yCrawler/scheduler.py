#!/usr/bin/python2.7
import sys, os
from spiders.comms import read_message
import time
from threading import Thread
import daemon



def runSpider(spider, **kwargs):
    """starts a spider from the command line using scrapy crawl <spider> <args> to avoid twisted reactor problems"""
    args = ''
    for key in kwargs.keys():
        args += ' -a {}="{}"'.format(key, kwargs[key])
    os.system('scrapy crawl {} {}'.format(spider, args))


def recieve():
    #create communication fifo
    if not os.path.exists('/tmp/url_pipe'):
        os.mkfifo('/tmp/url_pipe')
    while True:
        #reading url from fifo
        rcv = read_message('/tmp/url_pipe')
        if rcv:
            #calling video spider with the recieved url
            runSpider('videoscraper', start_url=rcv)



def main():
    downloadFlag = False
    example = '''./scheduler.py -p /home/user/Downloads/yImages -u "https://www.youtube.com/watch?v=qPvPiMbPSTE&list=PLZyvi_9gamL-EE3zQJbU5N3nzJcfNeFHU" -t 300 -D "/home/user/Downloads"'''
    usage = 'Usage: ./scheduler.py -p <download path> -u <start url> -t <time in seconds> (Optional: -D <video download path>) (Optional start as deamon: -d) \nExample:\n{}'.format(example)
    #parsing command line options
    if len(sys.argv) == 1:
        print(usage)
        exit()
    if '-p' in sys.argv:
        download_path = sys.argv[sys.argv.index('-p') + 1]
    else:
        print('Missing -p option.\n{}'.format(usage))
        exit()
    if '-u' in sys.argv:
        start_url = sys.argv[sys.argv.index('-u') + 1]
    else:
        print('Missing -u option.\n{}'.format(usage))
        exit()
    if '-t' in sys.argv:
        wait_time = float(sys.argv[sys.argv.index('-t') + 1])
    else:
        print('Missing -t option.\n{}'.format(usage))
        exit()
    if '-D' in sys.argv:
        downloadFlag = True
        try:
            vPath = sys.argv[sys.argv.index('-D') + 1]
            if not os.path.exists(vPath):
                print('Given Path "{}" does not exist'.format(vPath))
                exit()
        except:
            print('Missing download path.\n{}'.format(usage))
            exit()
    
    #checking the given url for a playlist or channel
    if '/videos' in start_url:
        spider = 'channelscraper'
    else:
        spider = 'playlistscraper'
        #starting another thread to continue crawling individual video urls
        t1 = Thread(target=recieve)
        t1.daemon = True
        t1.start()
        
    while True:
        if downloadFlag:
            runSpider(spider, start_url=start_url, download_path=download_path, vPath=vPath)
        else:
            runSpider(spider, start_url=start_url, download_path=download_path)
        for i in range(0, int(wait_time)):
            #to recieve keyboard interrupts
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit()

                
if __name__ == '__main__':
    if '-d' in sys.argv:
        print('starting in background with pid: {}'.format(os.getpid()))
        with daemon.DaemonContext():
            main()
    else:
        main()