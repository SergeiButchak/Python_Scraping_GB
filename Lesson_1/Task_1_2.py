"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
пройдя авторизацию. Ответ сервера записать в файл.
"""
import requests

with open("secret", "r") as file_out:
    token = file_out.readline()

    end_point = "https://cloud-api.yandex.net"
    query = "/v1/disk/resources"
    headers = {
        'Accept': 'application/json',
        'Authorization': f"OAuth {token}"
    }
    parameters = "path=%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B"
    response = requests.request("GET", end_point + query, headers=headers, params=parameters)
    if response.status_code == 200:
        with open("result_1_2.json", "w") as f_out:
            f_out.write(response.text)
    else:
        print(f"При выполнении запроса произошла ошибка: {response.status_code} {response.text}")
