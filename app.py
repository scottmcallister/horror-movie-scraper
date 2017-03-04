import urllib.request
import csv
import re
from bs4 import BeautifulSoup

list_of_horror_films = 'https://en.wikipedia.org/wiki/Lists_of_horror_films'


def inner_html(element):
    return element.decode_contents(formatter="html")


def get_cell_value(table_cell):
    if len(table_cell.select('a')) > 0:
        return inner_html(table_cell.select('a')[0])
    elif len(table_cell.select('i')) > 0:
        return inner_html(table_cell.select('i')[0])
    else:
        return inner_html(table_cell)


def read_country_flags(movie_row):
    if len(movie_row.select('td')) < 3:
        return ''
    else:
        country_names = ''
        flag_table_cell = movie_row.select('td')[2]
        flag_images = flag_table_cell.select('img')
        for image in flag_images[:-1]:
            country_names += image['alt'] + ' & '
        if len(flag_images) > 0:
            country_names += flag_images[-1]['alt']
        return country_names


def name_to_rt_url(name):
    converted_name = re.sub(r'([^\s\w]|_)+', '', name) \
        .replace(' ', '_').lower()
    url = 'https://rottentomatoes.com/m/' + converted_name
    return url


def name_with_year_to_rt_url(name, year):
    url = name_to_rt_url(name)
    return url + '_' + str(year)


def read_wiki_list_table(url, csv_writer):
    year = url[-4:]
    print('collecting films from ' + year)
    with urllib.request.urlopen(url) as wiki_list_response:
        wiki_list_html = wiki_list_response.read()
        wiki_list_soup = BeautifulSoup(wiki_list_html, "html.parser")
        table = wiki_list_soup.find_all('table')[1]
        movie_rows = table.find_all('tr')[1:]
        for movie_row in movie_rows:
            title = get_cell_value(movie_row.select('th')[0])
            director = get_cell_value(movie_row.select('th')[1]) \
                if len(movie_row.select('td')) < 1 \
                else get_cell_value(movie_row.select('td')[0])
            country = read_country_flags(movie_row)
            csv_row_contents = {
                'title': title,
                'director': director,
                'year': year,
                'country': country,
            }
            csv_writer.writerow(csv_row_contents)


print(name_to_rt_url("Don't Breathe"))
print(name_with_year_to_rt_url("Don't Breathe", 2016))

# with open('movies.csv', 'w+') as csvfile:
#     fieldnames = ['title', 'director', 'year', 'country']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     with urllib.request.urlopen(list_of_horror_films) as response:
#         html = response.read()
#         soup = BeautifulSoup(html, "html.parser")
#         ul_tags = soup.find_all('ul')[1:7]
#
#         for ul_tag in ul_tags:
#             a_tags = ul_tag.find_all('a')
#             for a_tag in a_tags:
#                 list_page = 'https://en.wikipedia.org' + a_tag['href']
#                 read_wiki_list_table(list_page, writer)
