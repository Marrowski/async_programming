import requests
import sqlite3
import asyncio
import logging
import aiohttp


logger_a = logging.getLogger('log_a')
logger_a.setLevel(logging.INFO)

file_handler = logging.FileHandler('log_a.txt', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

file_handler_b = logging.FileHandler('log_b.txt', encoding='utf-8')
file_handler_b.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

logger_a.addHandler(file_handler)

logger_b = logging.getLogger('log_b')
logger_b.setLevel(logging.INFO)

logger_b.addHandler(file_handler_b)

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
    logger_a.info(f'Початок запиту до ресурсу {response}')
    if response.status_code == 200:
        logger_a.info(f'Отримання статус коду 200:{response.status_code}')
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

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/posts') as resp:
            logger_b.info(f' Отримання статус коду {resp.status}')
            if resp.status == 200:
                items = await resp.json()
                for inf in items:
                    if inf['id'] <= 5:
                        logger_b.info(f'Дані:{inf}')
                        write_to_db(inf['title'],inf['body'])

asyncio.run(main())