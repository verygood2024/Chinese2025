import sys
import warnings

from 单列查询 import 查询

广韵表名字典 = {
    "小學堂":"_020_广韵_小学堂",
    "poem":"guang_yun"
}

广韵字头列字典 = {
    "poem": "廣韻字頭_覈校後",
    "小學堂":"字"
}

class 繁體廣韻搜索:
    def __init__(self,来源="小學堂"):
        if 来源 not in ["小學堂","poem"]:
            warnings.warn(f"没有此来源", SyntaxWarning)
            sys.exit()
        self.表名 = 来源

    def 返回韻部(self,字头):
        广韵列名字典 = {
            "poem": "韻部_調整後",
            "小學堂": "韻目"
        }
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名],广韵列名字典[self.表名],广韵字头列字典[self.表名],字头)})

    def 返回聲紐(self,字头):
        广韵列名字典 = {
            "poem": "聲紐",
            "小學堂": "字母"
        }
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], 广韵列名字典[self.表名], 广韵字头列字典[self.表名], 字头)})

    def 返回聲調(self,字头):
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "聲調", 广韵字头列字典[self.表名], 字头)})

    def 返回平仄(self,字头):
        聲調結果 = {item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "聲調", 广韵字头列字典[self.表名], 字头)}
        改写规则 = {
            "上": "仄",
            "去": "仄",
            "入": "仄",
            "平": "平"
        }
        改写後平仄 = {改写规则.get(聲調, 聲調) for 聲調 in 聲調結果}
        唯一平仄 = list(改写後平仄)
        return 唯一平仄

    def 返回反切(self,字头):
        return [a + b for a, b in zip(list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "上字", 广韵字头列字典[self.表名], 字头)}),
                                      list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "下字", 广韵字头列字典[self.表名], 字头)}))]

    def 返回反切上字(self,字头):
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "上字", 广韵字头列字典[self.表名], 字头)})

    def 返回反切下字(self,字头):
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "下字", 广韵字头列字典[self.表名], 字头)})

    def 返回開合(self,字头):
        广韵列名字典 = {
            "poem": "呼",
            "小學堂": "開合"
        }
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], 广韵列名字典[self.表名], 广韵字头列字典[self.表名], 字头)})

    def 返回等第(self,字头):
        广韵列名字典 = {
            "poem": "等",
            "小學堂": "等第"
        }
        等第結果 = list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], 广韵列名字典[self.表名], 广韵字头列字典[self.表名], 字头)})
        改写规则 = {
            "1": "一",
            "2": "二",
            "3": "三",
            "4": "四"
        }
        改写後等第 = {改写规则.get(等第, 等第) for 等第 in 等第結果}

        return 改写後等第

    def 返回攝(self,字头):
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "攝", 广韵字头列字典[self.表名], 字头)})

    @staticmethod
    def 返回清濁(字头):
        return list({item[0] for item in 查询.单列查询("_020_广韵_小学堂", "清濁", "字", 字头)})

    def 返回(self, 类别, 字头):
        match 类别:
            case "韻部":
                return self.返回韻部(字头)
            case "聲紐":
                return self.返回聲紐(字头)
            case "聲調":
                return self.返回聲調(字头)
            case "平仄":
                return self.返回平仄(字头)
            case "反切":
                return self.返回反切(字头)
            case "反切上字":
                return self.返回反切上字(字头)
            case "反切下字":
                return self.返回反切下字(字头)
            case "開合":
                return self.返回開合(字头)
            case "等第":
                return self.返回等第(字头)
            case "反切攝":
                return self.返回攝(字头)
            case "清濁":
                return self.返回清濁(字头)
            case _:
                warnings.warn(f"没有此类别", SyntaxWarning)
                sys.exit()