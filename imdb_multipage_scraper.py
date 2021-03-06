import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

# initialize empty lists where you'll store your data
titles = []
years = []
times = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

headers = {"Accept-Language": "en-US, en;q=0.5"}

# start, stop (not included would just go to 1000), step
pages = np.arange(1, 1001, 50)

for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" +
                        str(page) + "&ref_=adv_nxt", headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    sleep(randint(2, 10))

    # initiate the for loop
    # this tells your scraper to iterate through
    # every div container we stored in movie_div
    for container in movie_div:
        # name
        name = container.h3.a.text
        titles.append(name)
        # year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)
        # runtime
        time = container.p.find('span', class_='runtime').text
        times.append(time)
        # rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
        # metascore
        metascore = container.find('span', class_='metascore').text if container.find(
            'span', class_='metascore') else '-'
        metascores.append(metascore)
        # gets both votes and grosses
        nv = container.find_all('span', attrs={'name': 'nv'})
        # filter nv for votes
        vote = nv[0].text
        votes.append(vote)
        # filter nv for gross
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': times,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].str.extract('(\d+)')
movies['metascore'] = pd.to_numeric(
    movies['metascore'], errors='coerce')
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(
    lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(
    movies['us_grossMillions'], errors='coerce')

# check how much missing data
print(movies.isnull().sum())

movies.metascore = movies.metascore.fillna("None Given")
print(movies['metascore'])
movies.us_grossMillions = movies.us_grossMillions.fillna("")
print(movies['us_grossMillions'])

movies.to_csv('mult-movies.csv')
