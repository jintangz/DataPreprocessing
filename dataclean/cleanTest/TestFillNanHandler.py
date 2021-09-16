import unittest

from dataclean.nullHandler import ModeFillNullHandler, MeanFillNullHandler, MedianFillNullHandler, \
    ForwardFillNullHandler, InterpolateFillNullHandler
from dataclean.cleanTest import dataPath
import pandas as pd

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.data = pd.read_csv(dataPath, encoding='gbk')
        self.modeFill1 = ModeFillNullHandler()
        self.modeFill2 = ModeFillNullHandler(1, 'area')
        self.modeFill3 = ModeFillNullHandler(1, ['area', 'type'])

        self.meanFill1 = MeanFillNullHandler()
        self.meanFill2 = MeanFillNullHandler(1, 'area')
        self.meanFill3 = MeanFillNullHandler(1, ['area', 'type'])

        self.medianFill1 = MedianFillNullHandler()
        self.medianFill2 = MedianFillNullHandler(1, 'area')
        self.medianFill3 = MedianFillNullHandler(1, ['area', 'type'])

        self.fFill1 = ForwardFillNullHandler()
        self.fFill2 = ForwardFillNullHandler(1, 'area')
        self.fFill3 = ForwardFillNullHandler(1, ['area', 'type'])

        self.iFill1 = InterpolateFillNullHandler()
        self.iFill2 = InterpolateFillNullHandler(1, 'area')
        self.iFill3 = InterpolateFillNullHandler(1, ['area', 'type'])

    def test_modeFill1(self):
        print(self.modeFill1.clean(self.data))
        print("================" * 4)
        print(self.modeFill1.clean(self.data, 'age'))

    def test_modeFill2(self):
        # print(self.modeFill2.clean(self.data))
        # print("================" * 4)
        print(self.modeFill2.clean(self.data, ['age', 'num']))

    def test_modeFill3(self):
        print(self.modeFill3.clean(self.data))
        # print("================" * 4)
        # print(self.modeFill3.clean(self.data, ['age', 'hsr']))

    def test_meanFill1(self):
        print(self.meanFill1.clean(self.data))
        print("================" * 4)
        print(self.meanFill1.clean(self.data, 'age'))

    def test_meanFill2(self):
        print(self.meanFill2.clean(self.data))
        print("================" * 4)
        print(self.meanFill2.clean(self.data, 'age'))

    def test_meanFill3(self):
        print(self.meanFill3.clean(self.data))
        print("================" * 4)
        print(self.meanFill3.clean(self.data, ['age', 'hsr']))

    def test_median1(self):
        print(self.medianFill1.clean(self.data))
        print("================" * 4)
        print(self.medianFill1.clean(self.data, 'age'))

    def test_median2(self):

        # print(self.medianFill2.clean(self.data))
        # print("================" * 4)
        print(self.medianFill2.clean(self.data, 'age'))

    def test_median3(self):
        # print(self.medianFill3.clean(self.data))
        # print("================" * 4)
        print(self.medianFill3.clean(self.data, 'age'))

    def test_fFill1(self):
        # print(self.fFill1.clean(self.data))
        # print("================" * 4)
        print(self.fFill1.clean(self.data, 'age'))

    def test_fFill2(self):
        print(self.fFill2.clean(self.data))
        print("================" * 4)
        print(self.fFill2.clean(self.data, 'age'))

    def test_fFill3(self):
        # print(self.fFill3.clean(self.data))
        print("================" * 4)
        print(self.fFill3.clean(self.data, 'age'))

    def test_iFill1(self):
        print(self.iFill1.clean(self.data))
        print("================" * 4)
        print(self.iFill1.clean(self.data, 'age'))

    def test_iFill2(self):
        # print(self.iFill2.clean(self.data))
        print("================" * 4)
        print(self.iFill2.clean(self.data, 'age'))

    def test_iFill3(self):
        # print(self.iFill3.clean(self.data))
        print("================" * 4)
        print(self.iFill3.clean(self.data, ['age', 'hsr']))

if __name__ == '__main__':
    unittest.main()
