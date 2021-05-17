from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['hh_ru']
db_vacancies = db.vacancies


def salary_greater(min_salary):
    return db_vacancies.find({"$or": [{'Salary_min': {'$gt': min_salary}}, {'Salary_max': {'$gt': min_salary}}]})


salary = int(input("Введите желаемую зарплату: "))
for i in salary_greater(salary):
    print(i)
