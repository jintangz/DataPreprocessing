import abc
from typing import AnyStr, List, Union

from pandas import DataFrame

from dataclean import DataCleaner


class OutlierRecognizer(metaclass=abc.ABCMeta):
    """异常值识别器"""
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
    """使用四分位距离进行异常值识别"""
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
    """使用3-sigma准则进行异常值识别"""
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
    """
    异常值处理器,支持分组进行异常值识别后删除
    """
    def __init__(self, by: Union[None, AnyStr, List[AnyStr]] = None):
        """
        初始化属性
        :param by: 指定进行分组的列名。默认为None不进行分组。如果传入的是列名则，按照传入的列进行分组删除异常值
        """
        super().__init__(by)

    @abc.abstractmethod
    def clean(self, *args, **kwargs):
        pass

class DropOutlierHandler(OutlierHandler):
    """异常值删除处理器"""
    def __init__(self, outlierRecognizer: OutlierRecognizer, by: Union[None, AnyStr, List[AnyStr]]  = None):
        """

        :param outlierRecognizer: 异常值识别器
        :param by: 指定进行分组的列名。默认为None不进行分组。如果传入的是列名则，按照传入的列进行分组删除异常值
        """
        super().__init__(by)
        self.outlierRecognizer = outlierRecognizer

    def clean(self, data: DataFrame, subset):
        """
        清除异常值
        :param data: 进行异常值删除操作的数据
        :param subset: 指定进行异常值判别的列，支持None:全部列；以及指定列
        :return:
        """
        if self.by is None:
            return self.outlierRecognizer.recognize(data, subset)
        return data.groupby(by = self.by).apply(self.outlierRecognizer.recognize, subset=subset).reset_index(drop=True)