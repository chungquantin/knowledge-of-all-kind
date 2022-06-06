import json
import bs4
import requests
import time
from typing import Any, Dict, List
from bs4 import BeautifulSoup

from utils import *
from sources import *
from decorators import timer, debug

from schedule import repeat, every, run_pending
import hashlib


class NewsCardScraper():
    def __init__(self, data_source: Dict[str, Any]) -> None:
        self.data_source = data_source

    def get_card_metadata(self, field_name: str) -> Dict[str, Any]:
        return self.data_source["html"]["card_metadata"][field_name]

    def get_card_article(self, field_name: str) -> Dict[str, Any]:
        return self.data_source["html"]["article"][field_name]

    def get_selector(self, field_name: str):
        selector = self.get_card_metadata(field_name).split("@")
        return (selector[0], selector[1])

    def get_img(self, tag: bs4.element.Tag) -> str:
        (el, class_name) = self.get_selector(
            "img_wrapper_class")
        img_wrapper = tag.findChild(
            el, {"class": class_name})
        noscript = img_wrapper.find("noscript")
        img = noscript.find("img")
        if img:
            img_src = img.get("src")
            return img_src
        return img_wrapper.find("img").get("src")

    def get_title(self, tag: bs4.element.Tag) -> str:
        (el, class_name) = self.get_selector("card_title_class")
        card_title = tag.findChild(el, {"class": class_name})
        return card_title.text

    def get_href(self, tag: bs4.element.Tag) -> str:
        (el, class_name) = self.get_selector("href_class")
        card_href = tag.findChild(el, {"class": class_name})
        return card_href.get("href")

    def get_author(self, tag: bs4.element.Tag) -> str:
        (el, class_name) = self.get_selector("author_class")
        card_authors = tag.findChildren(el, {"class": class_name})
        return [card_author.text for card_author in card_authors]

    def get_timestamp(self, tag: bs4.element.Tag) -> str:
        (el, class_name) = self.get_selector("timestamp_class")
        card_timestamp = tag.findChild(el, {"class": class_name})
        return card_timestamp.text

    @timer
    def fetch_news_content(self, href: str):
        response = requests.get(href, headers=getRequestHeaders())
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()

    def convert_data_to_json(self, tag: bs4.element.Tag) -> dict:
        """
            Convert scrapped data to json
        """
        img_src = self.get_img(tag)
        title = self.get_title(tag)
        news_id = hashlib.md5(title.encode()).hexdigest()
        timestamp = self.get_timestamp(tag)
        author = self.get_author(tag)

        href = self.get_href(tag)
        if not (href.__contains__("https://") or href.__contains__("http://")):
            href = self.data_source["base_url"] + href

        content = self.fetch_news_content(href)

        data = {
            "id": news_id,
            "title": title,
            "href": href,
            "img_src": img_src,
            "content": content,
            "timestamp": timestamp,
            "author": author
        }
        return data

    @timer
    def process_scrap(self) -> Dict[str, Any]:
        """
            Process scrapping data from source url and do bs4
        """
        response = requests.get(
            self.data_source["url"], headers=getRequestHeaders())
        return self.process_soup(response.content)

    @timer
    def process_scrap_infinite_load(self) -> Dict[str, Any]:
        """
            Using selenium to load infinite web page
        """
        page_source = HeadlessBrowser().scroll_to_bottom(
            self.data_source["url"], 10)
        return self.process_soup(page_source)

    def process_soup(self, data):
        """
            Using beautiful soup to scrape card detail
        """
        soup: BeautifulSoup = BeautifulSoup(data, "html.parser")
        (card_el, card_class) = self.get_selector("card_class")
        news_element = soup.find_all(
            card_el, {"class": card_class})
        converted_data = [self.convert_data_to_json(
            element) for element in news_element]

        return {
            "data": converted_data,
            "length": len(converted_data),
            "timestamp": time.time()
        }


def save_json_file(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def scrap_decrypt_news():
    print("====> Scrapping Decrypt News...")
    decrypt_page_source = HeadlessBrowser().get_ssg_page_source(
        decrypt_data_source["url"])
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(decrypt_page_source)
    return scrapped_data


def scrap_cmc_news():
    print("====> Scrapping CoinMarketCap News...")
    scrapped_data = NewsCardScraper(cmc_data_source).process_scrap()
    return scrapped_data


data_source: List[Dict[str, Any]] = [
    {"data_source": cmc_data_source, "handler": lambda _: scrap_cmc_news()},
    {"data_source": decrypt_data_source, "handler": lambda _: scrap_decrypt_news()}
]


@repeat(every().hour)
@timer
@debug
def start_scrapping():
    cmc_json = scrap_cmc_news()
    save_json_file("dataset/coinmarketcap.json", cmc_json)

    decrypt_json = scrap_decrypt_news()
    save_json_file("dataset/decrypt.json", decrypt_json)


while True:
    run_pending()
    time.sleep(1)
