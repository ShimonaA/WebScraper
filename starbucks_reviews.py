import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}
url = "https://apps.apple.com/us/app/starbucks/id331177714#see-all/reviews"
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")
# print(soup.prettify())

# initialize empty lists where you'll store your data
dates = []
ratings = []
users = []
headlines = []
texts = []

review_div = soup.find_all(
    'div', class_="ember-view")

for container in review_div:
    # date
    date = container.find('time', class_='we-customer-review_date')
    dates.append(date)

    user = container.find('span', class_='we-customer-review_user')
    users.append(user)

    title = container.h3.find('span', class_='we-customer-review__title')
    headlines.append(title)


print(users)
print(len(users))
print(dates)
print(headlines)
