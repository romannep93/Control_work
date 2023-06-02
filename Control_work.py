import argparse
import requests
from bs4 import BeautifulSoup


def validate_url(url):
    response = requests.head(url)
    return response.status_code == 200


def parse_html(url):
    if not validate_url(url):
        print("Invalid URL or status code is not 200.")
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    valid_links = []
    broken_links = []

    for link in links:
        href = link.get('href')
        if href and (href.startswith('http://') or href.startswith('https://')):
            valid_links.append(href)
        else:
            text = link.get_text()
            if text.startswith('http://') or text.startswith('https://'):
                valid_links.append(text)
            else:
                broken_links.append(href or text)

    with open('valid_links.txt', 'a') as valid_file:
        for link in valid_links:
            valid_file.write(link + '\n')

    with open('broken_links.txt', 'a') as broken_file:
        for link in broken_links:
            broken_file.write(link + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webpage Link Parser')
    parser.add_argument('-url', type=str, help='URL of the webpage')
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = input('Enter the URL: ')

    if not url.startswith('http'):
        url = 'http://' + url

    parse_html(url)

    print("Process completed successfully.")
