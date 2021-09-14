import unittest
import pandas as pd
from datamerge.datamerger import *
from datamerge.dataappender import DataAppender
from exceptionDefine import NoDefaultColumnToMerge

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.df1 = pd.DataFrame({'year': [2008, 2006, 2010], 'age': [18, 25, 23]})
        self.df2 = pd.DataFrame({'time': [2007, 2008, 2006], 'height':[170, 171, 72.5], 'weight':[55, 66, 77]})
        self.df3 = pd.DataFrame({'time': [2007, 2008, 2006], 'height':[170, 171, 72.5], 'weight':[55, 66, 77], 'age':[1,2, 3]})
        self.leftMerger = LeftDataMerger()
        self.rightMerger = RightDataMerger()
        self.outMerger = OuterDataMerger()
        self.innerMerger = InnerDataMerger()
        self.dataAppend = DataAppender()

    def test_leftMerger(self):
        with self.assertRaises(NoDefaultColumnToMerge):
            self.leftMerger.merge(self.df1, self.df2)
        print("==========================" * 4)
        print(self.leftMerger.merge(self.df1, self.df2, left_on='year', right_on='time'))
        print('==========================' * 4)

    def test_rightMerger(self):
        with self.assertRaises(NoDefaultColumnToMerge):
            self.rightMerger.merge(self.df1, self.df2)
        print("==========================" * 4)
        print(self.rightMerger.merge(self.df1, self.df2, left_on='year', right_on='time'))
        print("==========================" * 4)

    def test_outMerger(self):
        with self.assertRaises(NoDefaultColumnToMerge):
            self.outMerger.merge(self.df1, self.df2)
        print("==========================" * 4)
        print(self.outMerger.merge(self.df1, self.df2, left_on='year', right_on='time'))
        print("==========================" * 4)

    def test_innerMerger(self):
        with self.assertRaises(NoDefaultColumnToMerge):
            self.innerMerger.merge(self.df1, self.df2)
        print("==========================" * 4)
        print(self.innerMerger.merge(self.df1, self.df2, left_on='year', right_on='time'))
        print("==========================" * 4)

    def test_appender(self):
        print(self.dataAppend.append(self.df1, self.df3))
        print("+++++++++++++++++++++++++++" * 4)
        print(self.dataAppend.append(self.df1, self.df3, ignore_index=True))

if __name__ == '__main__':
    unittest.main()
