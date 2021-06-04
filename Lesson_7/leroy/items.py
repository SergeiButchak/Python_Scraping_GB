# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose


def get_price(value):
    price = int(value.replace(' ', ''))
    return price


def get_photo(value):
    try:
        photo = value.replace('w_82,h_82', 'w_1200,h_1200')
        print(photo)
        return photo
    except Exception:
        return value


def get_specifications_list(value):
    specifications_list = value.xpath('.//div')

    result = {}

    for item in specifications_list:
        name = item.xpath('.//dt/text()').extract()[0]
        value = item.xpath('.//dd/text()').extract()[0].replace('\n', '').strip()

        result[name] = value

    return result


class LeroyItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(get_price))
    text = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(get_photo))
    specifications = scrapy.Field(input_processor=MapCompose(get_specifications_list))
    _id = scrapy.Field()
