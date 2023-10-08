import requests
from bs4 import BeautifulSoup
import json
import sqlite3



url = 'https://quotes.toscrape.com/'
response = requests.get(url) 
soup = BeautifulSoup(response.text,"lxml")
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')
some_data = dict()
for i in range(len(quotes)):
    print(quotes[i].text)
    print(authors[i].text)
    print(tags[i].text.split()[1:])
    keys_aut = str(authors[i].text) + str(i)
    some_data[keys_aut] = quotes[i].text
    
print(some_data)

with open("result.json", "w", encoding="utf-8") as file:
    json.dump(some_data, file)

createSQL = """CREATE TABLE IF NOT EXISTS quotes (author TEXT, quote TEXT, tags TEXT)"""
conn =sqlite3.connect("data_from_web.db")
cursor = conn.cursor()
cursor.execute(createSQL)
SQL = """INSERT INTO quotes (author, quote, tags) VALUES (?,?,?)"""

for i in range(len(quotes)):
    quote = quotes[i].text
    author = authors[i].text
    tag = ', '.join(tags[i].text.split()[1:])
    cursor.execute(SQL, [author, quote, tag])
    conn.commit()