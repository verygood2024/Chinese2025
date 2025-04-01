class DictToList:
    def __init__(self, file_dict, path=None):
        """
        初始化 File 类的实例。

        参数:
        - file_dict (dict): 存储文件数据的字典。
        - path (str): 文件路径，用于保存或加载文件，默认为 None。
        """
        self.file_dict = file_dict
        self.path = path
        self.index_map = {i: key for i, key in enumerate(file_dict.keys())}

    def __getitem__(self, index):
        """
        重载 [] 操作符，用于根据索引号获取字典的值。

        参数:
        - index (int): 索引号。

        返回:
        - 对应索引号的字典值。

        异常:
        - IndexError: 当索引超出范围时抛出。
        """
        key = self.index_map.get(index)
        if key is not None:
            return self.file_dict.get(key)
        raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        """
        重载 [] 操作符，用于根据索引号设置字典的值。

        参数:
        - index (int): 索引号。
        - value: 要设置的新值。

        异常:
        - IndexError: 当索引超出范围时抛出。
        """
        key = self.index_map.get(index)
        if key is not None:
            self.file_dict[key] = value
        else:
            raise IndexError("Index out of range")