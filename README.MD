LinkValidator: This class contains the is_valid method, which performs a check to determine if a link is valid by sending a HEAD request and examining the response status code (200 - success).

LinkExtractor: This class is responsible for extracting all links from a webpage. It takes a URL as input, validates it using LinkValidator, and then uses requests and BeautifulSoup to extract all links from the HTML code of the page.

LinkProcessor: This class handles the processing of a list of links. It takes a list of links, uses LinkValidator to check each link's validity, and stores valid and invalid links in separate lists.

FileWriter: This class includes the save_links static method, which takes a list of links and a file path as input, and saves each link to the specified file.

PDFLinkChecker: This class is responsible for processing PDF files. It extracts all links from a PDF file using PyPDF2 and performs link processing using LinkProcessor. It then saves the valid and invalid links to separate files.

In the if __name__ == '__main__': block, command-line arguments are defined using argparse. If the url or pdf arguments are not provided, the user is prompted to enter a URL manually. The script then performs link checking based on the entered URL. If the pdf argument is provided, link checking is performed on the specified PDF file.

