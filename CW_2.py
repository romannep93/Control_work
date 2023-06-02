import argparse
import re
import requests
from PyPDF2 import PdfReader

class PDFLinkChecker:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def extract_links(self):
        # Extract all links from the PDF file
        links = []
        pdf = PdfReader(self.pdf_file)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()

            # Find all URLs in the page text using regular expressions
            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z0-9]|[^\s])*')
            urls = re.findall(url_pattern, page_text)

            links.extend(urls)

        return links

    def process_links(self):
        # Extract links from the PDF file
        links = self.extract_links()

        # Check the status code for each link
        for link in links:
            try:
                response = requests.head(link)
                if response.status_code != 200:
                    with open('broken_links.txt', 'a') as file:
                        file.write(link + '\n')
            except requests.exceptions.RequestException:
                with open('broken_links.txt', 'a') as file:
                    file.write(link + '\n')
            else:
                with open('valid_links.txt', 'a') as file:
                    file.write(link + '\n')

        print("Processing links completed.")

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', help='Path to the PDF file')
    args = parser.parse_args()

    # Check if the path to the PDF file is provided in the command-line arguments
    if args.pdf is None:
        print("Please provide the path to the PDF file.")
    else:
        pdf_link_checker = PDFLinkChecker(args.pdf)
        pdf_link_checker.process_links()
