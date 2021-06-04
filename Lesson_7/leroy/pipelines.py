# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class LeroyPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.db = client["leroy"]
        self.collect = self.db["leroy"]

    def process_item(self, item, spider):
        self.collect.insert_one(item.copy())
        return item


class LeroyPhotosLoader(ImagesPipeline):

    def get_media_requests(self, item, info):
        photo = item['photos']
        if photo:
            for img in photo:
                try:
                    yield scrapy.Request(img)

                except TypeError as e:
                    print(e)

    # def file_path(self, request, response=None, info=None, *, item=None):

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
