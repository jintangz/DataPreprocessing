class CsvFileTypeException(Exception):
    def __str__(self):
        return "请选择以.csv结尾的文件!"


class ExcelFileTypeException(Exception):
    def __str__(self):
        return "请选择以.xls或.xlsx结尾的excel文件！"


class ColumnNotExistsException(Exception):
    def __init__(self, col):
        self.col = col

    def __str__(self):
        return f"选择进行过滤的列{self.col}在数据中不存在!"
