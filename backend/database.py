#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  10 08:15:44 2023

@author: aaryanbhutani
"""

import requests
import sqlite3



# we need to Define API key, endpoint, and headers(not sure what order we are using right now)
API_KEY = 'YOUR_API_KEY'
ENDPOINT = 'https://api.openai.com/v1/engines/davinci/completions'  
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}


data = {
    "prompt": "List books with their authors, ratings, and descriptions.",
    "max_tokens": 200 # how many data points do we need? 
}

response = requests.post(ENDPOINT, headers=HEADERS, json=data)
response_data = response.json()['choices'][0]['text'].strip().split("\n")  


books = []
for line in response_data:
    parts = line.split(', ')
    book_name = parts[0].split(' by ')[0].strip()
    author_name = parts[0].split(' by ')[1].strip()
    rating = float(parts[1].split(': ')[1].strip())
    description = parts[2].split(': ')[1].strip()
    books.append((book_name, author_name, rating, description))

# we need to Connect database and insert data
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create the table (only once)
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_name TEXT,
    author_name TEXT,
    rating REAL,
    description TEXT
)
''')

# Insert data into the table
cursor.executemany('INSERT INTO books (book_name, author_name, rating, description) VALUES (?, ?, ?, ?)', books)

# Commit and close
conn.commit()
conn.close()