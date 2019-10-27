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

def book_num_to_name(n):
    """
    given the index, produce the book name
    e.g. 1 results in genesis
    """
    return heb_books.loc[ heb_books['b'] == n ]['n'].iloc[0]
# book_num_to_name(2)

user = {}
user['book_num'] = int(input('Book (select number from list above): '))
user['book_name'] = book_num_to_name(int(user['book_num']))
user['chap'] = int(input("Chapter: "))
user['verse'] = int(input("Verse: "))
print('We got you! The verse is...')
print(user)

def id_to_book(verse_id):
    book_num = heb_verses.loc[heb_verses['id'] == verse_id]['b'].iloc[0]
    book_name = book_num_to_name(book_num)
    result = {}
    result['num'] = book_num
    result['name'] = book_name
    return result
##id_to_book(1002001)

# TF IDF stands for "term frequency – inverse document frequency"
# it is a a numerical statistic that is intended to reflect how important a word is
# to a document in a collection or corpus.
from sklearn.feature_extraction.text import TfidfVectorizer # Convert a collection of raw documents to a matrix of TF-IDF features
from sklearn.metrics.pairwise import linear_kernel

tf = TfidfVectorizer(analyzer='word', # the feature should be made of word (not character) n-grams
                     ngram_range=(1, 3), # the inclusive range of n-values for different n-grams to be extracted
                     min_df=0, # When building the vocabulary, ignore terms that have a document frequency strictly lower than this threshold
                     stop_words='english' # passed to _check_stop_list and the appropriate stop list is returned
                    )

tfidf_matrix = tf.fit_transform(heb_verses['t']) # Learn vocabulary and idf, return term-document matrix.

##cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) # dot product

results = {}
"""
dict where each key is an id in the list of verses and 
the entry for that key is a ranked list of id's belonging to 
verses that are most simliar to the key
"""
for idx, row in heb_verses.iterrows(): # 
    similar_indices = cosine_similarities[idx].argsort()[:-10:-1] # numpy.ndarray
    #print(type(similar_indices))
    similar_rows = [(cosine_similarities[idx][i], heb_verses['id'][i]) for i in similar_indices] # list of 
    #print(type(similar_rows))
    # First row is the row itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, row_id)
    results[row['id']] = similar_rows[1:]
    
print('done!')
