from scrapy import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from scrapy import Request
from video import Video
from comms import send_message


class PlaylistSpider(Spider):
    name = "playlistscraper"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(PlaylistSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.download_path = kwargs['download_path']
        self.vDownload = False
        if 'vPath' in kwargs.keys():
            self.vPath = kwargs['vPath']
            self.vDownload = True
 
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_splash, endpoint='render.html')


    def parse_splash(self, response):
        for li in Selector(text=response.body).xpath('//ol[@class = "playlist-videos-list yt-uix-scroller yt-viewport"]/li').extract():
            img_url = Selector(text=li).xpath('//img/@data-thumb').extract_first()
            if img_url:
                img_src = img_url.split('&rs')[0] + '&amp;rs' + img_url.split('&rs')[1]
            else:
                img_url = Selector(text=li).xpath('//img/@src').extract_first()
                img_src = img_url.split('&rs')[0] + '&amp;rs' + img_url.split('&rs')[1]
            href = 'https://youtube.com' + Selector(text=li).xpath('//a/@href').extract_first()
            title = Selector(text=li).xpath('//h4 [@class = "yt-ui-ellipsis yt-ui-ellipsis-2"]/text()').extract_first().strip()
            try:
                v = Video.get(title=title)
            except Exception as e:
                print(e)
                exit(1)
            if not v:
                try:
                    v = Video(title=title, url=href, img_src=img_src, img_thumb=img_url)
                    v.save(self.download_path)
                    if self.vDownload:
                        v.download(self.vPath)
                except Exception as e:
                    print(e)
                    exit(1)
            send_message('/tmp/url_pipe', href)
            yield {
                    'title': title,
                    'url': href,
                    'img_src': img_src,
                    'img_thumb': img_url
                }