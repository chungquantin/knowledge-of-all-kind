from typing import Any, Dict, List, Optional, Set, Union
from dagster import OpDefinition, Out, get_dagster_logger, op

from classes import NewsCardScraper
from ops.base_op import BaseCategorizedOpFactory
from handlers.coinmarketcap import CoinMarketCapCategory
from config.providers import Provider
from ops.base_op import BaseCategorizedOp
from utils import CategoryKeyError, cmc_data_source, build_id


class CoinMarketCapScrapperOp(BaseCategorizedOp):
    def __init__(
        self,
        category: CoinMarketCapCategory,
        provider: Provider = Provider.COINMARKETCAP,
        required_resource_keys: Optional[Set[str]] = None,
        config_schema: Optional[Union[Dict[str, Any], List]] = None
    ) -> None:
        super().__init__(category, provider, required_resource_keys, config_schema)

    def build(self, **kwargs) -> OpDefinition:
        @op(name=build_id(provider=self.provider,
                          identifier=f"scrap_{self.category}_news_db_op"),
            config_schema=self.config_schema,
            required_resource_keys=self.required_resource_keys,
            **kwargs)
        def _op():
            data = NewsCardScraper(cmc_data_source).process_scrap(**kwargs)
            get_dagster_logger().log(data)
        return _op


class CoinMarketCapScrapperOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: CoinMarketCapCategory, **kwargs) -> OpDefinition:
        try:
            category = CoinMarketCapCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(CoinMarketCapCategory) from key_err
        scrapper_op = CoinMarketCapScrapperOp(category).build(**kwargs)
        return scrapper_op
