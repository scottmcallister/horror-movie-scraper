import unittest
from app import *


class TestHorrorScraper(unittest.TestCase):

    def test_convert_name(self):
        name = convert_name("Rosemary's Baby")
        expected_name = "rosemarys_baby"
        self.assertEqual(name, expected_name)

    def test_select_html(self):
        html = "<div><h1 class='title'>V/H/S</h1></div>"
        selector = ".title"
        expected_html = BeautifulSoup("<h1 class='title'>V/H/S</h1>",
                                      "html.parser")
        soup = BeautifulSoup(html, "html.parser")
        output = select_html(selector, soup)
        self.assertEqual(str(expected_html), str(output))

    def test_inner_html(self):
        soup = BeautifulSoup("<div><h2>Psycho</h2></div>", "html.parser")
        element = soup.select('h2')[0]
        output = inner_html(element)
        expected_output = "Psycho"
        self.assertEqual(output, expected_output)

    def test_get_cell_value(self):
        html = "<td><i>The Exorcist</i></td>"
        soup = BeautifulSoup(html, "html.parser")
        cell = soup.select('td')[0]
        value = get_cell_value(cell)
        expected_value = "The Exorcist"
        self.assertEqual(value, expected_value)

    def test_read_country_flag(self):
        row_html = '<table><tr><td></td><td></td>' + \
            '<td><img alt="United States"></td><td></td></tr></table>'
        soup = BeautifulSoup(row_html, "html.parser")
        row = soup.find_all('tr')[0]
        flag_value = read_country_flags(row)
        expected_value = "United States"
        self.assertEqual(flag_value, expected_value)

    def test_name_to_rt_url(self):
        expected_url = 'https://rottentomatoes.com/m/it_follows'
        url = name_to_rt_url("It Follows")
        self.assertEqual(url, expected_url)

    def test_name_with_year_to_rt_url(self):
        expected_url = 'https://rottentomatoes.com/m/dont_breathe_2016'
        url = name_with_year_to_rt_url("Don't Breathe", 2016)
        self.assertEqual(url, expected_url)

    def test_url_from_api_response(self):
        expected_url = 'https://www.rottentomatoes.com/m/1009113-halloween'
        url = url_from_api_response("Halloween", 1978)
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
