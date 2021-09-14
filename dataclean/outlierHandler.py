import abc
from typing import AnyStr, List, Union

from pandas import DataFrame

from dataclean import DataCleaner


class OutlierRecognizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def recognize(self, data, subset):
        pass

    @staticmethod
    def getCols(data, subset):
        if subset is None:
            cols = data.columns
        elif isinstance(subset, str):
            cols = [subset]
        else:
            cols = subset
        return cols


class FourQuantileGapOutlierRecognizer(OutlierRecognizer):
    def recognize(self, data: DataFrame, subset):
        df = data.copy()
        cols = OutlierRecognizer.getCols(data, subset)
        downFourQuantile = data[cols].quantile(0.25)
        upFourQuantile = data[cols].quantile(0.75)
        gap = upFourQuantile - downFourQuantile
        cols = list(gap.index)
        downLimit = downFourQuantile - 1.5 * gap
        upLimit = upFourQuantile + 1.5 * gap
        for col in cols:
            df = df.loc[(df[col] >= downLimit[col]) & (df[col] <= upLimit[col]) | (df[col].isna()), :]
        return df

class ThreeSigmaOutlierRecoginzer(OutlierRecognizer):
    def recognize(self, data, subset):
        df = data.copy()
        cols = OutlierRecognizer.getCols(data, subset)
        sigma = data[cols].std()
        avg = data[cols].mean()
        upLimit = avg + 3 * sigma
        downLimit = avg - 3 * sigma
        cols = upLimit.index
        for col in cols:
            df = df.loc[(df[col] >= downLimit[col]) & (df[col] <= upLimit[col]) | (df[col].isna()), :]
        return df


class OutlierHandler(DataCleaner):
    def __init__(self, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(by)

    @abc.abstractmethod
    def clean(self, *args, **kwargs):
        pass

class DropOutlierHandler(OutlierHandler):
    def __init__(self, outlierRecognizer: OutlierRecognizer, by: Union[None, AnyStr, List[AnyStr]]  = None):
        super().__init__(by)
        self.outlierRecognizer = outlierRecognizer

    def clean(self, data: DataFrame, subset):
        if self.by is None:
            return self.outlierRecognizer.recognize(data, subset)
        return data.groupby(by = self.by).apply(self.outlierRecognizer.recognize, subset=subset).reset_index(drop=True)