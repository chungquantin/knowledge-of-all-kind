import json
import time
from classes import NewsCardScraper
from utils import *

import schedule
import schedule
import threading


def save_json_file(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def scrap_decrypt_news():
    print("====> Scrapping Decrypt News...")
    decrypt_page_source = HeadlessBrowser().get_ssg_page_source(
        decrypt_data_source["url"])
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(decrypt_page_source)
    save_json_file("dataset/decrypt.json", scrapped_data)


def scrap_cmc_news():
    print("====> Scrapping CoinMarketCap News...")
    scrapped_data = NewsCardScraper(cmc_data_source).process_scrap()
    save_json_file("dataset/coinmarketcap.json", scrapped_data)


@schedule.repeat(schedule.every().hour)
@timer
def thread_one():
    print("==> Run thread 1")
    run_threaded(scrap_decrypt_news)


@schedule.repeat(schedule.every().hour)
@timer
def thread_two():
    print("==> Run thread 2")
    run_threaded(scrap_cmc_news)


@auto_invoked_fn
def run_app():
    print("==> Running scrapping service...")
    print("==> Remaining job")
    for job in schedule.get_jobs():
        print(f"+ {job}")
    while True:
        schedule.run_pending()
        time.sleep(1)
