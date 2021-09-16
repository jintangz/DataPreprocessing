import abc
from typing import Union, AnyStr, List

from pandas import DataFrame
from exceptionDefine import NoDefaultColumnToMerge


class DataMerger(metaclass=abc.ABCMeta):
    """
    数据进行行连接的抽象类
    """
    @abc.abstractmethod
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        pass

    def __hasSameCol(self, left: DataFrame, right: DataFrame):
        """判断进行连接的两个数据集是否具有相同列名的列"""
        return len(set(left.columns).intersection(right.columns)) > 0

    def auxMerge(self, left: DataFrame, right: DataFrame, how: str = 'left', left_on=None, right_on=None, **kwargs):
        """进行数据集连接的方法"""
        if left_on == None:
            if self.__hasSameCol(left, right):
                return left.merge(right)
            raise NoDefaultColumnToMerge
        return left.merge(right, how=how, left_on=left_on, right_on=right_on, **kwargs)


class LeftDataMerger(DataMerger):
    """实现数据集左连接的类"""
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='left', left_on=left_on, right_on=right_on, **kwargs)


class RightDataMerger(DataMerger):
    """实现数据集右连接的类"""
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='right', left_on=left_on, right_on=right_on, **kwargs)


class InnerDataMerger(DataMerger):
    """实现数据集内连接的类"""
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='inner', left_on=left_on, right_on=right_on, **kwargs)


class OuterDataMerger(DataMerger):
    """实现数据集外连接的类"""
    def merge(self, left: DataFrame, right: DataFrame, left_on: Union[None, AnyStr, List[AnyStr]] = None,
              right_on: Union[None, AnyStr, List[AnyStr]] = None, **kwargs):
        return self.auxMerge(left=left, right=right, how='outer', left_on=left_on, right_on=right_on, **kwargs)


class Merger(object):
    """实现数据集进行链式连接的包装类"""
    def __init__(self, data: DataFrame):
        self.data = data

    def merge(self, dataMerger: DataMerger, right: DataFrame, left_on, right_on, **kwargs):
        return Merger(dataMerger.merge(self.data, right, left_on=left_on, right_on=right_on, **kwargs))