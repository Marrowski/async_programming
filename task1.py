from gettext import textdomain
from os import write

import requests
import sqlite3
import asyncio
import logging
import aiohttp


logger = logging.getLogger('logs')
logging.basicConfig(filename='log_a.txt', level=logging.INFO, filemode='w', format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8')

connection = sqlite3.connect('content.db')
cursor = connection.cursor()


def create_table_api():
    query = '''
    CREATE TABLE IF NOT EXISTS Content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    body VARCHAR(255) NOT NULL
    );
    '''
    cursor.execute(query)

#1. За допомогою response

def get_data():
    global response
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    print(f'Status code: {response.status_code}')
    logging.info(f'Початок запиту до ресурсу {response}')
    if response.status_code == 200:
        logging.info(f'Отримання статус коду 200:{response.status_code}')
    else:
        print('З`єднання не встановлене. Спробуйте ще раз')
    items = response.json()

    for info in items:
        if info['id'] <= 7:
            print(info)
            write_to_db(info['title'], info['body'])


def write_to_db(title: str, body: str):
    global info
    query = '''
    INSERT INTO Content(title, body) VALUES (?,?)
    '''
    cursor.execute(query, [title, body])
    connection.commit()


#За допомогою aiohttp

file_handler2 = logging.FileHandler('log_b.txt', encoding='utf-8')
file_handler2.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.addHandler(file_handler2)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/posts') as resp:
            print(f'Status code: {resp.status}')

            html_text = await resp.text()
            logging.info(f'Отримання доступу до ресурсу: {html_text}')
asyncio.run(main())