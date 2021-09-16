import abc
from typing import Union, AnyStr, List

from pandas import DataFrame

class DataCleaner(metaclass=abc.ABCMeta):
    def __init__(self, by):
        self.by = by

    @abc.abstractmethod
    def clean(self, *args, **kwargs):
        pass

    @staticmethod
    def testColsExists(data: DataFrame, col: Union[AnyStr, List]):
        if isinstance(col, str):
            return col in data.columns
        return set(col).issubset(data.columns)