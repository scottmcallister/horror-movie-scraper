# horror-movie-scraper

A web scraper for reading horror movie information from various websites.

### Installation

After cloning and changing into the project directory, you'll need to create a
virtual environment that uses Python 3.

```
$ git clone https://github.com/scottmcallister/horror-movie-scraper
$ cd horror-movie-scraper
$ virtualenv -p python3 env
$ source env/bin/activate
```

Once you're in your virtual environment, install the project dependencies from
`requirements.txt`.

```
(env) $ pip install -r requirements.txt
```

Now that you have everything set up you can run the script. Downloading all
available reviews should take quite a while.

```
(env) $ python app.py
```

## Running the tests

TODO: add unit tests


## Built With

* [Python 3](https://www.python.org/download/releases/3.0/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
