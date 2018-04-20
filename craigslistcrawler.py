import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

results=[]
print('Let me help you find an apartment in Rhode Island!')
print('')
max_price = int(input('Enter your maximum price? $'))
print('')
print('searching... this will only take a moment!\n')


for count in range(0, 3000, 120):
    urlvary = 'https://providence.craigslist.org/search/apa?s=' + str(count)
    url = requests.get(urlvary).text
    soup = bs(url,'html.parser')
    listings = soup.find_all('li', {'class', 'result-row'})

    for l in listings:
        price = l.find('span', {'class': 'result-price'})
        if price == None:
            pass
        else:
            price = int(price.contents[0][1:])

        location = l.find('span', {'class': 'result-hood'})
        if location == None:
            pass
        else:
            location = l.find('span', {'class': 'result-hood'}).text[2:-1]
            title = l.find('a', {'class': 'result-title'}).text
            link = l.find('a', {'class': 'result-title hdrlnk'})
            link = link.get('href')
            results.append((price, location, title, link))

df = pd.DataFrame(results, columns=['price','location', 'title', 'link',])
bypricedf = df[df.price <= max_price]
sorted_df = bypricedf.sort_values(by = 'price')
sorted_df.to_csv('craigslist.csv', index = False, encoding = 'utf-8')
print(input('I created a CSV file in your working directory with your results!\npress enter to close!'))
