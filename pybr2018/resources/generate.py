import argparse
import base64
import subprocess

import requests


def generate(url, destination_directory, destination_file_name):
    response = requests.get(url)
    with open('{}/{}.html'.format(destination_directory, destination_file_name), 'wb') as f:
        f.write(response.text.encode('utf8'))
    with open('{}/{}.b64.txt'.format(destination_directory, destination_file_name), 'wb') as f:
        f.write(base64.b64encode(response.text.encode('utf8')))
    zip_command = [
        'zip',
        '{}.b64.txt.zip'.format(destination_file_name),
        '{}.b64.txt'.format(destination_file_name)]
    subprocess.call(zip_command, cwd=destination_directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('destination_directory')
    parser.add_argument('destination_file_name')
    args = parser.parse_args()
    generate(**vars(args))

# python generate.py http://quotes.toscrape.com /Users/eugenio/dev-scrapinghub/scrapy-beyond-first-steps/pybr2018/resources Quotes  # noqa
