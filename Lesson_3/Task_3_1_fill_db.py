from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
import re

client = MongoClient('localhost', 27017)
db = client['hh_ru']
db_vacancies = db.vacancies


def search_job(search_str, limit=10):
    vacancies = []
    page = 0
    end_point = 'https://hh.ru'
    req = '/search/vacancy'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    params = {
        'st': 'searchVacancy',
        'text': search_str,
        'clusters': 'true',
        'enable_snippets': 'true',
        'customDomain': 1,
        'items_on_page': '100',
        'page': page,
    }
    while True:
        response = requests.request("GET", end_point+req, params=params, headers=headers)
        text = response.text.replace(u"\xa0", u" ")
        text = text.replace(u"\u202f", "")
        res = bs(text, "html.parser")
        vacancies.append(res.find_all("div", {"class": "vacancy-serp-item"}))
        page += 1
        if page >= limit:
            break
        try:
            res.find("a", {"data-qa": "pager-next"}).find("span")
        except AttributeError:
            break
    return vacancies


def job_parser(source_list):
    res = []
    job_struct = dict()
    for i in source_list:
        for j in i:
            job_struct["Vacancy_name"] = j.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).getText()
            job_struct["Employer_name"] = j.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).getText()
            job_struct["City"] = j.find("span", {"data-qa": "vacancy-serp__vacancy-address"}).getText().split(", ")[0]
            job_struct["Link"] = j.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).get("href").split("?")[0]
            salary = j.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary:
                salary_text = j.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"}).getText()
                job_struct["Salary"] = salary_text
                if salary_text.find(u"от") >= 0:
                    parse_res = re.search(r"(.*) (.*) (.*)", salary_text)
                    job_struct["Salary_min"] = int(parse_res.group(2))
                    job_struct["Salary_max"] = None
                    job_struct["Salary_Currency"] = parse_res.group(3)
                elif salary_text.find(u"до") >= 0:
                    parse_res = re.search(r"(.*) (.*) (.*)", salary_text)
                    job_struct["Salary_min"] = None
                    job_struct["Salary_max"] = int(parse_res.group(2))
                    job_struct["Salary_Currency"] = parse_res.group(3)
                elif salary_text.find(u"–") >= 0:
                    parse_res = re.search(r"(.*) – (.*) (.*)", salary_text)
                    job_struct["Salary_min"] = int(parse_res.group(1))
                    job_struct["Salary_max"] = int(parse_res.group(2))
                    job_struct["Salary_Currency"] = parse_res.group(3)
                else:
                    parse_res = re.search(r"(.*) (.*)", salary_text)
                    job_struct["Salary_min"] = parse_res.group(1)
                    job_struct["Salary_max"] = parse_res.group(1)
                    job_struct["Salary_Currency"] = parse_res.group(2)
            res.append(job_struct.copy())
            job_struct.clear()

    return res


vac = search_job("python", 15)
vac_list = job_parser(vac)
for el in vac_list:
    if db_vacancies.count_documents({"Link": {"$eq": el["Link"]}}) == 0:
        db_vacancies.insert_one(el)
