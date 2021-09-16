import unittest

import pandas as pd

from dataclean.cleanTest import dataPath
from dataclean.dataEncoder import LabelEncoder, DummyEncoder

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.labelEncoder = LabelEncoder()
        self.dummyEncoder = DummyEncoder()
        self.data = pd.read_csv(dataPath, encoding='gbk')

    def testLabelEncoder(self):
        print(self.labelEncoder.encode(self.data, 'area'))

    def testDummyEncoder(self):
        print(self.dummyEncoder.encode(self.data, 'area'))

if __name__ == '__main__':
    unittest.main()
