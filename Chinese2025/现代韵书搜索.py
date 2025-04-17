from .Error import 输入不合法
import pprint
import warnings
import sys

from pypinyin import pinyin, lazy_pinyin,Style

# 加载所有单字拼音数据
from pypinyin_dict.pinyin_data import (
    ktghz2013, khanyupinyin, kxhc1983, khanyupinlu,
    kmandarin_8105, pinyin as pinyin_data_file, zdic, cc_cedict
)

ktghz2013.load()
khanyupinyin.load()
kxhc1983.load()
khanyupinlu.load()
kmandarin_8105.load()
pinyin_data_file.load()
zdic.load()
cc_cedict.load()

# 加载所有词组拼音数据
from pypinyin_dict.phrase_pinyin_data import (
    pinyin as phrase_pinyin,
    zdic_cibs, zdic_cybs, cc_cedict as phrase_cc_cedict,
    di, large_pinyin
)

phrase_pinyin.load()
zdic_cibs.load()
zdic_cybs.load()
phrase_cc_cedict.load()
di.load()
large_pinyin.load()


from 全局变量 import 中华通韵字典,中华新韵字典

声母列表 = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
           'g', 'k', 'h', 'j', 'q', 'x',
           'zh', 'ch', 'sh', 'r', 'z', 'c', 's',
           'y', 'w']

