import sys
import warnings

from .查询 import 查询


class 繁體方言搜索:
    def __init__(self,序号):
        try:
            code_int = int(序号)
            if code_int < 27:
                warnings.warn(f"您不能输入小于027的数字", SyntaxWarning)
                sys.exit()
        except ValueError:
            warnings.warn(f"您要输入数字，例如：027", SyntaxWarning)
            sys.exit()

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
        match 类别:
            case "調值":
                return self.返回調值(字头)
            case "調類":
                return self.返回調類(字头)
            case "發音":
                return self.返回發音(字头)
            case "聲母":
                return self.返回聲母(字头)
            case "韻母":
                return self.返回韻母(字头)
            case _:
                warnings.warn(f"没有此类别", SyntaxWarning)
                sys.exit()