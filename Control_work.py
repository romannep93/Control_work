import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import validators


def validate_url(url):
    return validators.url(url)


def parse_html(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(scheme='http')
    base_url = parsed_url.geturl()
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and validate_url(href):
                    links.append(href)
                for text in link.stripped_strings:
                    if validate_url(text):
                        links.append(text)
            absolute_links = [urljoin(base_url, link) for link in links]
            return absolute_links
        else:
            print(f"Error: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return []


def save_valid_links(links, filename):
    with open(filename, 'a') as file:
        for link in links:
            if validate_url(link):
                file.write(link + '\n')


def save_broken_links(links, filename):
    with open(filename, 'a') as file:
        for link in links:
            if not validate_url(link):
                file.write(link + '\n')


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

    parsed_links = parse_html(url)
    save_valid_links(parsed_links, 'valid_links.txt')
    save_broken_links(parsed_links, 'broken_links.txt')

    print("Process completed successfully.")
