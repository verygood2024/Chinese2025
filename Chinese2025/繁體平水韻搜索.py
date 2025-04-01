import sys
import warnings

from .查询 import 查询

class 繁體平水韻搜索:
    def __init__(self):
        pass

    @staticmethod
    def 返回韻部(字头):
        return list({item[0][-1] for item in 查询.单列查询("ping_shui_yun", "韻部", "字頭", 字头)})

    @staticmethod
    def 返回聲調(字头):
        return list({item[0][-1] for item in 查询.单列查询("ping_shui_yun", "聲調", "字頭", 字头)})

    @staticmethod
    def 返回平仄(字头):
        聲調結果 = {item[0] for item in 查询.单列查询("ping_shui_yun", "聲調", "字頭", 字头)}
        改写规则 = {
            "上": "仄",
            "去": "仄",
            "入": "仄",
            "平": "平"
        }
        改写後平仄 = {改写规则.get(聲調, 聲調) for 聲調 in 聲調結果}
        唯一平仄 = list(改写後平仄)
        return 唯一平仄

    @staticmethod
    def 返回表字典(字头):
        return 查询.多列查询("ping_shui_yun","字頭",字头)

    def 返回(self, 类别, 字头):
        match 类别:
            case "韻部":
                return self.返回韻部(字头)
            case "聲調":
                return self.返回聲調(字头)
            case "平仄":
                return self.返回平仄(字头)
            case "返回表字典":
                return self.返回表字典(字头)
            case _:
                warnings.warn(f"没有此类别", SyntaxWarning)
                sys.exit()