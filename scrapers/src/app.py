import json
import bs4
import requests
import time
from typing import Any, Dict, List
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


cmc_data_source: Dict[str, Any] = {
    "name": "CoinMarketCap News",
    "base_url": "https://coinmarketcap.com",
    "url": "https://coinmarketcap.com/headlines/news/",
    "html": {
        "card_metadata": {
            "card_class": "div@sc-16r8icm-0 sc-5q2msl-0 fFalqR",
            "card_title_class": "a@sc-1eb5slv-0 kLhpLY cmc-link",
            "img_wrapper_class": "div@cover-image",
            "href_class": "a@sc-1eb5slv-0 kLhpLY cmc-link",
            "timestamp_class": "span@sc-1t3hyg7-0 hTMYuT",
            "author_class": "span@sc-1eb5slv-0 ehYyPC",
        },
    }
}

decrypt_data_source: Dict[str, Any] = {
    "name": "Decrypt News",
    "base_url": "https://decrypt.co",
    "url": "https://decrypt.co/news",
    "html": {
        "card_metadata": {
            "card_class": "div@sc-e83fcda8-1 gcNmAw border-b mobileUI:border-r border-decryptGridline",
            "card_title_class": "h2@mb-2 font-ak-bold text-base md:text-xl leading-4.5 md:leading-5.5 text-neutral-900 dark:text-primary-200",
            "img_wrapper_class": "div@md:col-span-3 shrink-0 w-22 md:w-auto mr-3 md:mr-0",
            "href_class": "a@block",
            "timestamp_class": "span@font-ak-regular font-normal text-xs md:text-sm text-neutral-700 dark:text-primary-100 leading-3 md:leading-4 whitespace-nowrap",
            "author_class": "span@font-ak-regular font-normal text-xs md:text-sm text-neutral-700 dark:text-primary-100 leading-3 md:leading-4",
        },
    }
}


class HeadlessBrowser():
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def get_ssg_page_source(self, url: str):
        self.browser.get(url)
        self.browser.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(15)
        page_source = self.browser.page_source
        return page_source

    def scroll_to_bottom(self, url: str, pages: int):
        no_of_pagedowns = pages
        self.browser.get(url)
        time.sleep(1)
        elem = self.browser.find_element_by_tag_name("html")
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns -= 1

        page_source = self.browser.page_source
        self.browser.close()
        return page_source


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

    def get_news_content(self, href: str):
        response = requests.get(href)
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()

    def convert_data_to_json(self, tag: bs4.element.Tag) -> dict:
        """
            Convert scrapped data to json
        """
        img_src = self.get_img(tag)
        title = self.get_title(tag)
        timestamp = self.get_timestamp(tag)
        author = self.get_author(tag)

        href = self.get_href(tag)
        if not (href.__contains__("https://") or href.__contains__("http://")):
            href = self.data_source["base_url"] + href

        content = self.get_news_content(href)

        data = {
            "title": title,
            "href": href,
            "img_src": img_src,
            "content": content,
            "timestamp": timestamp,
            "author": author
        }
        return data

    def process_scrap(self) -> Dict[str, Any]:
        """
            Process scrapping data from source url and do bs4
        """
        response = requests.get(self.data_source["url"])
        return self.process_soup(response.content)

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
            "length": len(converted_data)
        }


def save_json_file(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def scrap_decrypt_news():
    decrypt_page_source = HeadlessBrowser().get_ssg_page_source(
        decrypt_data_source["url"])
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(decrypt_page_source)
    return scrapped_data


def scrap_cmc_news():
    scrapped_data = NewsCardScraper(cmc_data_source).process_scrap()
    return scrapped_data


data_source: List[Dict[str, Any]] = [
    {"data_source": cmc_data_source, "handler": lambda _: scrap_cmc_news()},
    {"data_source": decrypt_data_source, "handler": lambda _: scrap_decrypt_news()}
]


cmc_json = scrap_cmc_news()
save_json_file("dataset/coinmarketcap.json", cmc_json)

decrypt_json = scrap_decrypt_news()
save_json_file("dataset/decrypt.json", decrypt_json)
