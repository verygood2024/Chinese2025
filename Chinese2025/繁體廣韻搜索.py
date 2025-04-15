import sys
import warnings

from .查询 import 查询
from .Error import 输入不合法

广韵表名字典 = {
    "小學堂":"_020_广韵_小学堂",
    "poem":"guang_yun",
    "nk2028":"nk2028廣韻"
}

广韵字头列字典 = {
    "poem": "廣韻字頭_覈校後",
    "小學堂":"字",
    "nk2028":"字頭"
}

聲母對類別 = {
    "幫": "全清", "滂": "次清", "並": "全濁", "明": "次濁",
    "端": "全清", "透": "次清", "定": "全濁", "泥": "次濁",
    "來": "次濁", "知": "全清", "徹": "次清", "澄": "全濁", "娘": "次濁",
    "精": "全清", "清": "次清", "從": "全濁", "心": "全清", "邪": "全濁",
    "莊": "全清", "初": "次清", "崇": "全濁", "生": "全清", "俟": "全濁",
    "章": "全清", "昌": "次清", "常": "全濁", "書": "全清", "船": "全濁", "日": "次濁",
    "以": "次濁", "見": "全清", "溪": "次清", "群": "全濁", "疑": "次濁",
    "影": "全清", "曉": "全清", "匣": "全濁", "云": "次濁"
}


class 繁體廣韻搜索:
    def __init__(self,来源="poem"):
        if 来源 not in ["小學堂","poem","nk2028"]:
            raise 输入不合法(来源,["小學堂","poem","nk2028"])
        self.表名 = 来源

    def 返回韻目(self, 字头):
        广韵列名字典 = {
            "poem": "韻部_調整後",
            "小學堂": "韻目",
            "nk2028":"韻目原貌"
        }
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名],广韵列名字典[self.表名],广韵字头列字典[self.表名],字头)})

    def 返回韻部(self,字头):
        if self.表名 in ["nk2028", "小學堂"]:
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表。", UserWarning)
            self.表名 = "poem"

        return list({item[0][-2:] for item in 查询.单列查询(广韵表名字典[self.表名], "廣韻韻部順序", 广韵字头列字典[self.表名], 字头)})

    def 返回聲紐(self,字头):
        广韵列名字典 = {
            "poem": "聲紐",
            "小學堂": "字母"
        }
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], 广韵列名字典[self.表名], 广韵字头列字典[self.表名], 字头)})

    def 返回聲調(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "聲調", 广韵字头列字典[self.表名], 字头)})

    def 返回平仄(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
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
        if self.表名 == "nk2028":
            return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "反切", 广韵字头列字典[self.表名],字头)})
        else:
            return [a + b for a, b in zip(list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "上字", 广韵字头列字典[self.表名], 字头)}),
                                      list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "下字", 广韵字头列字典[self.表名], 字头)}))]

    def 返回反切上字(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "上字", 广韵字头列字典[self.表名], 字头)})

    def 返回反切下字(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "下字", 广韵字头列字典[self.表名], 字头)})

    def 返回開合(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        广韵列名字典 = {
            "poem": "呼",
            "小學堂": "開合"
        }
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], 广韵列名字典[self.表名], 广韵字头列字典[self.表名], 字头)})

    def 返回等第(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
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
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "攝", 广韵字头列字典[self.表名], 字头)})

    def 返回清濁(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        if self.表名 == "poem":
            return [聲母對類別[聲紐][1] for 聲紐 in self.返回聲紐(字头)]
        else:
            return list({item[0][1] for item in 查询.单列查询("_020_广韵_小学堂", "清濁", "字", 字头)})

    def 返回全次清濁(self,字头):
        if self.表名 == "nk2028":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        if self.表名 == "poem":
            return [聲母對類別[聲紐] for 聲紐 in self.返回聲紐(字头)]
        else:
            return list({item[0] for item in 查询.单列查询("_020_广韵_小学堂", "清濁", "字", 字头)})

    def 返回表字典(self,字头):
        return 查询.多列查询(广韵表名字典[self.表名],广韵字头列字典[self.表名],字头)

    def 返回音韻地位(self,字头):
        if self.表名 in ["小學堂","poem"]:
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
        return list({item[0] for item in 查询.单列查询("nk2028廣韻", "音韻地位", "字頭", 字头)})

    def 返回釋義(self,字头):
        if self.表名 == "小學堂":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "廣韻釋義", 广韵字头列字典[self.表名], 字头)})

    def 返回補充釋義(self,字头):
        if self.表名 == "小學堂":
            warnings.warn("此表不支持該功能,以自動轉換成支持該功能的表.", UserWarning)
            self.表名 = "poem"
        return list({item[0] for item in 查询.单列查询(广韵表名字典[self.表名], "釋義補充", 广韵字头列字典[self.表名], 字头)})

    def 返回(self, 类别, 字头):
        func_map = {
            "韻部": lambda:self.返回韻部(字头),
            "韵目": lambda:self.返回韻目(字头),
            "聲紐": lambda:self.返回聲紐(字头),
            "聲調": lambda:self.返回聲調(字头),
            "平仄": lambda:self.返回平仄(字头),
            "反切": lambda:self.返回反切(字头),
            "反切上字": lambda:self.返回反切上字(字头),
            "反切下字": lambda:self.返回反切下字(字头),
            "開合":lambda: self.返回開合(字头),
            "等第": lambda:self.返回等第(字头),
            "反切攝": lambda:self.返回攝(字头),
            "清濁": lambda:self.返回清濁(字头),
            "全次清濁": lambda:self.返回全次清濁,
            "音韻地位": lambda:self.返回音韻地位(字头),
            "表字典": lambda:self.返回表字典(字头),
            "釋義": lambda:self.返回釋義(字头),
            "補充釋義": lambda:self.返回補充釋義(字头)
        }

        func = func_map.get(类别)
        if func:
            return func()
        else:
            warnings.warn("没有此类别", SyntaxWarning)
            sys.exit()
