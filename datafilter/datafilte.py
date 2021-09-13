import abc
import re
from typing import AnyStr, Tuple, Any

from pandas import DataFrame, Series

from datafilter import TYPEMATCH, EXACTMATCH, FUZZYMATCH
from datafilter.logicoperator import LogicOperator, OnePartLogicOperator, TwoPartLogicOperator


class DataFilter(metaclass=abc.ABCMeta):
    """数据过滤器接口"""
    @abc.abstractmethod
    def filter(self, *args, **kwargs):
        pass


class ColumnDataFilter(DataFilter):
    """列过滤器"""
    __slots__ = ['__matchType']

    def __init__(self, matchType: AnyStr = EXACTMATCH):
        """

        :param matchType: 匹配方式，默认为精确匹配。支持精确匹配,模糊匹配以及类型匹配
        """
        self.__matchType = matchType

    def filter(self, data: DataFrame, filterCols: Tuple[AnyStr]):
        if self.__matchType == EXACTMATCH:
            # 精确匹配
            existsCols = list(filter(lambda x: x in data.columns, filterCols))
            return data[existsCols]
        elif self.__matchType == TYPEMATCH:
            # 类型匹配
            types = data.dtypes
            return data[ColumnDataFilter.__isTypeMatch(types, filterCols)]
        elif self.__matchType == FUZZYMATCH:
            # 模糊匹配，支持正则表达式
            cols = list(filter(lambda x: ColumnDataFilter.__isFuzzyMatch(x, filterCols), data.columns))
            return data[cols]
        else:
            raise Exception(f"列筛选方式仅支持{EXACTMATCH}、{TYPEMATCH}、{FUZZYMATCH}!")

    @staticmethod
    def __isFuzzyMatch(col, fuzzyStrs):
        """判断列名是否可以和正则表达式匹配"""
        for fuzzyStr in fuzzyStrs:
            if re.match(fuzzyStr, col) is not None:
                return True
        return False

    @staticmethod
    def __isTypeMatch(types: Series, filterTypes: Tuple[AnyStr]):
        """判断列数据类型是否和指定数据类型匹配"""
        filterTypes = tuple(map(lambda x: x if x != 'string' else 'object', filterTypes))
        return types.loc[types.map(lambda x: x.name.startswith(filterTypes))].index.tolist()


class RowDataFilter(DataFilter):
    """行过滤器"""
    def filter(self, logicOperator: LogicOperator, t1: Tuple[DataFrame, AnyStr, Any] = None, t2: Tuple[DataFrame, AnyStr, Any] = None):
        """
        进行行过滤的方法
        :param logicOperator: 逻辑运算符,支持二元和一元逻辑运算符
        :param t1: 使用logicOperator的第一个比较运算符进行比较所需要的数据. 第一个元素是数据，第二个元素是列名，第三个元素是进行比较的值
        :param t2:使用logicOperator(如果是二元逻辑运算符)的第二个比较运算符进行比较所需要的数据. 第一个元素是数据，第二个元素是列名，第三个元素是进行比较的值
        :return:
        """
        if isinstance(logicOperator, OnePartLogicOperator):
            return t1[0].loc[logicOperator.operate(t1), :]
        return t1[0].loc[logicOperator.operate(t1, t2), :]
