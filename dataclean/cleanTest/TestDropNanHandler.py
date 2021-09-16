import unittest
import pandas as pd

from dataclean.cleanTest import dataPath
from dataclean.nullHandler import RowDropNullHandler, ColumnDropNullHandler

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.data = pd.read_csv(dataPath, encoding='gbk')
        self.rowHandler1 = RowDropNullHandler()
        self.colHandler1 = ColumnDropNullHandler()

        self.rowHandler2 = RowDropNullHandler(2)
        self.colHandler2 = ColumnDropNullHandler(5)

        self.rowHandler3 = RowDropNullHandler(0.4)
        self.colHandler3 = ColumnDropNullHandler(0.2)

        self.rowHandler4 = RowDropNullHandler(1, 'area')

        self.rowHandler5 = RowDropNullHandler(1, ['area', 'year'])

    def test_Row1(self):
        print(self.rowHandler1.clean(self.data))
        print("==================" * 6)
        print(self.rowHandler1.clean(self.data, ['type', 'age']))

    def test_Col1(self):
        print(self.colHandler1.clean(self.data))

    def test_row2(self):
        print(self.rowHandler2.clean(self.data))
        print("==================" * 6)
        print(self.rowHandler2.clean(self.data, ['type', 'age']))

    def test_col2(self):
        print(self.colHandler2.clean(self.data))

    def test_row3(self):
        print(self.rowHandler3.clean(self.data))
        print("==================" * 6)
        print(self.rowHandler3.clean(self.data, ['type', 'age']))

    def test_col3(self):
        print(self.colHandler3.clean(self.data))

    def test_row4(self):
        print(self.rowHandler4.clean(self.data))
        print("==================" * 6)
        print(self.rowHandler4.clean(self.data, ['type', 'age']))

    def test_row5(self):
        print(self.rowHandler5.clean(self.data))
        print("==================" * 6)
        print(self.rowHandler5.clean(self.data, ['type', 'age']))


if __name__ == '__main__':
    unittest.main()
