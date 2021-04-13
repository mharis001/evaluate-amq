from abc import ABC, abstractmethod
from typing import TextIO


class BaseTest(ABC):
    """A base class for the various tests."""

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    @abstractmethod
    def export_csv(self, file: TextIO) -> None:
        pass
