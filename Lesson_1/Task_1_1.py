"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import requests

name = input("Введите имя пользователя: ")

url = f"https://api.github.com/users/{name}/repos"

headers = {
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    json_resp = response.json()
    print(f"Репозитории пользователя {name}")
    for el in json_resp:
        print(el['name'])
    with open("result_1_1.json", "w") as f_out:
        f_out.write(response.text)
elif response.status_code == 404:
    print(f"Пользоаватель {name} не найден")
else:
    print(f"При выполнении запроса произошла ошибка: {response.status_code} {response.text}")
