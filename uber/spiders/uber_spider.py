import scrapy

from uber.items import UberItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from w3lib.html import replace_escape_chars

def addDomain(path):
    return "http://uber.com%s" % path

class UberSpider(scrapy.Spider):
    name = "uber"
    allowed_domains = ["uber.com"]
    start_urls = [
        "https://www.uber.com/cities/"
    ]

    def parse(self, response):
        city_list_path = '//section[@class="cities-list"]/div[@class="grid-locked"]/article/nav'
        region_path = './p[@class = "title"]/text()'
        city_path = './ul/li/a'
        
        for continent in response.xpath(city_list_path):
            region = continent.xpath(region_path)[0].extract() 
            for city in continent.xpath(city_path):
                l = UberLoader (item = UberItem(), selector=city)
                l.add_xpath('city', 'text()')
                l.add_xpath('link', '@href')
                l.add_value('region', region)
                yield l.load_item()

class UberLoader (ItemLoader):
    default_input_processor = MapCompose(unicode.strip, replace_escape_chars)

    link_out = MapCompose(addDomain)