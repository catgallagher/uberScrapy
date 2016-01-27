import scrapy

from uber.items import UberItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from w3lib.html import replace_escape_chars

def addDomain(l):
    return "http://uber.com%s" %l

class UberSpider(scrapy.Spider):
    name = "uber"
    allowed_domains = ["uber.com"]
    start_urls = [
        "https://www.uber.com/cities/"
    ]

    def parse(self, response):
        for sel in response.xpath('//section[@class="cities-list"]/div[@class="grid-locked"]/article/nav'):
            region = sel.xpath('./p[@class = "title"]/text()')[0].extract() 
            for city in sel.xpath('./ul/li/a'):
                l = UberLoader (item = UberItem(), selector=city)
                l.add_xpath('city', 'text()')
                l.add_xpath('link', '@href')
                l.add_value('region', region)
                yield l.load_item()

class UberLoader (ItemLoader):
    default_input_processor = MapCompose(unicode.strip, replace_escape_chars)

    link_out = MapCompose(addDomain)