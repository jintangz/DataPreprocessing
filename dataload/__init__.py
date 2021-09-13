import os
from typing import Union, AnyStr, Tuple


#csv文件的后缀名
CSVENDS = ('.csv')
#excel文件的后缀名
EXCELENDS = ('.xls', '.xlsx')

def readData(path: str, ends: Union[AnyStr, Tuple[AnyStr]], func: callable, **kwargs):
    """
    读取一个目录下,以指定字符结尾的文件
    :param path: 目录的路径
    :param ends: 文件的结尾字符,用来判断文件的格式
    :param func: 传入的用来读取指定格式的文件的方法
    :param kwargs:
    :return: 返回一个字典,key值为每个对应格式的文件名, value值为读取对应文件的DataFrame
    """
    if os.path.isfile(path):
        raise Exception("请选择目录名!")
    if os.path.isdir(path):
        files = os.listdir(path)
        paths = list(map(lambda x: os.path.join(path, x), files))
        return {file: func(paths[index], **kwargs) for index, file in enumerate(files) if file.endswith(ends)}