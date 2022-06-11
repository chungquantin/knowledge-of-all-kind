from enum import Enum
from typing import Any, Dict, Optional
from jobs import BaseCategorizedJob
from config.providers import Provider
from ops.base_op import BaseCategorizedOpFactory
from utils import build_id

from dagster import JobDefinition, job


class BaseScrapperJob(BaseCategorizedJob):
    def __init__(self,
                 category: Enum,
                 provider: Provider,
                 scrapper_op_factory: BaseCategorizedOpFactory,
                 resource_defs: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            category,
            provider,
        )
        self._resource_defs = resource_defs
        self._scrapper_op_factory = scrapper_op_factory

    @property
    def scrapper_op_factory(self) -> BaseCategorizedOpFactory:
        return self._scrapper_op_factory

    def build(self, **kwargs) -> JobDefinition:
        scrapper_op = self.scrapper_op_factory().create_op(
            category=self.category)

        @job(name=build_id(provider=self.provider,
                           identifier=f"scrap_{self.category}_news_db_job"),
             resource_defs=self.resource_defs,
             **kwargs)
        def _job():
            scrapper_op()

        return _job
