import abc
from typing import  AnyStr

from pandas import DataFrame
from exceptionDefine import ColumnNotExistsException

class CompareOperator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def compare(self, data: DataFrame, col: AnyStr, value):
        pass

    @staticmethod
    def colExists(data: DataFrame, col: AnyStr) -> bool:
        """
        判断一个列在指定数据中是否存在
        :param data: 数据
        :param col: 列名
        :return: bool
        """
        return col in data.columns


class Equal(CompareOperator):
    """==运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if Equal.colExists(data, col):
            return data[col] == value
        raise ColumnNotExistsException(col)


class NotEqual(CompareOperator):
    """!=运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if NotEqual.colExists(data, col):
            return data[col] != value
        raise ColumnNotExistsException(col)


class GreaterThan(CompareOperator):
    """>=运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if GreaterThan.colExists(data, col):
            return data[col] > value
        raise ColumnNotExistsException(col)


class GreaterEqual(CompareOperator):
    """>运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if GreaterEqual.colExists(data, col):
            return data[col] >= value
        raise ColumnNotExistsException(col)


class LessThan(CompareOperator):
    """<运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if LessThan.colExists(data, col):
            return data[col] < value
        raise ColumnNotExistsException(col)


class LessEqual(CompareOperator):
    """<=运算符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if LessEqual.colExists(data, col):
            return data[col] <= value
        raise ColumnNotExistsException(col)


class StartsWith(CompareOperator):
    """以指定字符开头"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if StartsWith.colExists(data, col):
            return data[col].apply(lambda x: str(x).startswith(str(value)))
        raise ColumnNotExistsException(col)


class NotStartsWith(CompareOperator):
    """不以指定字符开头"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if NotStartsWith.colExists(data, col):
            return data[col].apply(lambda x: not str(x).startswith(str(value)))
        raise ColumnNotExistsException(col)


class EndsWith(CompareOperator):
    """以指定字符结尾"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if EndsWith.colExists(data, col):
            return data[col].apply(lambda x: str(x).endswith(str(value)))
        raise ColumnNotExistsException(col)


class NotEndsWith(CompareOperator):
    """不以指定字符结尾"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if NotEndsWith.colExists(data, col):
            return data[col].apply(lambda x: not str(x).endswith(str(value)))
        raise ColumnNotExistsException(col)


class Contains(CompareOperator):
    """包含指定字符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if Contains.colExists(data, col):
            return data[col].apply(lambda x: str(value) in str(x))
        raise ColumnNotExistsException(col)


class NotContains(CompareOperator):
    """不包含指定字符"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if NotContains.colExists(data, col):
            return data[col].apply(lambda x: str(value) not in str(x))
        raise ColumnNotExistsException(col)


class In(CompareOperator):
    """值在指定列表中=>等价于excel中的筛选的多选功能"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if In.colExists(data, col):
            return data[col].isin(value)
        raise ColumnNotExistsException(col)


class NotIn(CompareOperator):
    """值不在指定列表中=>等价于excel中的筛选的返选功能"""
    def compare(self, data: DataFrame, col: AnyStr, value):
        if NotIn.colExists(data, col):
            return ~ data[col].isin(value)
        raise ColumnNotExistsException(col)