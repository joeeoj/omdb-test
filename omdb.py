"""
M.Yu
10/26/2016

Test of omdbapi. Didn't spend any time on parsing file names. Assumption is that 
file/folders follow a 'Title - Year' naming convention. One improvement would be
to replace the `movies` list comprehension with something that more robustly 
searches a given folder for movie names.
"""
from collections import namedtuple
from copy import copy
import json
import os
import requests
import sqlite3
import time
from urllib.parse import urlencode


SLEEP = 2  # rate limiting like all good citizens should
URL = 'http://www.omdbapi.com/?{}'
PARAMS = {
    't': None,
    'y': None,
    'plot': 'short',
    'r': 'json',
    # 'tomatoes': True,
}
Movies = namedtuple('Movies', ['title', 'year'])

def create_url(title, year):
    """Returns formed api call to omdbapi.com"""
    temp = copy(PARAMS)
    temp.update({'t': title, 'y': year})
    return URL.format(urlencode(temp))

# create db with create_table.sql
# > sqlite3 movies.db -init create_table.sql
conn = sqlite3.connect('movies.db')
c = conn.cursor()

movies = [Movies(*f.split(' - ')) for f in os.listdir() if len(f.split(' - ')) == 2]
col_names = ['imdbID', 'Title', 'Year', 'Rated', 'imdbRating', 'Metascore']
total_len = len(movies)
for i, movie in enumerate(movies):
    print('Starting {} out of {}'.format(i+1, total_len))
    try:
        print('Requesting: {} ({})'.format(movie.title, movie.year))
        r = requests.get(create_url(*movie))
    except KeyError as e:
        print('url:', create_url(*movie))
        print('Error:', e)
    data = r.json()
    vals = [data[c] for c in col_names]

    c.execute('''
        INSERT INTO movies (imdb_id, title, year, rated, imdb_rating, metascore) 
        VALUES(?, ?, ?, ?, ?, ?)''', vals)
    conn.commit()

    print('-----sleeping {} seconds-----'.format(SLEEP))
    time.sleep(SLEEP)
