import unittest

from dataload.reader import CsvDataReader, ExcelDataReader

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.csvReader = CsvDataReader()
        self.excelReader = ExcelDataReader()

    def testCsvRead(self):
        print(self.csvReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)\test.txt'))
        print(self.csvReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)\data.csv'))
        print(self.csvReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)'))

    def testExcelReader(self):
        print(self.excelReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)\test.txt'))
        print(self.excelReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)\test.xlsx'))
        print(self.excelReader.read(r'C:\Users\acer-pc\Desktop\新建文件夹 (4)'))


if __name__ == '__main__':
    unittest.main()