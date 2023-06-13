import argparse
import re
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, filename='link_checker.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


class LinkValidator:
    @staticmethod
    def is_valid(link):
        try:
            response = requests.head(link)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


class LinkExtractor:
    def __init__(self, url):
        self.url = url

    def extract_links(self):
        if not LinkValidator.is_valid(self.url):
            logging.error("Invalid URL or status code is not 200: %s", self.url)
            return []

        response = requests.get(self.url)
        html_parser = BeautifulSoup(response.text, "html.parser")
        links = []
        for link in html_parser.find_all('a'):
            href_attribute = link.get("href")
            if href_attribute:
                links.append(href_attribute)
        return links


class LinkProcessor:
    def __init__(self):
        self.valid_links = []
        self.invalid_links = []

    def process_links(self, links):
        validator = LinkValidator()
        for link in links:
            if validator.is_valid(link):
                self.valid_links.append(link)
                logging.info("Valid link found: %s", link)
            else:
                self.invalid_links.append(link)
                logging.warning("Broken link found: %s", link)


class FileWriter:
    @staticmethod
    def save_links(links, file_path):
        with open(file_path, "a", encoding="utf-8") as file:
            for link in links:
                file.write(link + '\n')


class PDFLinkChecker:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def extract_links(self):
        links = []
        pdf = PdfReader(self.pdf_file)
        for page in pdf.pages:
            page_text = page.extract_text()

            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z0-9]|\S)*')
            urls = re.findall(url_pattern, page_text)

            links.extend(urls)

        return links

    def process_links(self):
        logging.info("Processing PDF links for file: %s", self.pdf_file)
        links = self.extract_links()

        link_processor = LinkProcessor()
        link_processor.process_links(links)

        FileWriter.save_links(link_processor.valid_links, 'valid_links.txt')
        FileWriter.save_links(link_processor.invalid_links, 'broken_links.txt')

        logging.info("Processing PDF links completed.")


def process_url(url):
    link_extractor = LinkExtractor(url)
    links = link_extractor.extract_links()

    link_processor = LinkProcessor()
    link_processor.process_links(links)

    FileWriter.save_links(link_processor.valid_links, 'valid_links.txt')
    FileWriter.save_links(link_processor.invalid_links, 'broken_links.txt')


def process_pdf(pdf_file):
    pdf_link_checker = PDFLinkChecker(pdf_file)
    pdf_link_checker.process_links()


def main():
    parser = argparse.ArgumentParser(description='Link Checker')
    parser.add_argument('-url', type=str, help='URL of the webpage')
    parser.add_argument('--pdf', help='Path to the PDF file')
    args = parser.parse_args()

    if not args.url and not args.pdf:
        while True:
            user_choice = input("Choose an option (pdf or url): ")
            if user_choice.lower() == "pdf":
                pdf_file = input("Enter the path to the PDF file: ")
                process_pdf(pdf_file)
                break
            elif user_choice.lower() == "url":
                url = input("Enter the URL: ")
                if not url.startswith('http'):
                    url = 'http://' + url
                process_url(url)
                break
            else:
                print("Invalid choice. Please choose 'pdf' or 'url'.")

    else:
        if args.url:
            url = args.url
            if not url.startswith('http'):
                url = 'http://' + url
            process_url(url)

        if args.pdf:
            pdf_file = args.pdf
            process_pdf(pdf_file)

    print("Link checking completed.")


if __name__ == '__main__':
    main()
