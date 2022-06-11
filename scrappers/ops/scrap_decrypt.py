from classes import NewsCardScraper
from utils import *

from dagster import In, Out, op, get_dagster_logger


@op(ins={"page_source": In(str)}, out=Out(dict))
def scrap_decrypt(page_source):
    scrapped_data = NewsCardScraper(
        decrypt_data_source).process_soup(page_source)
    get_dagster_logger().info(scrapped_data)
    return scrapped_data
