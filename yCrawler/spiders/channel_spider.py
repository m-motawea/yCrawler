from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy_splash import SplashRequest
from video import Video

class ChannelSpider(Spider):
    name = "channelscraper"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ChannelSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs['start_url']]
        self.download_path = kwargs['download_path']
        if 'vPath' in kwargs.keys():
            self.vPath = kwargs['vPath']
            self.vDownload = True

    def start_requests(self):
        for url in self.start_urls:
            script = '''
function main(splash)
    local num_scrolls = 20
    local scroll_delay = 1.0

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end'''
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': script, 'wait': 0.5})

    def parse(self, response):
        for vid in Selector(text=response.body).xpath('//ytd-grid-video-renderer[@class="style-scope ytd-grid-renderer use-ellipsis"]').extract():
            duration = Selector(text=vid).xpath('//span[@class="style-scope ytd-thumbnail-overlay-time-status-renderer"]/text()').extract_first().strip()
            href = 'https://youtube.com' + Selector(text=vid).xpath('//a[@id="thumbnail"]/@href').extract_first()
            title = Selector(text=vid).xpath('//a[@id="video-title"]/text()').extract_first()
            views = int(Selector(text=vid).xpath('//a[@id="video-title"]/@aria-label').extract_first().split()[-2].replace(',', ''))
            img_thumb = Selector(text=vid).xpath('//img/@src').extract_first()
            img_src = None
            if img_thumb:
                img_src = img_thumb.split('?sqp')[0] + '?amp;sqp' + img_thumb.split('?sqp')[1]
            v = Video.get(title=title)
            if v:
                v.update(views=views, duration=duration)
            else:
                v = Video(title, href, img_src, img_thumb, views, duration)
                v.save(self.download_path)
                if self.vDownload:
                        v.download(self.vPath)