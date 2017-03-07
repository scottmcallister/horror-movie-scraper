import unittest
from app import *


class TestHorrorScraper(unittest.TestCase):

    def test_convert_name(self):
        name = convert_name("Don't Breathe")
        expected_name = "dont_breathe"
        self.assertEqual(name, expected_name)

    def test_select_html(self):
        html = "<div><h1 class='title'>Hello</h1></div>"
        selector = ".title"
        expected_html = BeautifulSoup("<h1 class='title'>Hello</h1>",
                                      "html.parser")
        soup = BeautifulSoup(html, "html.parser")
        output = select_html(selector, soup)
        self.assertEqual(str(expected_html), str(output))


if __name__ == '__main__':
    unittest.main()

name_test = convert_name("Don't Breathe")
print(name_test)
