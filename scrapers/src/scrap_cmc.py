from dagster import job, op
from utils import save_json_file, cmc_data_source

from classes.news_scrapper import NewsCardScraper


@op
def scrap_cmc_news():
    print("====> Scrapping CoinMarketCap News...")
    scrapped_data = NewsCardScraper(cmc_data_source).process_scrap()
    save_json_file("dataset/coinmarketcap.json", scrapped_data)


@job
def process_scrap_cmc_news():
    scrap_cmc_news()
