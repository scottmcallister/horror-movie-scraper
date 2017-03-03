import urllib.request
from bs4 import BeautifulSoup

list_of_horror_films = 'https://en.wikipedia.org/wiki/Lists_of_horror_films'


def innerHTML(element):
    return element.decode_contents(formatter="html")


def read_wiki_list_table(url):
    print('\n' + url + '\n')
    with urllib.request.urlopen(url) as wiki_list_response:
        wiki_list_html = wiki_list_response.read()
        wiki_list_soup = BeautifulSoup(wiki_list_html, "html.parser")
        table = wiki_list_soup.find_all('table')[1]
        title_links = table.select('th a')
        for title_link in title_links:
            print(innerHTML(title_link))


with urllib.request.urlopen(list_of_horror_films) as response:
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    ul_tags = soup.find_all('ul')[1:7]
    for ul_tag in ul_tags:
        a_tags = ul_tag.find_all('a')
        for a_tag in a_tags:
            list_page = 'https://en.wikipedia.org' + a_tag['href']
            read_wiki_list_table(list_page)
