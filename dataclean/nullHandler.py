import abc
from typing import Union, AnyStr, List
from pandas import DataFrame

from dataclean import DataCleaner

from exceptionDefine import FillColumnNotExistsException, KeyUsedGroupNotExistsException


class NullHandler(DataCleaner):
    """空值处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(by)
        self.limit = limit

    @abc.abstractmethod
    def clean(self, *args, **kwargs):
        pass


class FillNullHandler(NullHandler):
    """空值填充处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        """

        :param limit: 缺失值填充的最大数量
        :param by: 进行分组的列。支持分组进行缺失值填充.默认为None不进行分组 。
        """
        super().__init__(limit, by)

    @abc.abstractmethod
    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        pass

    def __getCol(self, data, col):
        if isinstance(col, str):
            return [col]
        elif col is None:
            return data.columns
        else:
            return col

    def clean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None] = None, *args, **kwargs):
        df = data.copy()
        if col is not None:
            if not NullHandler.testColsExists(df, col):
                raise FillColumnNotExistsException
        cols = self.__getCol(df, col)
        if self.by is None:
            return self.auxClean(df, cols)
        else:
            if not NullHandler.testColsExists(df, self.by):
                raise KeyUsedGroupNotExistsException
            return df.groupby(by=self.by).apply(self.auxClean, col=cols).reset_index(drop=True)


class ModeFillNullHandler(FillNullHandler):
    """众数填充空值处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        if data[col].mode().shape[0] > 0:
            data[col] = data[col].fillna(data[col].mode().loc[0, :], limit=self.limit)
        return data



class MedianFillNullHandler(FillNullHandler):
    """中位数填充空值处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        data[col] = data[col].fillna(data[col].median(), limit=self.limit)
        return data


class MeanFillNullHandler(FillNullHandler):
    """均值填充处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        data[col] = data[col].fillna(data[col].mean(), limit=self.limit)
        return data

class ForwardFillNullHandler(FillNullHandler):
    """前项填充空值处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        if self.by is not None:
            df = data.sort_values(by=self.by)
        else: df = data
        df[col] = df[col].ffill(limit=self.limit)
        return df



class InterpolateFillNullHandler(FillNullHandler):
    """插值填充空值处理器"""
    def __init__(self, limit=None, by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    def auxClean(self, data: DataFrame, col: Union[AnyStr, List[AnyStr], None], *args, **kwargs):
        if self.by is not None:
            df = data.sort_values(by=self.by)
        else: df = data
        df[col] = df[col].interpolate(limit=self.limit, limit_area='inside')
        return df


class DropNullHandler(NullHandler):
    """空值删除处理器"""
    def __init__(self, limit: Union[int, float, None] = None,
                 by: Union[None, AnyStr, List[AnyStr]] = None):
        super().__init__(limit, by)

    @abc.abstractmethod
    def clean(self, *args, **kwargs):
        pass
    @staticmethod
    def getCols(data: DataFrame, subset):
        if subset is None:
            return data.columns
        elif isinstance(subset, str):
            return [subset]
        else:
            return subset

    def auxClean(self, data: DataFrame, axis, subset = None):
        cols = DropNullHandler.getCols(data, subset)
        if isinstance(self.limit, float):
            thresh = data[cols].shape[1- axis] - int(self.limit * data[cols].shape[1 - axis])
        else:
            limit = self.limit if self.limit is not None else 0
            thresh = data[cols].shape[1- axis] - limit
        if axis == 0:
            return data.dropna(axis=axis, subset=subset, thresh=thresh)
        else:
            return data.loc[:, data[cols].dropna(axis=axis, thresh=thresh).columns]


class RowDropNullHandler(DropNullHandler):
    """按行删除空值处理器"""
    def __init__(self, limit=None, by: Union[AnyStr, List[AnyStr], None] = None):
        """

        :param limit: 容忍某行的缺失值最大数量。支持int, float, None; None值为不能包含任意缺失值。float表示最大缺失值比率.
        :param by: 进行分组删除的列。如果该组数据超过容忍上限，则会把这组数据全部删除
        """
        super().__init__(limit, by)

    def clean(self, data: DataFrame, subset: Union[None, AnyStr, List[AnyStr]] = None):
        if self.by is None:
            return self.auxClean(data, 0, subset)
        else:
            return data.groupby(by=self.by).apply(self.__groupClean, subset=subset).reset_index(drop=True)

    def __groupClean(self, data: DataFrame, subset):
        cols = DropNullHandler.getCols(data, subset)
        if isinstance(self.limit, float):
            thresh = int(self.limit * data.shape[0])
        else:
            thresh = self.limit if self.limit is not None else data.shape[0]
        if data[cols].isna().sum().min() < thresh:
            return data
        else: return DataFrame()


class ColumnDropNullHandler(DropNullHandler):
    """
    按列删除空值处理器, 如果某列的缺失值数量超过指定值，那么就删除这一列
    """
    def __init__(self, limit=None):
        """

        :param limit: 容忍某列的缺失值最大数量。支持int, float, None; None值为不能包含任意缺失值。float表示最大缺失值比率.
        """
        super().__init__(limit, None)

    def clean(self, data: DataFrame):
        return self.auxClean(data, 1, None)