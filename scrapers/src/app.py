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
    "url": "https://coinmarketcap.com/headlines/news/",
    "html": {
        "card_class": "sc-16r8icm-0 sc-5q2msl-0 fFalqR",
        "card_title_class": "sc-1eb5slv-0 kLhpLY cmc-link",
        "img_wrapper_class": "cover-image",
    }
}

coindesk_data_source = {}

data_source: List[Dict[str, Any]] = [cmc_data_source]


class HeadlessBrowser():
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def scroll_to_bottom(self, url: str, pages: int):
        no_of_pagedowns = pages
        self.browser.get(url)
        time.sleep(1)
        elem = self.browser.find_element_by_tag_name("body")
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

    def get_noscript_img(self, img_wrapper: bs4.element.Tag) -> str:
        noscript = img_wrapper.find("noscript")
        img_src = noscript.find("img").get("src")
        return img_src

    def convert_data_to_json(self, tag: bs4.element.Tag) -> dict:
        img_wrapper = tag.findChild(
            "div", {"class": self.data_source["html"]["img_wrapper_class"]})
        img_src = self.get_noscript_img(img_wrapper)
        card_title = tag.findChild(
            "a", {"class": self.data_source["html"]["card_title_class"]})
        title = card_title.text
        href = card_title.get("href")

        data = {
            "title": title,
            "href": href,
            "img_src": img_src
        }
        return data

    def process_scrap(self) -> Dict[str, Any]:
        response = requests.get(self.data_source["url"])
        return self.process_soup(response.content)

    def process_scrap_inifinite_load(self) -> Dict[str, Any]:
        page_source = HeadlessBrowser().scroll_to_bottom(
            self.data_source["url"], 10)
        return self.process_soup(page_source)

    def process_soup(self, data):
        soup: BeautifulSoup = BeautifulSoup(data, "html.parser")
        news_element = soup.find_all(
            "div", {"class": self.data_source["html"]["card_class"]})

        converted_data = [self.convert_data_to_json(
            element) for element in news_element]

        return {
            "data": converted_data,
            "length": len(converted_data)
        }


print(NewsCardScraper(data_source=cmc_data_source).process_scrap())
