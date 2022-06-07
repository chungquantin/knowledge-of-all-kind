import json
import time
from classes import NewsCardScraper
from utils import *

import schedule as scheduler


def save_json_file(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, indent=4, sort_keys=True)


@scheduler.repeat(scheduler.every().hour)
@timer
def scrap_decrypt_news():
    print("====> Scrapping Decrypt News...")
    decrypt_page_source = HeadlessBrowser().get_ssg_page_source(
        decrypt_data_source["url"])
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(decrypt_page_source)
    save_json_file("dataset/decrypt.json", scrapped_data)


@scheduler.repeat(scheduler.every().hour)
@timer
def scrap_cmc_news():
    print("====> Scrapping CoinMarketCap News...")
    scrapped_data = NewsCardScraper(cmc_data_source).process_scrap()
    save_json_file("dataset/coinmarketcap.json", scrapped_data)


@auto_invoked_fn
def run_app():
    print("==> Running scrapping service...")
    print("==> Remaining job")
    for job in scheduler.get_jobs():
        print(f"+ {job}")
    while True:
        scheduler.run_pending()
        time.sleep(1)
