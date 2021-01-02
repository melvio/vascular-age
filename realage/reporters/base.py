#%%
from abc import ABC, abstractmethod
from enum import Enum, auto


class ReportStrategy(Enum):
    TO_FILE = auto()
    TO_STDOUT = auto()
    NO_REPORT = auto()


class UnsupportedStrategy(Exception):
    pass


class MissingColumn(Exception):
    pass


class Reporter(ABC):
    @abstractmethod
    def report(self) -> object:
        """ report on the thing that this reporter is responsible for """
        pass

    @abstractmethod
    def report_to_file(self) -> None:
        """ report on the thing that this reporter is responsible for
            and guarantee a write of this data to some file """
        pass
