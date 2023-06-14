import os
import pytest
from Control_work import LinkProcessor, FileWriter, PDFLinkChecker, LinkValidator, LinkExtractor


@pytest.fixture
def create_temp_file(tmpdir):
    file_path = str(tmpdir.join("temp_file.txt"))
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


def test_valid_link_validator():
    link = "https://www.google.com"
    assert LinkValidator.is_valid(link)


def test_valid_link_extractor():
    url = "https://www.google.com"
    link_extractor = LinkExtractor(url)
    links = link_extractor.extract_links()
    assert len(links) > 0


def test_valid_link_processor():
    links = ["https://www.google.com", "https://www.example.com"]
    link_processor = LinkProcessor()
    link_processor.process_links(links)
    assert len(link_processor.valid_links) == len(links)


def test_valid_file_writer(create_temp_file):
    links = ["https://www.google.com", "https://www.example.com"]
    file_path = create_temp_file
    FileWriter.save_links(links, file_path)
    with open(file_path, "r") as f:
        saved_links = f.read().splitlines()
    assert saved_links == links

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in saved_links:
        print(link)


def test_valid_pdf_link_checker():
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


def test_invalid_link_processor():
    links = ["https://www.google.com", "invalid_link"]
    link_processor = LinkProcessor()
    link_processor.process_links(links)
    assert len(link_processor.invalid_links) == 1


def test_invalid_file_writer(create_temp_file):
    links = ["https://www.google.com", "invalid_link"]
    file_path = create_temp_file
    FileWriter.save_links(links, file_path)
    with open(file_path, "r") as f:
        saved_links = f.read().splitlines()
    assert saved_links == links

    # Вывод сохраненных линков
    print("Сохраненные линки:")
    for link in saved_links:
        print(link)


def test_invalid_pdf_link_checker():
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




if __name__ == '__main__':
    pytest.main()
