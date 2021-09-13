import os
import abc

from typing import AnyStr, Union, Mapping

import pandas as pd

from dataload import readData, CSVENDS, EXCELENDS
from exceptionDefine import CsvFileTypeException, ExcelFileTypeException

class DataReader(metaclass=abc.ABCMeta):
    """
    数据读取器
    """
    def __init__(self, header, index_col, usecols, skiprows):
        """
        初始化DataReader的共有属性
        """
        self.header = header
        self.index_col = index_col
        self.usecols = usecols
        self.skiprows = skiprows

    @abc.abstractmethod
    def read(self, *args, **kwargs):
        pass


class CsvDataReader(DataReader):
    """csv文件读取器"""
    def __init__(self, sep=',', delimiter=None, header='infer', index_col=None, usecols=None, skiprows=None, **kwargs):
        super().__init__(header, index_col, usecols, skiprows)
        self.sep = sep
        self.delimiter = delimiter
        self.kwargs = kwargs

    def read(self, path: AnyStr) -> Union[pd.DataFrame, Mapping[AnyStr, pd.DataFrame]]:
        """
        读取csv文件的方法
        :param path: 路径名；可以是一个具体文件的路径还可以是一个目录路径
        :return:
        """
        if os.path.isfile(path):
            # 如果传入的path是一个文件，并且以.csv结尾，对csv文件进行读取；否则抛出csv文件类型异常
            if not path.endswith(CSVENDS):
                raise CsvFileTypeException
            return self.__read(path)
        # 如果传入一个目录，调用辅助方法readData，读取目录中所有的csv文件
        return readData(path, CSVENDS, self.__read)

    def __read(self, path):
        #读取一个具体的csv文件
        return pd.read_csv(path, sep=self.sep, delimiter=self.delimiter, header=self.header,
                           index_col=self.index_col, usecols=self.usecols, skiprows=self.skiprows, **self.kwargs)


class ExcelDataReader(DataReader):
    """Excel文件读取器"""
    def __init__(self, header=0, index_col=None, usecols=None, skiprows=None, **kwargs):
        super().__init__(header, index_col, usecols, skiprows)
        self.kwargs = kwargs

    def read(self, path: AnyStr, sheet_name: int = 0) -> Union[pd.DataFrame, Mapping[AnyStr, pd.DataFrame]]:
        """
              读取Excel文件的方法
              :param path: 路径名；可以是一个具体文件的路径还可以是一个目录路径
              :return:
        """
        if os.path.isfile(path):
            # 如果传入的path是一个文件，并且以.xls或。xlsx结尾，对excel文件进行读取；否则抛出excel文件类型异常
            if not path.endswith(EXCELENDS):
                raise ExcelFileTypeException
            return self.__read(path, sheet_name)
        return readData(path, EXCELENDS, self.__read, sheet_name=sheet_name)

    def __read(self, path, sheet_name):
        """读取一个具体的excel文件的一个子表"""
        return pd.read_excel(path, sheet_name=sheet_name, header=self.header, index_col=self.index_col,
                             usecols=self.usecols, skiprows=self.skiprows, **self.kwargs)