class 现代韵书搜索:
    def __init__(self,韵书字典="中华通韵",多音字:bool=True,自动分词:bool=True,连音变调:bool=False,轻声:bool=False, 特殊声母="特殊声母", 转换符:str= "-i", 转换前符:str= "i"):
        if 韵书字典 is None:
            韵书字典 = "中华通韵"
        if isinstance(韵书字典,dict):
            if len(韵书字典) != 41:
                raise 输入不合法(韵书字典,"输入的字典长度必须等于41.")
            self.韵书字典 = 韵书字典
        elif 韵书字典 in ["中华通韵","中華通韻","0",0]:
            self.韵书字典 = 中华通韵字典
        elif 韵书字典 in ["中华新韵","中華新韻","1",1]:
            self.韵书字典 = 中华新韵字典
        else:
            raise 输入不合法(韵书字典, pprint.pformat(sorted(["中华通韵","中華通韻","0",0] + ["中华新韵","中華新韻","1",1]), compact=True))

        if 连音变调:
            self.多音字, self.自动分词 = False, True
        else:
            self.多音字, self.自动分词 = 多音字, (False if 多音字 else 自动分词)

        self.连音变调 = 连音变调

        self.轻声 = 轻声

        self.特殊声母 = 特殊声母
        self.转换符 = 转换符
        self.转换前符 = 转换前符

    '''原型:
    def __返回拼音(self, 字头):
        拼音韵母有多音字 = pinyin(字头, style=Style.FINALS, heteronym=True, errors='ignore', strict=True, v_to_u=False,
                                  neutral_tone_with_five=False)
        拼音韵母无多音字 = pinyin(字头, style=Style.FINALS, heteronym=False, errors='ignore', strict=True,
                                  v_to_u=False, neutral_tone_with_five=False)

        拼音有多音字 = pinyin(字头, style=Style.NORMAL, heteronym=True, errors='ignore', strict=True, v_to_u=False,
                              neutral_tone_with_five=False)
        拼音无多音字 = pinyin(字头, style=Style.NORMAL, heteronym=False, errors='ignore', strict=True, v_to_u=False,
                              neutral_tone_with_five=False)

        if not self.多音字 and not self.自动分词:
            拼音韵母有多音字 = [[None] if len(p) > 1 else p for p in 拼音韵母有多音字]
            return 拼音韵母有多音字
        elif not self.多音字 and self.自动分词:
            return 拼音韵母无多音字
        else:
            return 拼音韵母有多音字
    '''


    def __返回韵母(self, 字头, 特殊声母="特殊声母", 转换符:str= "-i", 转换前符:str= "i"):
        if self.连音变调:
            拼音韵母有多音字 = lazy_pinyin(字头, style=Style.FINALS, errors='ignore', strict=True,v_to_u=False,neutral_tone_with_five=False,tone_sandhi=True)
            拼音韵母无多音字 = lazy_pinyin(字头, style=Style.FINALS, errors='ignore', strict=True,v_to_u=False, neutral_tone_with_five=False,tone_sandhi=True)
            拼音无多音字 = lazy_pinyin(字头, style=Style.NORMAL,errors='ignore', strict=True, v_to_u=True, neutral_tone_with_five=False,tone_sandhi=True)
            拼音有多音字 = lazy_pinyin(字头, style=Style.NORMAL,errors='ignore', strict=True, v_to_u=False, neutral_tone_with_five=False,tone_sandhi=True)
        else:
            拼音韵母有多音字 = pinyin(字头, style=Style.FINALS, heteronym=True, errors='ignore', strict=True,v_to_u=False,neutral_tone_with_five=False)
            拼音韵母无多音字 = pinyin(字头, style=Style.FINALS, heteronym=False, errors='ignore', strict=True,v_to_u=False, neutral_tone_with_five=False)

            拼音有多音字 = pinyin(字头, style=Style.NORMAL, heteronym=True,errors='ignore', strict=True, v_to_u=False, neutral_tone_with_five=False)
            拼音无多音字 = pinyin(字头, style=Style.NORMAL, heteronym=False,errors='ignore', strict=True, v_to_u=False, neutral_tone_with_five=False)

        if not self.多音字:
            if not self.自动分词:
                finals = [[None] if len(p) > 1 else p for p in 拼音韵母有多音字]
                py_list = 拼音有多音字
            else:
                finals = 拼音韵母无多音字
                py_list = 拼音无多音字
        else:
            finals = 拼音韵母有多音字
            py_list = 拼音有多音字

        if 特殊声母 == "特殊声母":
            特殊声母 = {"zi", "ci", "si", "zhi", "chi", "shi", "ri"}
        elif isinstance(特殊声母, set):
            if len(特殊声母) <= 23:
                raise 输入不合法(特殊声母, "输入的集合长度必须等于23.")

        for idx in range(len(finals)):
            if any(py_candidate in 特殊声母 for py_candidate in py_list[idx]):
                finals[idx] = [f"{转换符}" if elem == f"{转换前符}" else elem for elem in finals[idx]]

        return finals

    def 返回韵部(self, 字头):
        韵部结果 = []
        #ppprint(self.返回拼音(字头))
        for 韵母候选 in  self.__返回韵母(字头, 特殊声母=self.特殊声母, 转换符=self.转换符, 转换前符=self.转换前符):
            if not 韵母候选 or 韵母候选[0] is None:
                韵部结果.append([None])
            else:
                单字韵部 = []
                for 韵母 in 韵母候选:
                    韵部 = self.韵书字典[韵母]
                    #print(韵母, 韵部)
                    单字韵部.append(韵部 if 韵部 is not None else None)
                韵部结果.append(单字韵部)
        return self.__为空则None(韵部结果)

    def 返回韵目(self,字头):
        韵部列表 = self.返回韵部(字头)
        声调列表 = self.返回声调(字头)

        # 合并：对两个嵌套列表对应位置的字符串合并
        合并结果 = []
        for 韵部子列表, 声调子列表 in zip(韵部列表, 声调列表):
            合并子列表 = [a + b for a, b in zip(韵部子列表, 声调子列表)]
            合并结果.append(合并子列表)

        return 合并结果

    '''
    @staticmethod
    def __去声母(拼音列表):
        结果 = []
        for 词组 in 拼音列表:
            新词组 = []
            for 拼 in 词组:
                原拼 = 拼.lower()
                去除 = 原拼
                匹配到声母 = ""
                # 按声母长度从长到短排序，优先匹配 zh ch sh
                for shengmu in sorted(声母列表, key=lambda x: -len(x)):
                    if 原拼.startswith(shengmu):
                        匹配到声母 = shengmu
                        去除 = 原拼[len(shengmu):]
                        break

                # 特别处理 j/q/x + u 或 ue 的情况，应还原为 jü/qü/xü
                if 匹配到声母 in {"j", "q", "x"}:
                    if 去除 == "u":
                        去除 = "v"
                    elif 去除.startswith("u") and not 去除.startswith("ua") and not 去除.startswith("uo"):
                        # 例如 "ue" -> "üe"
                        去除 = "v" + 去除[1:]

                新词组.append(去除)
            结果.append(新词组)
        return 结果
        '''

    @staticmethod
    def __转换(音列表,s1="阴平",s2="阳平",s3="上",s4="去"):
        结果 = []
        for 音 in 音列表:
            单字结果 = []
            for 拼音项 in 音:
                if 拼音项 is None:
                    单字结果.append(None)
                elif isinstance(拼音项, str) and 拼音项 and 拼音项[-1].isdigit():
                    声调 = 拼音项[-1]
                    if 声调 == '1':
                        单字结果.append(f"{s1}")
                    elif 声调 == '2':
                        单字结果.append(f"{s2}")
                    elif 声调 == '3':
                        单字结果.append(f"{s3}")
                    elif 声调 == '4':
                        单字结果.append(f"{s4}")
                    else:
                        单字结果.append("轻")
                else:
                    单字结果.append("轻")
            结果.append(单字结果)
        return 结果

    def __获取声调(self,字头):
        if self.连音变调:
            声调有多音字 = lazy_pinyin(字头, style=Style.TONE3,errors='ignore', strict=True, v_to_u=False, neutral_tone_with_five=True,tone_sandhi=True)
            声调无多音字 = lazy_pinyin(字头, style=Style.TONE3,errors='ignore', strict=True, v_to_u=False, neutral_tone_with_five=True,tone_sandhi=True)
        else:
            声调有多音字 = pinyin(字头, style=Style.TONE3, heteronym=True, errors='ignore', strict=True, v_to_u=False,neutral_tone_with_five=True)
            声调无多音字 = pinyin(字头, style=Style.TONE3, heteronym=False, errors='ignore', strict=True, v_to_u=False,neutral_tone_with_five=True)
        return 声调有多音字,声调无多音字

    @staticmethod
    def __为空则None(传入):
        return [[None] if len(p) < 1 else p for p in 传入]

    def __过滤轻声(self,a):
        声调有多音字, 声调无多音字 = a
        if self.轻声:
            return 声调有多音字, 声调无多音字

        结果 = []
        for idx, (多音列表, 单音列表) in enumerate(zip(声调有多音字, 声调无多音字)):
            非轻声列表 = [音 for 音 in 多音列表 if not 音.endswith('5')]

            if 单音列表[0].endswith('5') and 非轻声列表:
                结果.append([非轻声列表[0]])
            else:
                结果.append(单音列表)

        return 结果, 结果

    @staticmethod
    def __移除重复(lst):
        """
        对列表中的每个子列表进行去重，保持原来顺序
        例如：[['去', '去', '阴平'], ['中', '中']] 变成 [['去', '阴平'], ['中']]
        """
        # 利用字典保持顺序去重（Python3.6+ 保证了有序）
        return [list(dict.fromkeys(sub)) for sub in lst]

    def 返回声调(self,字头,s1="阴平",s2="阳平",s3="上",s4="去"):
        声调有多音字, 声调无多音字 = self.__过滤轻声(self.__获取声调(字头))

        #print(声调有多音字)
        #print(声调无多音字)

        if not self.多音字 and not self.自动分词:
            转换结果 = self.__转换([[None] if len(p) > 1 else p for p in 声调有多音字],s1,s2,s3,s4)
        elif not self.多音字 and self.自动分词:
            转换结果 = self.__转换(声调无多音字,s1,s2,s3,s4)
        else:
            转换结果 = self.__转换(声调有多音字,s1,s2,s3,s4)

        转换结果 = self.__移除重复(转换结果)

        return self.__为空则None(转换结果)

    def 返回平仄(self,字头):
        return self.返回声调(字头,"平","平","仄","仄")

    def 返回(self,类别,字头):
        func_map = {
            "韵部":lambda: self.返回韵部(字头),
            "声调":lambda: self.返回声调(字头),
            "平仄":lambda: self.返回平仄(字头),
            "韻部": lambda: self.返回韵部(字头),
            "聲調": lambda: self.返回声调(字头),
            "韵目": lambda: self.返回韵目(字头),
            "韻目": lambda: self.返回韵目(字头),
        }

        func = func_map.get(类别)
        if func:
            return self.__为空则None(func())
        else:
            warnings.warn("没有此类别", SyntaxWarning)
            sys.exit()