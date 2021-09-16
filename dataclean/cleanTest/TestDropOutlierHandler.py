import unittest

import pandas as pd

from dataclean.cleanTest import dataPath
from dataclean.outlierHandler import DropOutlierHandler, ThreeSigmaOutlierRecoginzer, FourQuantileGapOutlierRecognizer

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(dataPath, encoding='gbk')
        self.sigma = ThreeSigmaOutlierRecoginzer()
        self.four = FourQuantileGapOutlierRecognizer()
        self.handler1 = DropOutlierHandler(self.sigma)
        self.handler2 = DropOutlierHandler(self.four)

        self.handler3 = DropOutlierHandler(self.sigma, by = 'area')
        self.handler4 = DropOutlierHandler(self.four, by = 'area')

        self.handler5 = DropOutlierHandler(self.sigma, by='year')
        self.handler6 = DropOutlierHandler(self.sigma, by='year')

        self.handler7 = DropOutlierHandler(self.sigma, by = ['year', 'type'])
        self.handler8 = DropOutlierHandler(self.sigma, by=['year', 'type'])

    def test_sigmaByNone(self):
        print(self.handler1.clean(self.data, ['year', 'age']))

    def test_fourByNone(self):
        print(self.handler2.clean(self.data, ['year', 'age']))

    def test_sigmaByStrCol(self):
        print(self.handler3.clean(self.data, ['year', 'age']))

    def test_fourByStrCol(self):
        print(self.handler4.clean(self.data, ['year', 'age']))

    def test_sigmaByNumCol(self):
        print(self.handler5.clean(self.data, ['year', 'age']))

    def test_fourByNumCol(self):
        print(self.handler6.clean(self.data, ['year', 'age']))

    def test_sigmaByCols(self):
        print(self.handler7.clean(self.data, ['year', 'num']))

    def test_fourByCols(self):
        print(self.handler8.clean(self.data, ['year', 'num']))

if __name__ == '__main__':
    unittest.main()
