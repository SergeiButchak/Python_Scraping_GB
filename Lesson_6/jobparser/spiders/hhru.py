import re
import scrapy
from scrapy.http import HtmlResponse
from Python_Scraping_GB.Lesson_6.jobparser.items import HhruItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item_link = response.url
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//p/span[@data-qa='bloko-header-2']/text()").extract()
        if len(item_salary) == 1:
            item_min_salary = ""
            item_max_salary = ""
            item_currency = ""
        else:
            if "от " in item_salary:
                item_min_salary = item_salary[item_salary.index("от ") + 1]
            else:
                item_min_salary = ""
            if " до " in item_salary:
                item_max_salary = item_salary[item_salary.index(" до ") + 1]
            else:
                item_max_salary = ""
            item_currency = item_salary[len(item_salary) - 2]

        item = HhruItem(name=item_name, link=item_link, min_salary=item_min_salary,
                        max_salary=item_max_salary, currency=item_currency)
        yield item


class SjruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//div[contains(@class, 'f-test-vacancy-item')]//a[@target='_blank']/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item_link = response.url
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//span/span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        # item = HhruItem(name=item_name, link=item_link, salary=item_salary)
        if len(item_salary) == 1:
            item_min_salary = ""
            item_max_salary = ""
            item_currency = ""
        else:
            if "от" in item_salary:
                match = re.search(r'(\d*)(.*)', item_salary[2].replace(u'\xa0', u''))
                item_min_salary = match.group(1)
                item_max_salary = ""
                item_currency = match.group(2)
            elif "до" in item_salary:
                match = re.search(r'(\d*)(.*)', item_salary[2].replace(u'\xa0', u''))
                item_max_salary = match.group(1)
                item_min_salary = ""
                item_currency = match.group(2)
            elif len(item_salary) == 4:
                item_min_salary = item_salary[0].replace(u'\xa0', u'')
                item_max_salary = item_salary[1].replace(u'\xa0', u'')
                item_currency = item_salary[3]
            else:
                item_min_salary = item_salary[0].replace(u'\xa0', u'')
                item_max_salary = item_salary[0].replace(u'\xa0', u'')
                item_currency = item_salary[2]

        item = HhruItem(name=item_name, link=item_link, min_salary=item_min_salary,
                        max_salary=item_max_salary, currency=item_currency)
        yield item
