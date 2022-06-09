from dagster import repository
from scrap_cmc import process_scrap_cmc_news
from scrap_decrypt import process_scrap_decrypt_news


@repository
def my_repo():
    return [process_scrap_decrypt_news, process_scrap_cmc_news]
