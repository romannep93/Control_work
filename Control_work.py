import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import validators


def validate_url(url):
    return validators.url(url)


def parse_html(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(scheme='http')
    base_url = parsed_url.geturl()

    response = requests.get(base_url)
    if response.status_code != 200:
        with open('broken_links.txt', 'a') as file:
            file.write(url + '\n')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    valid_links = []
    broken_links = []
    for link in links:
        href = link.get('href')
        if href and validate_url(href):
            valid_links.append(href)
        else:
            broken_links.append(href)

        text = link.get_text()
        if text and validate_url(text):
            valid_links.append(text)

    with open('valid_links.txt', 'a') as valid_file:
        for link in valid_links:
            valid_file.write(link + '\n')

    with open('broken_links.txt', 'a') as broken_file:
        for link in broken_links:
            broken_file.write(link + '\n')

    print("Process completed successfully.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', type=str, help='URL of the HTML page')
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = input('Enter the URL: ')

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parse_html(url)


if __name__ == '__main__':
    main()
