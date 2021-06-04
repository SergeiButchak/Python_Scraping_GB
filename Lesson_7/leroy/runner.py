from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Python_Scraping_GB.Lesson_7.leroy.spiders.leroyru import LeroyruSpider
from Python_Scraping_GB.Lesson_7.leroy import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # query = input('')

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyruSpider, search='шуруповерты')

    process.start()
