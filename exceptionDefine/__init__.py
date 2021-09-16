class CsvFileTypeException(Exception):
    def __str__(self):
        return "请选择以.csv结尾的文件!"


class ExcelFileTypeException(Exception):
    def __str__(self):
        return "请选择以.xls或.xlsx结尾的excel文件！"


class FilterColumnNotExistsException(Exception):
    def __init__(self, col):
        self.col = col

    def __str__(self):
        return f"选择进行过滤的列{self.col}在数据中不存在!"

class NoDefaultColumnToMerge(Exception):
    def __str__(self):
        return "未找到默认的可以进行表连接的列，请具体指定"

class FillColumnNotExistsException(Exception):
    def __str__(self):
        return "指定的进行缺失值填充的列不存在!"


class KeyUsedGroupNotExistsException(Exception):
    def __str__(self):
        return "指定的用于分组的列不存在!"