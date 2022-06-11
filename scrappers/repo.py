from jobs import init_categorized_job
from dagster import RepositoryDefinition, repository
from handlers.coinmarketcap import CoinMarketCapScrapperJobFactory, CoinMarketCapCategory
from handlers.decrypt import DecryptScrapperJobFactory, DecryptCategory

jobs = [
    *(init_categorized_job(DecryptScrapperJobFactory(), DecryptCategory)),
    *(init_categorized_job(CoinMarketCapScrapperJobFactory(), CoinMarketCapCategory)),
]


@repository("SolomonDev")
def solomon_dev() -> RepositoryDefinition:
    return [*jobs]
