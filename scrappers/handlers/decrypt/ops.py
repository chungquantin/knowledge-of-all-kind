from typing import Any, Dict, List, Optional, Set, Union
from dagster import OpDefinition, get_dagster_logger, op

from classes import NewsCardScraper
from ops.base_op import BaseCategorizedOpFactory
from handlers.decrypt import DecryptCategory
from config.providers import Provider
from ops.base_op import BaseCategorizedOp
from utils import CategoryKeyError, build_id, decrypt_data_source


class DecryptScrapperOp(BaseCategorizedOp):
    def __init__(
        self,
        category: DecryptCategory,
        provider: Provider = Provider.DECRYPT,
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
            data = NewsCardScraper(decrypt_data_source).process_scrap(**kwargs)
            get_dagster_logger().log(data)
        return _op


class DecryptScrapperOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: DecryptCategory, **kwargs) -> OpDefinition:
        try:
            category = DecryptCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(DecryptCategory) from key_err
        scrapper_op = DecryptScrapperOp(category).build(**kwargs)
        return scrapper_op
