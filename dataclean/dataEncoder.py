import abc

from pandas import DataFrame
import pandas as pd

class DataEncoder(metaclass=abc.ABCMeta):
    def encode(self, data: DataFrame, col: str):
        pass


class LabelEncoder(DataEncoder):
    def encode(self, data: DataFrame, col: str):
        codeMap = {val: i + 1 for i, val in enumerate(list(data[col].unique()))}
        return data[col].map(codeMap)

class DummyEncoder(DataEncoder):
    def encode(self, data: DataFrame, col: str):
        return pd.get_dummies(data[col], col)