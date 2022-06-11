from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from dagster import OpDefinition

from config.providers import Provider


class BaseOp(ABC):

    @abstractmethod
    def __init__(
            self,
            provider: Provider,
            required_resource_keys: Optional[Set[str]] = None,
            config_schema: Optional[Union[Dict[str, Any], List]] = None) -> None:

        self._provider = provider
        self._required_resource_keys = required_resource_keys
        self._config_schema = config_schema

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def required_resource_keys(self) -> Set[str]:
        return self._required_resource_keys

    @required_resource_keys.setter
    def required_resource_keys(self, required_resource_keys: Set[str]) -> None:
        self._required_resource_keys = required_resource_keys

    @property
    def config_schema(self) -> Optional[Union[Dict[str, Any], List]]:
        return self._config_schema

    @config_schema.setter
    def config_schema(
            self, config_schema: Optional[Union[Dict[str, Any], List]]) -> None:
        self._config_schema = config_schema

    @abstractmethod
    def build(self, **kwargs) -> OpDefinition:
        pass


class BaseCategorizedOp(BaseOp):
    @abstractmethod
    def __init__(
            self,
            category: Enum,
            provider: Provider,
            required_resource_keys: Optional[Set[str]] = None,
            config_schema: Optional[Union[Dict[str, Any], List]] = None) -> None:
        self._category = category
        super().__init__(provider, required_resource_keys, config_schema)

    @property
    def category(self) -> str:
        return self._category


class BaseCategorizedOpFactory(ABC):
    @abstractmethod
    def create_op(self, category: Enum, **kwargs) -> OpDefinition:
        pass
