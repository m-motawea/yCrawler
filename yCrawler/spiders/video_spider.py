from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy_splash import SplashRequest
from video import Video

class VideoSpider(Spider):
    name = "videoscraper"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(VideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs['start_url']]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        player = Selector(text=response.body).xpath('//div[@id="player-api"]').extract_first()
        duration = Selector(text=player).xpath('//div[@class="ytp-bound-time-right"]/text()').extract_first()
        views = int(Selector(text=response.body).xpath('//div[@id="watch7-views-info"]/div[@class="watch-view-count"]/text()').extract_first().split()[0].replace(',', ''))
        title = Selector(text=response.body).xpath('//title/text()').extract_first().split(' -')[0]
        v = Video.get(title=title)
        if v:
            v.update(views=views, duration=duration)
        yield {'title': title, 'views': views, 'duration': duration}