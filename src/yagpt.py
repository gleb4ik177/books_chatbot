import requests
import sys
import re
sys.path.append("../")
from config import catalog_id, apikey
from src.postgres import value_of_attribute,authors_by_book_id
def response(query):
    prompt = {
        "modelUri": f"gpt://{catalog_id}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Представь, что ты работаешь в службе поддержки книжного магазина. Тебе нужно определить тип запроса клиента, в зависимости от того, что спрашивает клиент. Всего вариантов 8:\
                  1. Автор книги.\
                  2. Дата выпуска/выхода книги.\
                  3. Количество страниц в книге.\
                  4. Возрастное ограничение.\
                  5. Размер книги.\
                  6. Тип обложки книги.\
                  7. Тип бумаги.\
                  8. Вес книги.\
                  Выведи одно из вышеупомянутых чисел, в зависимости от запроса клиента."
            },
            {
                "role": "user",
                "text": query
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {apikey}"
    }
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()['result']['alternatives'][0]['message']['text']
    return re.search('\d+', result)[0]

def answer_by_type(question_type:str, book_id):
    type_attribute = {'1':'authors', '2':'release', '3':'pages', '4':'age', '5':'size', '6':'type_cover', '7':'type_paper', '8':'weight'}
    attribute = type_attribute[question_type]
    if attribute != 'authors':
        value = value_of_attribute(attribute, book_id)
        if attribute == 'release':
            print(f"Здравствуйте! Книга была выпущена в {value} году")
        if attribute == 'pages':
            print(f"Здравствуйте! В книге содержится {value} страниц")
        if attribute == 'age':
            print(f"Здравствуйте! Книга рекомендована лицам старше {value[:-1]} лет")
        if attribute == 'size':
            print(f"Здравствуйте! Размер книги: {value} (мм)")
        if attribute == 'type_cover':
            print(f"Здравствуйте! Тип обложки, используемый в книге: {value}")
        if attribute == 'type_paper':
            print(f"Здравствуйте! Тип бумаги, используемый в книге: {value}")
        if attribute == 'weight':
            print(f"Здравствуйте! Вес книги составляет {value} грамм")
    elif attribute == 'authors':
        authors = authors_by_book_id(book_id)
        n = len(authors)
        if n > 1:
            print("Здравствуйте! Книгу написали ", end='')
            for i in range(n-2):
                print(authors[i][0], end=', ')
            print(f"{authors[n-2][0]} и {authors[n-1][0]}")
        elif n == 1:
            print(f"Здравствуйте! Автором книги является {authors[0][0]}")

