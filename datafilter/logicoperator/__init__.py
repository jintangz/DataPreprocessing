import abc
from typing import Tuple, AnyStr, Any
from pandas import DataFrame
from datafilter.compareoperator import CompareOperator


class LogicOperator(metaclass=abc.ABCMeta):
    """逻辑运算符接口"""
    @abc.abstractmethod
    def operate(self, *args):
        pass


class TwoPartLogicOperator(LogicOperator):
    """二元逻辑运算符接口"""
    def __init__(self, left: CompareOperator, right: CompareOperator):
        self.left = left
        self.right = right

    @abc.abstractmethod
    def operate(self, t1: Tuple[DataFrame, AnyStr, Any], t2: Tuple[DataFrame, AnyStr, Any]):
        pass


class OnePartLogicOperator(LogicOperator):
    """一元逻辑运算符接口"""
    def __init__(self, compareOprator: CompareOperator):
        self.compareOprator = compareOprator

    @abc.abstractmethod
    def operate(self, t: Tuple[DataFrame, AnyStr, Any]):
        pass


class Not(OnePartLogicOperator):
    """取反运算符"""
    def __init__(self, compareOprator: CompareOperator):
        super().__init__(compareOprator)

    def operate(self, t: Tuple[DataFrame, AnyStr, Any]):
        return ~ self.compareOprator.compare(t[0], t[1], t[2])

class OnePartLogicOperatorWrapper(OnePartLogicOperator):
    """对单个比较运算符进行的兼容的一元运算符包装器"""
    def __init__(self, compareOprator: CompareOperator):
        super().__init__(compareOprator)

    def operate(self, t: Tuple[DataFrame, AnyStr, Any]):
        return self.compareOprator.compare(t[0], t[1], t[2])


class And(TwoPartLogicOperator):
    """逻辑与运算符"""
    def __init__(self, left: CompareOperator, right: CompareOperator):
        super().__init__(left, right)

    def operate(self, t1: Tuple[DataFrame, AnyStr, Any], t2: Tuple[DataFrame, AnyStr, Any]):
        return self.left.compare(t1[0], t1[1], t1[2]) & self.right.compare(t2[0], t2[1], t2[2])


class Or(TwoPartLogicOperator):
    """逻辑或运算符"""
    def __init__(self, left: CompareOperator, right: CompareOperator):
        super().__init__(left, right)

    def operate(self, t1: Tuple[DataFrame, AnyStr, Any], t2: Tuple[DataFrame, AnyStr, Any]):
        return self.left.compare(t1[0], t1[1], t1[2]) | self.right.compare(t2[0], t2[1], t2[2])