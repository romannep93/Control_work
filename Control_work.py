import argparse
import re
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='link_checker.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def validate_url(url):
    response = requests.head(url)
    return response.status_code == 200


def get_valid_links(url):
    if not validate_url(url):
        logging.error("Invalid URL or status code is not 200: %s", url)
        return []

    response = requests.get(url)
    html_parser = BeautifulSoup(response.text, "html.parser")
    links = []
    for link in html_parser.find_all('a'):
        href_attribute = link.get("href")
        if href_attribute:
            links.append(href_attribute)
    return links


def validate_links(links):
    valid_links = []
    invalid_links = []
    for link in links:
        if link.startswith('http://') or link.startswith('https://'):
            response = requests.head(link)
            if response.status_code == 200:
                valid_links.append(link)
            else:
                invalid_links.append(link)
        else:
            invalid_links.append(link)
    return valid_links, invalid_links


def save_to_file(valid_links, invalid_links):
    with open("valid_links.txt", "w", encoding="utf-8") as valid_file:
        valid_file.write("\n".join(valid_links))

    with open("broken_links.txt", "w", encoding="utf-8") as invalid_file:
        invalid_file.write("\n".join(invalid_links))


def parse_html(url):
    logging.info("Processing HTML links for URL: %s", url)
    links = get_valid_links(url)
    valid_links, invalid_links = validate_links(links)
    save_to_file(valid_links, invalid_links)

    logging.info("Processing HTML links completed.")


class PDFLinkChecker:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def extract_links(self):
        links = []
        pdf = PdfReader(self.pdf_file)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()

            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z0-9]|[^\s])*')
            urls = re.findall(url_pattern, page_text)

            links.extend(urls)

        return links

    def process_links(self):
        logging.info("Processing PDF links for file: %s", self.pdf_file)
        links = self.extract_links()

        for link in links:
            try:
                response = requests.head(link)
                if response.status_code != 200:
                    with open('broken_links.txt', 'a') as file:
                        file.write(link + '\n')
                        logging.warning("Broken link found: %s", link)
            except requests.exceptions.RequestException:
                with open('broken_links.txt', 'a') as file:
                    file.write(link + '\n')
                    logging.warning("Broken link found: %s", link)
            else:
                with open('valid_links.txt', 'a') as file:
                    file.write(link + '\n')
                    logging.info("Valid link found: %s", link)

        logging.info("Processing PDF links completed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Link Checker')
    parser.add_argument('-url', type=str, help='URL of the webpage')
    parser.add_argument('--pdf', help='Path to the PDF file')
    args = parser.parse_args()

    if not args.url and not args.pdf:
        url = input('Enter the URL: ')
        if not url.startswith('http'):
            url = 'http://' + url
        parse_html(url)

        pdf_file = input('Enter the path to the PDF file: ')
        pdf_link_checker = PDFLinkChecker(pdf_file)
        pdf_link_checker.process_links()
    else:
        if args.url:
            url = args.url
            if not url.startswith('http'):
                url = 'http://' + url
            parse_html(url)
        if args.pdf:
            pdf_file = args.pdf
            pdf_link_checker = PDFLinkChecker(pdf_file)
            pdf_link_checker.process_links()
