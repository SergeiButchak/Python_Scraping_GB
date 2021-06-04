import scrapy
from scrapy.http import HtmlResponse
from Python_Scraping_GB.Lesson_7.leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class LeroyruSpider(scrapy.Spider):
    name = "leroyru"
    allowed_domains = ["samara.leroymerlin.ru"]
    start_urls = ["https://samara.leroymerlin.ru/"]

    custom_settings = {
        "ITEM_PIPELINES": {"Python_Scraping_GB.Lesson_7.leroy.pipelines.LeroyPhotosLoader": 200},
        "IMAGES_STORE": "images"
    }

    def __init__(self, search):
        super(LeroyruSpider, self).__init__()
        self.start_urls = [f"https://samara.leroymerlin.ru/search/?q={search}&suggest=true"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница: ')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//a[@data-qa='product-name']")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[contains(@slot,'thumbs')]/@src")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('specifications', response.xpath('//dl[@class="def-list"]'))

        yield loader.load_item()



        # name = response.xpath("//h1/text()").extract_first()
        # photos = response.xpath("//img[contains(@class,'PreviewListSmall__image')]/@src").extract()
        # item = CitilinkItem(name=name, photos=photos)
        # yield item
