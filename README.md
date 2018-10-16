Scrapy beyond the first steps
=============================

This the Scrapy project I'm basing my talk at [Python Brasil 2018](https://2018.pythonbrasil.org.br/evento)

Most of the components (pipelines, item exporters, middlewares) are enabled by default.


#### Install requirements:

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```


#### Run some spiders

```
$ scrapy crawl books -o books.json

$ cat books.json | jq .
[
  {
    "price": 51.7,
    "title": "A Light in the Attic",
    "url": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  },
  {
    "price": 47.82,
    "title": "Sharp Objects",
    "url": "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
  },
...
```

```
$ scrapy crawl temperature -o temperature.json

$ cat temperature.json | jq .
[
  {
    "destination": "115.594409475582 Fahrenheit",
    "source": "46.441338597545496 Celsius"
  },
  {
    "destination": "51.3302595502288 Fahrenheit",
    "source": "10.73903308346043 Celsius"
  },
...
```
