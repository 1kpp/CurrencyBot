import json
from data.request_body import return_body
import requests

url = 'https://api.tinkoff.ru/geo/withdraw/clusters'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


def get_currency_places():
    response = requests.post(url=url, json=return_body(), headers=headers).json()

    result = []
    list_of_places = [item for item in response['payload']['clusters']]
    for item in list_of_places:
        address = f'{item["points"][0]["address"]}'
        is_work = "Да" if item["points"][0]["atmInfo"]["available"] is True else "Нет"
        latitude = item["points"][0]['location']['lat']
        longitude = item["points"][0]['location']['lng']
        map_link = 'https://yandex.ru/maps/?mode=search&text='
        list_of_currencies = []
        for curr_type in item["points"][0]["limits"]:
            currency = curr_type["currency"]
            currency_sum = curr_type["amount"]
            currency_remains = f'{currency}, осталось: {currency_sum}'
            list_of_currencies.append(currency_remains)
        result.append({
            'address': address,
            'is_work': is_work,
            'currencies_available': list_of_currencies,
            'map_link': f'{map_link}{latitude}%2C+{longitude}'
        })
    if len(list_of_places) == 0:
        return 'Валюты нет в городе, сожалею..'

    with open('data/current_result.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    get_currency_places()


if __name__ == '__main__':
    get_currency_places()
