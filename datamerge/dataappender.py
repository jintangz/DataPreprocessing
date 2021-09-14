
from pandas import DataFrame


class DataAppender:
    def append(self, up: DataFrame, down: DataFrame, ignore_index=False, **kwargs):
        return up.append(down, ignore_index=ignore_index, **kwargs)

