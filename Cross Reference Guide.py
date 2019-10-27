## Cross reference guide for bible search
from os import listdir # list all files in a directory
import pandas as pd # data manipulation

PATH = "bible/"

BOOKS = 'key_english.csv' # a constant, the file with book numbers
df_books = pd.read_csv(PATH + BOOKS) # load data into dataframe 

KING_JAMES = 't_kjv.csv' # a constant, the tail end of the file with the verses of the KJV bible
df_verses = pd.read_csv(PATH + KING_JAMES) # load verses into dataframe

heb_books = df_books.loc[df_books['t'] == 'OT']

heb_verses = df_verses[df_verses['b']<=39]
heb_verses.tail()

print(heb_books[['b','n']])

print('What is the verse you chose? Type and press enter...')

user = {}
user['book_num'] = int(input('Book (select number from list above): '))
user['book_name'] = book_num_to_name(int(user['book_num']))
user['chap'] = int(input("Chapter: "))
user['verse'] = int(input("Verse: "))
