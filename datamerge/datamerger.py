import abc
from typing import Union, AnyStr, List

from pandas import DataFrame
from exceptionDefine import NoDefaultColumnToMerge


class DataMerger(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        pass

    def __hasSameCol(self, left: DataFrame, right: DataFrame):
        return len(set(left.columns).intersection(right.columns)) > 0

    def auxMerge(self, left: DataFrame, right: DataFrame, how: str = 'left', left_on=None, right_on=None, **kwargs):
        if left_on == None:
            if self.__hasSameCol(left, right):
                return left.merge(right)
            raise NoDefaultColumnToMerge
        return left.merge(right, how=how, left_on=left_on, right_on=right_on, **kwargs)


class LeftDataMerger(DataMerger):
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='left', left_on=left_on, right_on=right_on, **kwargs)


class RightDataMerger(DataMerger):
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='right', left_on=left_on, right_on=right_on, **kwargs)


class InnerDataMerger(DataMerger):
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='inner', left_on=left_on, right_on=right_on, **kwargs)


class OuterDataMerger(DataMerger):
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='outer', left_on=left_on, right_on=right_on, **kwargs)


class Merger(object):
    def __init__(self, data: DataFrame):
        self.data = data

    def merge(self, dataMerger: DataMerger, right: DataFrame, left_on, right_on, **kwargs):
        return Merger(dataMerger.merge(self.data, right, left_on=left_on, right_on=right_on, **kwargs))