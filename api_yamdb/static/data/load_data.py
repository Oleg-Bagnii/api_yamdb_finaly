import sqlite3

import pandas as pd

con = sqlite3.connect('./db.sqlite3')
cursor = con.cursor()

DATA_TABLE = [['./static/data/category.csv',
               'reviews_category',
              'INSERT INTO reviews_category (id, name, slug)'
               ' VALUES (?, ?, ?)'],
              ['./static/data/genre.csv',
               'reviews_genre',
              'INSERT INTO reviews_genre (id, name, slug)'
               ' VALUES (?, ?, ?)'],
              ['./static/data/titles.csv',
               'reviews_title',
              'INSERT INTO reviews_title (id, name, year, category)'
               ' VALUES (?, ?, ?, ?)'],
              ['./static/data/genre_title.csv',
               'reviews_genretitle',
              'INSERT INTO reviews_genretitle (id, genre_id, title_id)'
               ' VALUES (?, ?, ?)'],
              ['./static/data/comments.csv',
               'reviews_comment',
              'INSERT INTO reviews_comment '
               '(id, text, pub_date, author, review_id)'
               ' VALUES (?, ?, ?, ?, ?)'],
              ['./static/data/review.csv',
               'reviews_review',
              'INSERT INTO reviews_review '
               '(id, text, pub_date, score, author, title_id)'
               ' VALUES (?, ?, ?, ?, ?, ?)'],
              ['./static/data/users.csv',
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
