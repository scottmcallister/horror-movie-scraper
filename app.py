import urllib.request
import csv
import re
import json
from bs4 import BeautifulSoup

list_of_horror_films = 'https://en.wikipedia.org/wiki/Lists_of_horror_films'


def convert_name(name):
    s = re.sub(r'([^\s\w]|_)+', '', name) \
        .replace(' ', '_').lower()
    return "".join(i for i in s if ord(i) < 128)


def select_html(selector, html):
    if len(html.select(selector)) > 0:
        return html.select(selector)[0]
    else:
        new_html = BeautifulSoup("<p></p>", "html.parser")
        return new_html.select('p')[0]


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
    converted_name = convert_name(name)
    url = 'https://rottentomatoes.com/m/' + converted_name
    return url


def name_with_year_to_rt_url(name, year):
    url = name_to_rt_url(name)
    return url + '_' + str(year)


def url_from_api_response(name, year):
    api = 'https://www.rottentomatoes.com/api/private/v1.0/search/'
    query_params = '?catCount=10&q=' + convert_name(name).replace('_', '+')
    api_url = api + query_params
    try:
        with urllib.request.urlopen(api_url) as api_response:
            data = json.loads(api_response.read().decode('iso-8859-15'))
            for movie in data['movies']:
                if str(movie.get('year', '')) == str(year):
                    return 'https://rottentomatoes.com' + movie['url']
            return ''
    except urllib.error.HTTPError:
        return ''


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
            rt_url = name_to_rt_url(title)
            rt_content = read_rt_content(rt_url, title, year)
            csv_row_contents = {
                'title': title,
                'director': director,
                'year': year,
                'country': country,
                'critic_score': rt_content['critic_score'],
                'user_score': rt_content['user_score'],
            }
            csv_writer.writerow(csv_row_contents)


def read_rt_year_suffix(rt_url):
    print(rt_url)
    with urllib.request.urlopen(rt_url) as rt_response:
        rt_html = rt_response.read()
        rt_soup = BeautifulSoup(rt_html, "html.parser")
        critic_score = select_html('.critic-score .meter-value span', rt_soup)
        user_score = select_html('.audience-score .meter-value span', rt_soup)
        response = {
            'critic_score': inner_html(critic_score),
            'user_score': inner_html(user_score),
        }
        return response


def read_rt_content(rt_url, title, year):
    print(rt_url)
    try:
        with urllib.request.urlopen(rt_url) as rt_response:
            rt_html = rt_response.read()
            rt_soup = BeautifulSoup(rt_html, "html.parser")
            # check if movie is from the right year
            year_string = str(inner_html(select_html('span.year', rt_soup)))
            rt_year = year_string[year_string.find("(") +
                                  1:year_string.find(")")]
            if str(rt_year) != str(year):
                return read_rt_year_suffix(rt_url + '_' + str(year))
            else:
                critic_score = select_html('.critic-score .meter-value span',
                                           rt_soup)
                user_score = select_html('.audience-score .meter-value span',
                                         rt_soup)
                response = {
                    'critic_score': inner_html(critic_score),
                    'user_score': inner_html(user_score),
                }
                return response
    except urllib.error.HTTPError:
        url_from_api = url_from_api_response(title, year)
        if len(url_from_api) > 0 and url_from_api != rt_url:
            return read_rt_content(url_from_api, title, year)
        else:
            return {
                'critic_score': '',
                'user_score': '',
            }


with open('movies.csv', 'w+') as csvfile:
    fieldnames = [
        'title',
        'director',
        'year',
        'country',
        'critic_score',
        'user_score'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with urllib.request.urlopen(list_of_horror_films) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        ul_tags = soup.find_all('ul')[1:7]

        for ul_tag in ul_tags:
            a_tags = ul_tag.find_all('a')
            for a_tag in a_tags:
                list_page = 'https://en.wikipedia.org' + a_tag['href']
                read_wiki_list_table(list_page, writer)
