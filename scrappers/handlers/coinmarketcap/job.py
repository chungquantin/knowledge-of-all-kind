from dagster import JobDefinition

from config.providers import Provider
from jobs.base_jobs import BaseCategorizedJobFactory
from jobs.base_scrapper_job import BaseScrapperJob
from handlers.coinmarketcap.category import CoinMarketCapCategory
from handlers.coinmarketcap.ops import CoinMarketCapScrapperOpFactory
from utils.errors import CategoryKeyError


class CoinMarketCapScrapperJob(BaseScrapperJob):
    def __init__(
            self,
            category: CoinMarketCapCategory,
    ) -> None:
        super().__init__(
            category=category,
            provider=Provider.COINMARKETCAP,
            scrapper_op_factory=CoinMarketCapScrapperOpFactory,
            resource_defs=None
        )


class CoinMarketCapScrapperJobFactory(BaseCategorizedJobFactory):
    def create_job(self, category: CoinMarketCapCategory, **kwargs) -> JobDefinition:
        try:
            category = CoinMarketCapCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(CoinMarketCapCategory) from key_err
        scrapper_job = CoinMarketCapScrapperJob(category).build(**kwargs)
        return scrapper_job
