import unittest
import pandas as pd
from datafilter.datafilte import ColumnDataFilter, RowDataFilter
from datafilter import *
from datafilter.compareoperator import *
from datafilter.logicoperator import *

class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)\data.csv')
        self.exactColFilter = ColumnDataFilter(EXACTMATCH)
        self.fuzzyColFilter = ColumnDataFilter(FUZZYMATCH)
        self.typeColFilter = ColumnDataFilter(TYPEMATCH)
        self.badColFilter = ColumnDataFilter("测试")
        self.t1 = (self.data, 'year', 2008)
        self.t2 = (self.data, 'yea', 2009)
        self.rowFilter = RowDataFilter()
        self.leftComparator = GreaterEqual()
        self.rightComparator = LessThan()
        self.andOp = And(self.leftComparator, self.rightComparator)
        self.orOp = Or(self.leftComparator, self.rightComparator)
        self.notOp = Not(self.leftComparator)
        self.wrapper = OnePartLogicOperatorWrapper(self.leftComparator)

    def testColExactMatch(self):
        print("exact", self.exactColFilter.filter(self.data, ("lele", "year", "age")))

    def testColFuzzyMatch(self):
        print("fuzzy", self.fuzzyColFilter.filter(self.data, ("y.*",)))

    def testColTypeMatch(self):
        print("type", self.typeColFilter.filter(self.data, ('int', 'string', 'll')))

    def testColBadMatch(self):
        print("bad", self.badColFilter.filter(self.data, ("ll")))

    def testRowFilter(self):
        print(self.rowFilter.filter(self.andOp, self.t1, self.t2)['year'].unique())
        print("=======================" * 4)
        print(self.rowFilter.filter(self.orOp, self.t1, self.t2)['year'].unique())
        print("=======================" * 4)
        print(self.rowFilter.filter(self.notOp, self.t1, self.t2)['year'].unique())
        print("=======================" * 4)
        print(self.rowFilter.filter(self.wrapper, self.t2)['year'].unique())


if __name__ == '__main__':
    unittest.main()
