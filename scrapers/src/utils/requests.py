import random
import time
from typing import Any, Dict
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


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


def get_random_proxies():
    free_proxies = [
        {'http': 'http://62.33.210.34:58918', 'https': 'http://194.233.69.41:443'},
        {'http': 'http://190.64.18.177:80', 'https': 'http://203.193.131.74:3128'},
    ]
    proxies = {
        'free': free_proxies,
    }

    return random.choice(proxies["free"])


def get_request_headers() -> Dict[str, Any]:
    header_list = [
        {
            'authority': 'httpbin.org',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9'
        }
    ]
    headers = random.choice(header_list)
    return headers


def avoid_detection_request(url: str):
    # TODO: Add proxies for avoid detection request
    return requests.get(url, headers=get_request_headers())
