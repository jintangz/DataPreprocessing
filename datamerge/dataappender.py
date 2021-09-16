
from pandas import DataFrame


class DataAppender:
    """实现数据进行纵向连接的类，连接方式是按照列名进行连接的"""
    def append(self, up: DataFrame, down: DataFrame, ignore_index=False, **kwargs):
        return up.append(down, ignore_index=ignore_index, **kwargs)