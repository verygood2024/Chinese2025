import sys
import warnings

from .Error import 输入不合法
from .查询 import 查询


class 繁體方言搜索:
    def __init__(self,序号):
        # 检查输入是否为字符串类型
        if not isinstance(序号, str):
            raise 输入不合法(序号, 提示="输入类型应为字符串形式的数字,例如'027'或'284'.")

        # 检查字符串是否全为数字
        if not 序号.isdigit():
            raise 输入不合法(序号, 提示="输入必须是全数字的字符串,例如'027'或'284'.")

        # 新增规则：四位数及以上不允许前导零,三位数允许前导零
        if len(序号) != 3 and 序号.startswith("0"):
            raise 输入不合法(序号, 提示="三位数允许前导零（如'027'）,但四位数及以上需直接输入数字如'284'.")

        # 转换为整数并验证范围
        code_int = int(序号)
        if not (27 <= code_int <= 434):
            raise 输入不合法(序号,提示="您不能输入区间[27,434]以外字符串数字.")

        self.表名 = 查询.查找表名(序号)

    def 返回調值(self, 字头):
        return list({item[0] for item in 查询.单列查询(self.表名, "調值", "字", 字头)})

    def 返回調類(self, 字头):
        return list({item[0] for item in 查询.单列查询(self.表名, "調類", "字", 字头)})

    def 返回發音(self, 字头):
        return [a + b for a, b in zip(list({item[0] for item in 查询.单列查询(self.表名, "聲母", "字", 字头)}),
                                      list({item[0] for item in 查询.单列查询(self.表名, "韻母", "字", 字头)}))]

    def 返回聲母(self, 字头):
        return list({item[0] for item in 查询.单列查询(self.表名, "聲母", "字", 字头)})

    def 返回韻母(self, 字头):
        return list({item[0] for item in 查询.单列查询(self.表名, "韻母", "字", 字头)})

    def 返回(self,类别,字头):
        func_map = {
            "調值": lambda: self.返回調值(字头),
            "調類": lambda: self.返回調類(字头),
            "發音": lambda: self.返回發音(字头),
            "聲母": lambda: self.返回聲母(字头),
            "韻母": lambda: self.返回韻母(字头),
        }

        func = func_map.get(类别)
        if func:
            return func()
        else:
            warnings.warn("没有此类别", SyntaxWarning)
            sys.exit()
