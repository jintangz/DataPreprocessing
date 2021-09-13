import abc
import pandas as pd
from typing import AnyStr, Tuple, Any


# 列过滤时候的方式
EXACTMATCH = '精确匹配'
FUZZYMATCH = '模糊匹配'
TYPEMATCH = '类型匹配'
columnDataFilterWays = (EXACTMATCH, FUZZYMATCH, TYPEMATCH)