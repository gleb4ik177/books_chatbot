import psycopg2
import sys
sys.path.append("../")
from config import host, database, user, password
def connect():
    conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
    )
    return conn

def print_books():
    conn = connect()
    q = conn.cursor()
    q.execute('SELECT id, name FROM books')
    books = q.fetchall()
    for id,name in books:
        print(id,name)
    conn.close()

def value_of_attribute(attribute:str, book_id:str):
    conn = connect()
    q = conn.cursor()
    q.execute(f'SELECT {attribute} FROM books WHERE id = {book_id}')
    value = q.fetchone()
    conn.close()
    return value[0]

def authors_by_book_id(book_id:str):
    conn = connect()
    q = conn.cursor()
    q.execute(f'select a.name\
        from authors a \
        join author_to_book ab on a.id = ab.author_id \
        where ab.book_id = {book_id};')
    authors = q.fetchall()
    conn.close()
    return authors
