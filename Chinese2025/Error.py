import pprint


class 输入不合法(ValueError):
    def __init__(self, 不合法的输入, 合法输入示例=None,提示=None):
        self.输入不合法 = 合法输入示例
        self.输入不合法__ = 不合法的输入
        if 提示 is not None:
            message = (
                f"{self.输入不合法__}\n合法输入提示:{提示}"
            )
        else:
            message = (
                f"{self.输入不合法__}\n合法输入示例:{self.输入不合法}"
            )
        super().__init__(message)