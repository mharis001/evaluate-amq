from abc import ABC, abstractmethod

from amq.filteritem import FilterItem


class BaseFilter(ABC):
    """A base class for the various filters."""

    @abstractmethod
    def insert(self, item: FilterItem) -> None:
        pass

    @abstractmethod
    def delete(self, item: FilterItem) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def __contains__(self, item: FilterItem) -> bool:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
