import os
from Control_work import LinkProcessor, FileWriter, PDFLinkChecker, LinkValidator, LinkExtractor


def test_valid_link_validator():
    link = "https://www.google.com"
    assert LinkValidator.is_valid(link)


def test_valid_link_extractor():
    url = "https://www.google.com"
    link_extractor = LinkExtractor(url)
    links = link_extractor.extract_links()
    assert len(links) > 0


def test_valid_link_processor(test_links):
    link_processor = LinkProcessor()
    link_processor.process_links(test_links)
    assert all(link in link_processor.valid_links for link in test_links if link != 'invalid_link')


def test_valid_file_writer(create_temp_file, test_links):
    file_path = create_temp_file
    FileWriter.save_links(test_links, file_path)
    with open(file_path, "r") as f:
        saved_links = f.read().splitlines()
    assert saved_links == test_links

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in saved_links:
        print(link)


def test_valid_pdf_link_checker(create_temp_file):
    pdf_file = os.path.join(os.path.dirname(__file__), "../1.pdf")
    pdf_link_checker = PDFLinkChecker(pdf_file)
    links = pdf_link_checker.extract_links()
    assert len(links) > 0

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in links:
        print(link)


def test_invalid_link_validator():
    link = "invalid_link"
    assert not LinkValidator.is_valid(link)


def test_invalid_link_extractor():
    url = "invalid_url"
    link_extractor = LinkExtractor(url)
    links = link_extractor.extract_links()
    assert len(links) == 0


def test_invalid_link_processor(test_links):
    link_processor = LinkProcessor()
    link_processor.process_links(test_links)
    assert len(link_processor.invalid_links) == 1


def test_invalid_file_writer(create_temp_file, test_links):
    file_path = create_temp_file
    FileWriter.save_links(test_links, file_path)
    with open(file_path, "r") as f:
        saved_links = f.read().splitlines()
    assert saved_links == test_links

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in saved_links:
        print(link)


def test_invalid_pdf_link_checker(create_temp_file):
    pdf_file = os.path.join(os.path.dirname(__file__), "../invalid.pdf")
    pdf_link_checker = PDFLinkChecker(pdf_file)
    try:
        links = pdf_link_checker.extract_links()
    except Exception as e:
        print("Ошибка при извлечении ссылок из PDF:", str(e))
        links = []

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in links:
        print(link)
