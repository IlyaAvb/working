import sqlite3
from datetime import datetime


# Получение текущей даты и времени
def get_current_data():
    now = datetime.now()

    # Форматирование даты
    formatted_date = now.strftime("%d-%m-%Y")
    print(formatted_date)
    return formatted_date




conn = sqlite3.connect('database.db')
cur = conn.cursor()

async def start():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS shops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            name TEXT,
            price INTEGER
        )
    ''')

    conn.commit()

async def add_items(data):
    for shop_name, price in data.items():
        cur.execute('INSERT INTO shops (time, name, price) VALUES (?, ?, ?)', (get_current_data(), shop_name, price))
    conn.commit()

async def get_sum_from_db():
    today = get_current_data()
    sum = 0
    select = cur.execute('SELECT * FROM shops WHERE (time) = ?', (today,))
    for i in select:
        sum += i[3]

    return sum








