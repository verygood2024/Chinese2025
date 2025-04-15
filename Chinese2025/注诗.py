import pprint
import re

from .Unicode import valid_text, extract_chinese_characters
from .Error import 输入不合法
from .繁體廣韻搜索 import 繁體廣韻搜索
from .繁體平水韻搜索 import 繁體平水韻搜索
from .现代韵书搜索 import 现代韵书搜索

韵字典 = {
    "廣韻":"廣韻",
    "广韵":"廣韻",
    "平水韻":"平水韻",
    "平水韵":"平水韻",
    "现代韵书":"現代韻書",
    "現代韻書":"現代韻書",
    "0":"廣韻",
    "1":"平水韻",
    "2":"現代韻書"
}

class 注诗:
    def __init__(self,text: str,韵="平水韻",多音字=True,自动分词=True,连音变调=False,轻声=False,间隔:str="，"):
        self.yun_list = []
        self.韵书字典 = None
        self.pattern = re.compile(
            r'[\u3400-\u4DBF'  # 扩展A区 (U+3400 - U+4DBF)
            r'\u4E00-\u9FFF'  # 基本汉字 (U+4E00 - U+9FFF)
            r'\U00020000-\U0002A6DF'  # 扩展B区 (U+20000 - U+2A6DF)
            r'\U0002A700-\U0002B734'  # 扩展C区 (U+2A700 - U+2B734)
            r'\U0002B740-\U0002B81F'  # 扩展D区 (U+2B740 - U+2B81F)
            r'\U0002B820-\U0002CEAF'  # 扩展E区 (U+2B820 - U+2CEAF)
            r'\U0002CEB0-\U0002EBEF'  # 扩展F区 (U+2CEB0 - U+2EBEF)
            r'\U0002EBF0-\U0002EE5D'  # 扩展I区 (U+2EBF0 - U+2EE5D)
            r'\U00030000-\U0003134A'  # 扩展G区 (U+30000 - U+3134A)
            r'\U00031350-\U000323AF'  # 扩展H区 (U+31350 - U+323AF)
            r']'
        )
        if not valid_text(text):
            raise 输入不合法(text, "字符串不合法.并不允许中文与标点符号除外的字符.")

        韵_str = str(韵)
        if 韵_str not in 韵字典:
            raise 输入不合法(韵_str, pprint.pformat(sorted(韵字典), compact=True))
        self.韵 = 韵字典[韵_str]
        self.text = text
        self.多音字 = 多音字
        self.自动分词 = 自动分词
        self.连音变调 = 连音变调
        self.间隔 = 间隔
        self.轻声 = 轻声

    def __获取(self, last_chars, 韵书字典, 类别="韻部"):
        if self.韵 in ["廣韻","平水韻"]:
            for i, word in enumerate(last_chars):
                if self.韵 == "廣韻":
                    result = 繁體廣韻搜索().返回(类别,word)
                elif self.韵 == "平水韻":
                    result = 繁體平水韻搜索().返回(类别,word)
                else:
                    result = 繁體平水韻搜索().返回(类别,word)
                if len(result) == 0:
                    self.yun_list.append(None)
                else:
                    self.yun_list.append(result)
        else:
            for 韵部 in 现代韵书搜索(韵书字典=韵书字典, 多音字=self.多音字, 自动分词=self.自动分词,
                                   连音变调=self.连音变调,轻声=self.轻声).返回(类别,self.text):
                #print(韵部)
                if 韵部 is None:
                    self.yun_list.append(None)
                elif isinstance(韵部, list) and 韵部:
                    self.yun_list.append(韵部)
                else:
                    self.yun_list.append(None)

    def __逐字标注(self,yun_list: list) -> str:
        lines = self.text.splitlines()
        annotated_text = ""

        for line, yun_line in zip(lines, yun_list):
            if not line.strip():
                annotated_text += "\n"
                continue
            hanzi_matches = self.pattern.findall(line)
            new_line = ""
            for hanzi, yun in zip(hanzi_matches, yun_line):
                if isinstance(yun, list):
                    yun_text = f"{self.间隔}".join(str(y) for y in yun)
                elif yun is not None:
                    yun_text = str(yun)
                else:
                    yun_text = "None"
                new_line += f"{hanzi}({yun_text})"
            annotated_text += new_line + "\n"

        self.yun_list = []

        return annotated_text.strip()

    def 古体(self,韵书字典:dict|str="中华通韵"):
        if self.韵 == "現代韻書":
            if isinstance(韵书字典, dict):
                if len(韵书字典) != 36:
                    raise 输入不合法(韵书字典, "输入的字典长度必须等于36.")
                self.韵书字典 = 韵书字典
            elif 韵书字典 in ["中华通韵", "中華通韻", "0", 0]:
                self.韵书字典 = "中华通韵"
            elif 韵书字典 in ["中华新韵", "中華新韻", "1", 1]:
                self.韵书字典 = "中华新韵"
            else:
                raise 输入不合法(韵书字典, pprint.pformat(sorted(["中华通韵", "中華通韻", "0", 0] + ["中华新韵", "中華新韻", "1", 1]), compact=True))

        last_chars = extract_chinese_characters(self.text)

        self.__获取(last_chars, 韵书字典)

        annotated_text = ""

        lines = self.text.splitlines()
        #print(self.yun_list)
        for line, yun in zip(lines, self.yun_list):
            if not line.strip():
                continue
            hanzi_matches = self.pattern.findall(line)
            if not hanzi_matches:
                annotated_text += line + "\n"
                continue
            last_hanzi = hanzi_matches[-1]
            #print("yun",yun)
            if isinstance(yun, list):
                yun_text = f"{self.间隔}".join(str(y) for y in yun)
            elif yun is not None:
                yun_text = str(yun)
            else:
                yun_text = "None"

            annotated = f"{last_hanzi}({yun_text})"

            idx = line.rfind(last_hanzi)
            new_line = line[:idx] + annotated + line[idx + 1:]
            annotated_text += new_line + "\n"

        annotated_text = annotated_text.strip()

        self.yun_list = []

        return annotated_text

    def 韵部(self):
        last_chars = extract_chinese_characters(self.text)

        self.__获取(last_chars, None, "韻部")

        return self.__逐字标注(self.yun_list)

    def 声调(self):
        last_chars = extract_chinese_characters(self.text)

        self.__获取(last_chars, None,"聲調")

        return self.__逐字标注(self.yun_list)

    def 平仄(self):
        last_chars = extract_chinese_characters(self.text)

        self.__获取(last_chars, None, "平仄")

        return self.__逐字标注(self.yun_list)