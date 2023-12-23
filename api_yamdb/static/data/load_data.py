import sqlite3
import pandas as pd

con = sqlite3.connect('C:/Dev/api_yamdb/api_yamdb/db.sqlite3')
cursor = con.cursor()

DATA_TABLE = [['category.csv',
               'reviews_category',
              'INSERT INTO reviews_category (id, name, slug)'
               ' VALUES (?, ?, ?)'],
              ['genre.csv',
               'reviews_genre',
              'INSERT INTO reviews_genre (id, name, slug)'
               ' VALUES (?, ?, ?)'],
              ['titles.csv',
               'reviews_title',
              'INSERT INTO reviews_title (id, name, year, category)'
               ' VALUES (?, ?, ?, ?)'],
              ['genre_title.csv',
               'reviews_genretitle',
              'INSERT INTO reviews_genretitle (id, genre_id, title_id)'
               ' VALUES (?, ?, ?)'],
              ['comments.csv',
               'reviews_comment',
              'INSERT INTO reviews_comment '
               '(id, text, pub_date, author, review_id)'
               ' VALUES (?, ?, ?, ?, ?)'],
              ['review.csv',
               'reviews_review',
              'INSERT INTO reviews_review '
               '(id, text, pub_date, score, author, title_id)'
               ' VALUES (?, ?, ?, ?, ?, ?)'],
              ['users.csv',
               'users_user',
              'INSERT INTO users_user (id, username, email,'
               'first_name, last_name, bio, role)'
               ' VALUES (?, ?, ?, ?, ?, ?, ?)']
              ]

for table in DATA_TABLE:
    reader = pd.read_csv(table[0])
    reader.to_sql(table[1], con, if_exists='replace', index=False)
    records = cursor.fetchall()
    for row in records:
        print(row)
    cursor.executemany(
        table[2],
        records)
    con.commit()
con.close()
