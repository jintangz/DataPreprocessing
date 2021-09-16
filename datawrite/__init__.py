import abc
import pandas as pd

class DataWriter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def write(self, data: pd.DataFrame, savePath: str):
        pass

class CsvDataWriter(DataWriter):

    def write(self, data: pd.DataFrame, savePath: str):
        data.to_csv(savePath, index=False)

class ExcelDataWriter(DataWriter):

    def write(self, data: pd.DataFrame, savePath: str):
        data.to_excel(savePath, index=False)