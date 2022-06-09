from classes import NewsCardScraper
from utils import *

from dagster import job, op


@op
def download_decrypt_page_source():
    return HeadlessBrowser().get_ssg_page_source(
        decrypt_data_source["url"])


@op
def scrap_decrypt_news(page_source):
    print("====> Scrapping Decrypt News...")
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(page_source)
    save_json_file("dataset/decrypt.json", scrapped_data)


@job
def process_scrap_decrypt_news():
    page_source = download_decrypt_page_source()
    scrap_decrypt_news(page_source)
