import urllib.request
from bs4 import BeautifulSoup

list_of_horror_films = 'https://en.wikipedia.org/wiki/Lists_of_horror_films'

with urllib.request.urlopen(list_of_horror_films) as response:
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    ul_tags = soup.find_all('ul')[1:7]
    for ul_tag in ul_tags:
        a_tags = ul_tag.find_all('a')
        for a_tag in a_tags:
            print(a_tag['href'])
