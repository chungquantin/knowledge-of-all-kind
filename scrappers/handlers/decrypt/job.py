from dagster import JobDefinition

from config.providers import Provider
from jobs.base_jobs import BaseCategorizedJobFactory
from jobs.base_scrapper_job import BaseScrapperJob
from handlers.decrypt.category import DecryptCategory
from handlers.decrypt.ops import DecryptScrapperOpFactory
from utils.errors import CategoryKeyError


class DecryptScrapperJob(BaseScrapperJob):
    def __init__(
            self,
            category: DecryptCategory,
    ) -> None:
        super().__init__(
            category=category,
            provider=Provider.DECRYPT,
            scrapper_op_factory=DecryptScrapperOpFactory,
            resource_defs=None
        )


class DecryptScrapperJobFactory(BaseCategorizedJobFactory):
    def create_job(self, category: DecryptCategory, **kwargs) -> JobDefinition:
        try:
            category = DecryptCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(DecryptCategory) from key_err
        scrapper_job = DecryptScrapperJob(category).build(**kwargs)
        return scrapper_job
