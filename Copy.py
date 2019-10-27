

'''
THIS IS A WORK IN PROGRESS -- THANKS FOR YOUR PATIENCE
'''

#!/usr/bin/env python
# coding: utf-8

# In[31]:


##get_ipython().system('jupyter nbconvert --to script config_template.ipynb')


# # Bible Search:
# ### Find verses similar to yours!

# The user will provide information about his chosen Biblical verse, and the computer will return a ranked list of most similar other verses from the Tanach.

# Import Libraries

# In[1]:


from os import listdir # list all files in a directory
import pandas as pd # data manipulation


# First, let us examine what files we have to work with...

# In[3]:


PATH = "bible/"
# listdir(PATH)


# I will use two of these files.
# 1. The `key_english.csv`, which lists and numbers the biblical book names; and 
# 2. The `t_kjv.csv`, which lists and numbers all biblical verses.

# Let us list the books of the bible by name and number.

# In[4]:


BOOKS = 'key_english.csv' # a constant, the file with book numbers
df_books = pd.read_csv(PATH + BOOKS) # load data into dataframe 
# df_books.sample(5) # random sampling of 10 rows from the list of books


# I see the books are labeled in column `t` as either Old or New Testament.
# 
# I will work with only verses from the Hebrew Bible (OT).

# Let us now load the verses into a dataframe. 
# 
# I will use the King James version.

# In[5]:


KING_JAMES = 't_kjv.csv' # a constant, the tail end of the file with the verses of the KJV bible
df_verses = pd.read_csv(PATH + KING_JAMES) # load verses into dataframe
# df_verses.sample(5)


# I want the verses in which the book, i.e. `df_verses['b']` has a `OT` in the testament column of the list of books, i.e. `df_books['t']`.

# In[6]:


heb_books = df_books.loc[df_books['t'] == 'OT']
# heb_books.tail(5)


# Notice that the Hebrew books go up to number 39. Let's exlude anything higher.

# In[10]:


heb_verses = df_verses[df_verses['b']<=39][:5000]
heb_verses.tail()
# heb_verses.shape
# type(df_books['t'][0])


# Sure enough, the last verse is the final verse of Malachi, as we wished. 
# 
# Now let's ask the user to provide us the info about his chosen verse. 

# In[11]:


heb_books[['b','n']]


# In[12]:


def book_num_to_name(n):
    """
    given the index, produce the book name
    e.g. 1 results in genesis
    """
    return heb_books.loc[ heb_books['b'] == n ]['n'].iloc[0]
# book_num_to_name(2)



# In[13]:


print('What is the verse you chose? Type and press enter...')


# In[15]:


user = {}
user['book_num'] = int(input('Book (select number from list above): '))
user['book_name'] = book_num_to_name(int(user['book_num']))
user['chap'] = int(input("Chapter: "))
user['verse'] = int(input("Verse: "))
user


# In[16]:


def id_to_book(verse_id):
    book_num = heb_verses.loc[heb_verses['id'] == verse_id]['b'].iloc[0]
    book_name = book_num_to_name(book_num)
    result = {}
    result['num'] = book_num
    result['name'] = book_name
    return result
id_to_book(1002001)


# In[17]:


user['verse']
my_id = user['book_num']*1000000 + user['chap']*1000 + user['verse']
my_id


# In[18]:


my_row = heb_verses.loc[ heb_verses['id'] == my_id ] # select the row of verses in which 'id' matches my_id
my_row


# In[19]:


my_verse = my_row['t'].iloc[0] #
# print(type(my_verse))
# print(my_verse)


# In[20]:


# TF IDF stands for "term frequency – inverse document frequency"
# it is a a numerical statistic that is intended to reflect how important a word is
# to a document in a collection or corpus.
from sklearn.feature_extraction.text import TfidfVectorizer # Convert a collection of raw documents to a matrix of TF-IDF features
from sklearn.metrics.pairwise import linear_kernel


# In[21]:


