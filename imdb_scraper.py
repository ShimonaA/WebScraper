import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")
# print(soup.prettify())

# initialize empty lists where you'll store your data
titles = []
years = []
times = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

# each movie listing falls under the div w/ lass lister-item mode-advanced
movie_div = soup.find_all('div', class_='lister-item mode-advanced')

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
    metascores.append(int(metascore))
    # gets both votes and grosses
    nv = container.find_all('span', attrs={'name': 'nv'})
    # filter nv for votes
    vote = nv[0].text
    votes.append(vote)
    # filter nv for gross
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

# print("titles: " + str(titles))
# print("years: " + str(years))
# print("times: " + str(times))
# print("ratings: " + str(imdb_ratings))
# print("metascores: " + str(metascores))
# print("votes: " + str(votes))
# print("gross: " + str(us_gross))

# build dataframe to store data nicely in table
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': times,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})

# print(movies) - can just print dataframe to see what the table looks like
# print(movies.dtypes) - see types of each field (e.g. int, boolean, obj, string)

# clean data

# ('(\d+)') says to extract all the digits in the string
# .astype(int) method converts the results to an integer
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
# for number of votes, remove the commans and convert to integer
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
# want to get rid of $ and M
movies['us_grossMillions'] = movies['us_grossMillions'].map(
    lambda x: x.lstrip('$').rstrip('M'))
# can't use .astype(float) here because there are a lot of dashes so would create an error
movies['us_grossMillions'] = pd.to_numeric(
    movies['us_grossMillions'], errors='coerce')

print(movies)
print(movies.dtypes)

movies.to_csv('movies.csv')
