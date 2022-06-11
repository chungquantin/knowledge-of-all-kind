from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional, Set
from config.providers import Provider
from strenum import StrEnum
from dagster import JobDefinition


class BaseJob(ABC):
    @abstractmethod
    def __init__(self,
                 provider: Provider,
                 resource_defs: Optional[Dict[str, Any]] = None) -> None:
        self._provider = provider
        self._resource_defs = resource_defs

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def resource_defs(self) -> Set[str]:
        return self._resource_defs

    @resource_defs.setter
    def resource_defs(self, resource_defs: Dict[str, Any]) -> None:
        self._resource_defs = resource_defs

    @abstractmethod
    def build(self, **kwargs) -> JobDefinition:
        pass


class BaseCategorizedJob(BaseJob):
    @abstractmethod
    def __init__(self,
                 category: Enum,
                 provider: Provider,
                 resource_defs: Optional[Dict[str, Any]] = None) -> None:
        self._category = category
        super().__init__(provider, resource_defs)

    @property
    def category(self) -> str:
        return self._category


class BaseCategorizedJobFactory(ABC):
    @abstractmethod
    def create_job(self, category: Enum, **kwargs) -> JobDefinition:
        pass


def init_categorized_job(factory: BaseCategorizedJobFactory, categories: StrEnum) -> JobDefinition:
    jobs = [factory.create_job(category) for category in categories]
    return jobs