tf = TfidfVectorizer(analyzer='word', # the feature should be made of word (not character) n-grams
                     ngram_range=(1, 3), # the inclusive range of n-values for different n-grams to be extracted
                     min_df=0, # When building the vocabulary, ignore terms that have a document frequency strictly lower than this threshold
                     stop_words='english' # passed to _check_stop_list and the appropriate stop list is returned
                    ) 


# In[22]:


tfidf_matrix = tf.fit_transform(heb_verses['t']) # Learn vocabulary and idf, return term-document matrix.


# In[23]:


cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) # dot product


# In[24]:


results = {}
"""
dict where each key is an id in the list of verses and 
the entry for that key is a ranked list of id's belonging to 
verses that are most simliar to the key
"""
for idx, row in heb_verses.iterrows(): # 
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1] # numpy.ndarray
    #print(type(similar_indices))
    similar_rows = [(cosine_similarities[idx][i], heb_verses['id'][i]) for i in similar_indices] # list of 
    #print(type(similar_rows))
    # First row is the row itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, row_id)
    results[row['id']] = similar_rows[1:]
    
print('done!')


# In[25]:


def get_verse_text(id):
    """
    get the words of the verse, given the id
    """
    return heb_verses.loc[heb_verses['id'] == id]['t'].values[0]
get_verse_text(my_id)


# In[26]:


def get_verse_num(verse_id):
    return heb_verses.loc[heb_verses['id'] == verse_id]['v'].iloc[0]
get_verse_num(1001011)


# In[27]:


def get_chap(verse_id):
    return heb_verses.loc[heb_verses['id'] == verse_id]['c'].iloc[0]
get_chap(1002001)


# In[28]:


def cit_to_id(book_num,chap,verse):
    """
    given a book number, chap number, and verse number, produce the verse id
    """ 
    return book_num*1000000 + chap*1000 + verse
cit_to_id(1,1,1)


# In[29]:


user


# ### Time to Recommend!

# In[30]:


# reads the results out of the dictionary
def recommend(user, num):
    verse_id = cit_to_id(user['book_num'],user['chap'],user['verse'])
    print("The top {} similar verses to {} {}:{}\n{}".format(num, id_to_book(verse_id)['name'], get_chap(verse_id), get_verse_num(verse_id), get_verse_text(verse_id)))
    print("-------")
    recs = results[verse_id][:num] # the top num items listed in the recomendations for this id
    result = []
    for rec in recs:        
        rank = ''+str(recs.index(rec)+1)+'.)'
        citation = rec[1]
        book = id_to_book(citation)['name']
        chap = get_chap(citation)
        verse = get_verse_num(citation)
        score = str(int(rec[0]*100))[:2]+ "%"
        text = get_verse_text(rec[1])
        print()
        print(rank,score,book,str(chap)+':'+str(verse))
        print()
        print(text)
recommend(user=user, num=6)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


type(ds['t'].iloc[0])


# In[ ]:


ds['t'].iloc[0] == 'In the beginning God created the heaven and the earth.'


# In[ ]:


ds['t'][0]


# In[ ]:


df1 = ds.loc[ds['t']=='In the beginning God created the heaven and the earth.']
df1.head()


# In[ ]:


ds.t.str.startswith('In')


# In[ ]:


# ds[ds.t.str.startswith('In')]


# In[ ]:


keyword = input("Type the word you'd like to find. Then press enter. Your choice: ")


# In[ ]:


keyword


# In[ ]:


df_search = ds[ds['t'].str.contains(keyword)]
# ds[ds['t'].str.contains("song")]


# In[ ]:


df_search.head()


# In[ ]:


df_search[:5]


# In[ ]:


book = book_id_to_name(citation)
chap = get_chap(citation)
verse = get_verse_num(citation)


# In[ ]:


print("These verses contain your keyword '{}'.".format(keyword))
print()
for i in range(0,5):
    print(str(i+1)+'.',df_search.iloc[i]['t'])
    print()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




