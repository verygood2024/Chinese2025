from pprint import pprint
import re
import warnings
import sys

from Error import 输入不合法
from .繁體擬音搜索 import 繁體擬音搜索
from .繁體廣韻搜索 import 繁體廣韻搜索
from .繁體平水韻搜索 import 繁體平水韻搜索


class WordProcessor:
    def __init__(self, words):
        self.words = words
        self.result = []

    def process(self):
        temp = []  # 临时列表，用来存储每段处理的数据
        count = 0  # 记录括号外字的数量

        for word in self.words:
            # 判断是否有 "-"，如果有，拆分并加括号
            if '-' in word:
                base, suffix = word.split('-', 1)
                temp.append(f"{base}({suffix})")
                count += 1  # 增加一个括号外的字
            else:
                temp.append(word)
                count += 1  # 增加一个括号外的字

            # 每五个括号外字添加逗号，每十个括号外字添加句号并换行
            if count % 5 == 0 and (count % 10 != 0):  # 每五个字加逗号，排除十个字的情况
                temp.append('，')
            if count % 10 == 0:  # 每十个字加句号并换行
                temp.append('。')
                self.result.append(' '.join(temp))  # 句号后换行
                temp = []  # 清空临时列表
                count = 0  # 重置计数器

        # 处理剩余部分
        if temp:
            self.result.append(' '.join(temp))

    def get_result(self):
        return '\n'.join(self.result)

时代字典 = {
    "魏晉":"魏晉",
    "魏晋":"魏晉",
    "隋唐":"隋唐",
    "現代":"现代",
    "现代":"现代",
    "0":"魏晉",
    "1":"隋唐",
    #"2":"现代"
}

列字典 = {
    "拼音":"tupa_js",
    "白一平":"baxter_js",
    "高汉本": "karlgren_js",
    "高本漢":"karlgren_js",
    "潘悟云": "panwuyun_js",
    "潘悟雲":"panwuyun_js",
    "王力汉语语音史魏晋":"wangli魏晋南北朝_js",
    "王力汉语语音史隋唐": "wangli隋唐_js",
    "王力汉语史稿":"wangli汉语史稿_js",
    "王力漢語語音史魏晉":"wangli魏晋南北朝_js",
    "王力漢語語音史隋唐": "wangli隋唐_js",
    "王力漢語史稿":"wangli汉语史稿_js",
    "0":"tupa_js",
    "1":"baxter_js",
    "2":"karlgren_js",
    "3":"panwuyun_js",
    "4":"wangli魏晋南北朝_js",
    "5": "wangli隋唐_js",
    "6":"wangli汉语史稿_js",
}

韵字典 = {
    "王力汉语语音史魏晋":"王力漢語語音史魏晉",
    "王力漢語語音史魏晉":"王力漢語語音史魏晉",
    "廣韻":"廣韻",
    "广韵":"廣韻",
    "平水韻":"平水韻",
    "平水韵":"平水韻",
    "0":"王力漢語語音史魏晉",
    "1":"廣韻",
    "2":"平水韻",
}

基础无韵尾 = {
    "ə":"之",
    "e":"支",
    "ɑ":"歌",
    "ɔ":"鱼",
    "o":"模",
}

i韵尾 = {
    "ə":"微",
    "e":"脂",
    "ɐ":"灰",
    "ɑ":"泰",
    "æ":"祭",
}

k韵尾 = {
    "ə":"职",
    "ɐ":"德",
    "e":"锡",
    "ɑ":"铎",
    "o":"屋",
    "u":"沃"
}

t韵尾 = {
    "ə":"物",
    "e":"质",
    "ɐ":"没",
    "ɑ":"曷",
    "æ":"薛",
}

p韵尾 = {
    "ə":"缉",
    "ɐ":"业",
    "ɑ":"合",
    "æ":"葉",
}

ng韵尾 = {
    "ə":"蒸",
    "ɐ":"登",
    "e":"耕",
    "ɑ":"阳",
    "o":"东",
    "u":"冬"
}

n韵尾 = {
    "ə":"文",
    "e":"真",
    "ɐ":"魂",
    "ɑ":"寒",
    "æ":"仙",
}

m韵尾 = {
    "ə":"侵",
    "ɐ":"严",
    "ɑ":"覃",
    "æ":"盐",
}

#韵列表 = ["王力汉语语音史魏晋","廣韻","广韵","平水韻","平水韵","0","1","2"]
#声调列表 = ["平上去入","平仄","0","1"]

声调字典 = {
    "平上去入":"平上去入",
    "平仄":"平仄",
    "0":"平上去入",
    "1":"平仄"
}

蜂腰字典 = {
    "二五同调":"二五同調",
    "二五同調":"二五同調",
    "二四同调":"二四同調",
    "二四同調":"二四同調",
    "二四同浊":"二四同濁",
    "二四同濁":"二四同濁",
    "二四同浊调":"二四同濁調",
    "二四同濁調":"二四同濁調",
    "中浊四清":"中濁四清",
    "中濁四清":"中濁四清",
    "0":"二五同調",
    "1":"二四同調",
    "2":"二四同濁",
    "3":"二四同濁調",
    "4":"中濁四清",
}

鹤膝字典 = {
    "五与十五同调":"五與十五同調",
    "五與十五同調":"五與十五同調",
    "二四同清":"二四同清",
    "中清四濁":"中清四濁",
    "中清四浊":"中清四濁",
    "0":"五與十五同調",
    "1":"二四同清",
    "2":"中清四濁",
}

小韵字典 = {
    "字韵部不同":"字韻部不同",
    "字韻部不同":"字韻部不同",
    "上下字韵部不同":"上下字韻部不同",
    "上下字韻部不同":"上下字韻部不同",
    "上四下一非同韵部":"上四下一非同韻部",
    "上四下一非同韻部":"上四下一非同韻部",
    "0":"字韻部不同",
    "1":"上下字韻部不同",
    "2":"上四下一非同韻部",
}

旁纽字典 = {
    "韵部检查-半联":"韻部檢查-半聯",
    "韻部檢查-半聯":"韻部檢查-半聯",
    "主元音韵尾检查-半联":"主元音韻尾檢查-半聯",
    "主元音韻尾檢查-半聯":"主元音韻尾檢查-半聯",
    "韵母检查-半联":"韻母檢查-半聯",
    "韻母檢查-半聯":"韻母檢查-半聯",
    "韵部检查-全联":"韻部檢查-全聯",
    "韻部檢查-全聯":"韻部檢查-全聯",
    "主元音韵尾检查-全联":"主元音韻尾檢查-全聯",
    "主元音韻尾檢查-全聯":"主元音韻尾檢查-全聯",
    "韵母检查-全联":"韻母檢查-全聯",
    "韻母檢查-全聯":"韻母檢查-全聯",
    "0":"韻部檢查-半聯",
    "1":"主元音韻尾檢查-半聯",
    "3":"韻母檢查-半聯",
    "4":"韻部檢查-全聯",
    "5":"主元音韻尾檢查-全聯",
    "6":"韻母檢查-全聯"
}

聲母字典 = {
    '幫': 'p',  '滂': 'pʰ',  '並': 'bʱ',  '明': 'm',
    '端': 't',  '透': 'tʰ',  '定': 'dʱ',  '泥': 'n',             '來': 'l',
    '知': 't',  '徹': 'tʰ',  '澄': 'dʱ',  '孃': 'n',
    '精': 'ts', '清': 'tsʰ', '從': 'dzʱ',          '心': 's', '邪': 'z',
    '莊': 'tʃ', '初': 'tʃʰ', '崇': 'dʒʱ',          '生': 'ʃ', '俟': 'ʒ',
    '章': 'tɕ', '昌': 'tɕʰ', '船': 'dʑʱ', '日': 'ȵ', '書': 'ɕ', '常': 'ʑ', '以': 'j',
    '見': 'k',  '溪': 'kʰ',  '羣': 'ɡʱ',  '疑': 'ŋ', '曉': 'x', '匣': 'ɣ', '云': 'ɣ',
    '影': 'ʔ',}

class YongMingTi:
    def __init__(self, text: str, 时代="魏晉", 源="王力汉语语音史魏晋", 韵="王力汉语语音史魏晋", 声调="平上去入",蜂腰="二四同浊",鹤膝="二四同清",小韵="上下字韵部不同",旁纽="主元音韵尾检查-半联"):
        if not re.fullmatch(r'^[\u4E00-\u9FFF\u3400-\u4DBF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\n\r]+$', text):
            raise 输入不合法(text,"字符串不合法.并不允许中文与标点符号除外的字符.")
        
        时代_str = str(时代)
        if 时代_str not in 时代字典:
            raise 输入不合法(时代_str,pprint.pformat(sorted(时代字典),compact=True))
        self.时代 = 时代字典[时代_str]

        源_str = str(源)
        if 源_str not in 列字典:
            raise 输入不合法(源_str,pprint.pformat(sorted(列字典),compact=True))
        self.源 = 列字典[源_str]

        韵_str = str(韵)
        if 韵_str not in 韵字典:
            raise 输入不合法(韵_str,pprint.pformat(sorted(韵字典),compact=True))
        self.韵 = 韵字典[韵_str]

        声调_str = str(声调)
        if 声调_str not in 声调字典:
            raise 输入不合法(声调_str,pprint.pformat(sorted(声调字典),compact=True))
        self.声调 = 声调_str

        蜂腰_str = str(蜂腰)
        if 蜂腰_str not in 蜂腰字典:
            raise 输入不合法(蜂腰_str,pprint.pformat(sorted(蜂腰字典),compact=True))
        self.蜂腰 = 蜂腰字典[蜂腰_str]

        鹤膝_str = str(鹤膝)
        if 鹤膝_str not in 鹤膝字典:
            raise 输入不合法(鹤膝_str,pprint.pformat(sorted(鹤膝字典),compact=True))
        self.鹤膝 = 鹤膝字典[鹤膝_str]

        小韵_str = str(小韵)
        if 小韵_str not in 小韵字典:
            raise 输入不合法(小韵_str,pprint.pformat(sorted(小韵字典),compact=True))
        self.小韵 = 小韵字典[小韵_str]

        旁纽_str = str(旁纽)
        if 旁纽_str not in 旁纽字典:
            raise 输入不合法(旁纽_str,pprint.pformat(sorted(旁纽字典),compact=True))
        self.旁纽 = 旁纽字典[旁纽_str]

        self.get_all = '\n'.join(line.strip() for line in text.splitlines())


    @staticmethod
    def __remove_chars(text, chars_to_remove):
        """
        使用正则表达式删除多个字符
        """
        # 将字符集合转换为正则表达式字符类
        pattern = f"[{re.escape(chars_to_remove)}]"
        return re.sub(pattern, '', text)

    def fetch(self):
        print("开始检查-请用繁体")
        hanzi_regex = r"[\u4E00-\u9FFF\u3400-\u4DBF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F]"
        get_all_list = re.findall(hanzi_regex, self.get_all, flags=re.UNICODE)
        #print(get_all_list)
        #print(len(get_all_list))

        if len(get_all_list)<20:
            sys.exit(warnings.warn(f"至少输入二句（二十个字）.", SyntaxWarning))

        基础标点符号列表 = re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', self.get_all, flags=re.UNICODE)
        qing_zhuo_list = []
        sheng_diao_list = []
        reconstructions_list = []
        yun_list = []
        main_vowel_rhyme_tail_list = []
        shengmu_yuanyin_yunwei_list = []
        多音字 = []
        没有字 = []

        for i,word in enumerate(get_all_list):
            result = 繁體擬音搜索().返回擬音(word)[word]
            result_len = len(result)
            if result_len > 1:#多音字
                reconstructions_list.append(None)
                qing_zhuo_list.append(None)
                yun_list.append(None)
                sheng_diao_list.append(None)
                main_vowel_rhyme_tail_list.append(None)
                shengmu_yuanyin_yunwei_list.append(None)
                多音字.append([word,i])
            elif result_len == 0:#没有此字
                reconstructions_list.append(None)
                qing_zhuo_list.append(None)
                yun_list.append(None)
                sheng_diao_list.append(None)
                main_vowel_rhyme_tail_list.append(None)
                shengmu_yuanyin_yunwei_list.append(None)
                没有字.append([word, i])
            else:
                '''擬音'''
                擬音 = result[0][0]
                reconstructions_list.append(擬音)
                '''清濁'''
                qing_zhuo_list.append(繁體廣韻搜索().返回清濁(word)[0])

                '''韻部'''
                if self.韵 == "王力漢語語音史魏晉":
                    last_char = 擬音[-1]
                    second_last_char = 擬音[-2]

                    # 无韵尾
                    韵F = 基础无韵尾.get(last_char, False)
                    if 韵F:
                        yun_list.append(韵F)
                    elif last_char == "u":
                        韵F = "宵" if second_last_char == "o" else "幽"
                        yun_list.append(韵F)

                    #有韵尾
                    yun_mapping = {
                        "i": i韵尾,
                        "k": k韵尾,
                        "t": t韵尾,
                        "p": p韵尾,
                        "ŋ": ng韵尾,
                        "n": n韵尾,
                        "m": m韵尾
                    }

                    if last_char in yun_mapping:
                        韵F = yun_mapping[last_char].get(second_last_char, None)
                        yun_list.append(韵F)
                    print(i,":",word,":",韵F)
                    #print(word)
                elif self.韵 == "廣韻":
                    韵F = 繁體廣韻搜索().返回韻部(word)[0]
                    yun_list.append(韵F)
                elif self.韵 == "平水韻":
                    韵F = 繁體平水韻搜索().返回韻部(word)[0]
                    yun_list.append(韵F)

                '''聲調'''
                if self.声调 == "平上去入":
                    sheng_diao_list.append(繁體廣韻搜索().返回聲調(word)[0])
                else:
                    sheng_diao_list.append(繁體廣韻搜索().返回平仄(word)[0])

                '''旁纽'''

                輔音 = 聲母字典[result[0][4][0]]
                韻母 = YongMingTi.__remove_chars(擬音, 輔音)

                if self.旁纽 == "韻母檢查-半聯" or "韻母檢查-全聯":
                    main_vowel_rhyme_tail_list.append(韻母)
                else:
                    main_vowel_rhyme_tail_list = yun_list

                '''正纽'''

                # noinspection PyUnboundLocalVariable
                正纽 = 輔音 + str(韵F or "")
                shengmu_yuanyin_yunwei_list.append(正纽)

        return self.__sickness_detect(sheng_diao_list, qing_zhuo_list, yun_list, main_vowel_rhyme_tail_list, shengmu_yuanyin_yunwei_list, get_all_list)

    def __sickness_detect(self, sheng_diao_list, qing_zhuo_list, yun_list, main_vowel_rhyme_tail_list, shengmu_yuanyin_yunwei_list, get_all_list):
        """
        :param shengmu_yuanyin_yunwei_list: 聲母與主元音與韻尾列表
        :param main_vowel_rhyme_tail_list: 主元音與韻尾列表或韻母列表
        :param yun_list: 韻部列表
        :param qing_zhuo_list: 清濁列表
        :param sheng_diao_list: 聲調列表
        :param get_all_list: 字符列表
        :return:
        """
        print(len(yun_list))
        '''押韻'''

        tenth_elements = [yun_list[i] for i in range(9, len(sheng_diao_list), 10)]

        get_all_list = self.__rhyme_or_shang_wei(tenth_elements, get_all_list, 10, 9, "出韻")

        '''平頭'''

        if sheng_diao_list[0] == sheng_diao_list[5] and sheng_diao_list[0] is not None:
            _0 = get_all_list[0]
            _5 = get_all_list[5]
            get_all_list[0] = f"{_0}-平頭"
            get_all_list[5] = f"{_5}-平頭"

        if sheng_diao_list[1] == sheng_diao_list[6] and sheng_diao_list[1] is not None:
            _1 = get_all_list[1]
            _6 = get_all_list[6]
            get_all_list[1] = f"{_1}-平頭"
            get_all_list[6] = f"{_6}-平頭"
        '''上尾'''

        # 提取每五个元素的第五个元素
        fifth_elements = [sheng_diao_list[i] for i in range(4, len(sheng_diao_list), 5)]

        get_all_list = self.__rhyme_or_shang_wei(fifth_elements, get_all_list, 5, 4, "上尾")

        '''蜂腰'''

        '''聲調'''

        # 提取每五个元素的第二个元素，并保留索引
        first_elements = [(sheng_diao_list[i], i) for i in range(1, len(sheng_diao_list), 5)]

        # 获取每五个元素的第四个元素，并保留索引
        fourth_elements = [(sheng_diao_list[i], i) for i in range(3, len(sheng_diao_list), 5)]

        # 提取每五个元素的第五个元素，并保留索引
        fifth_elements_new = [(sheng_diao_list[i], i) for i in range(4, len(sheng_diao_list), 5)]

        '''清濁'''
        # 提取每五个元素的第二个元素，并保留索引
        first_elements_qing_zhuo = [(qing_zhuo_list[i], i) for i in range(1, len(qing_zhuo_list), 5)]

        # 获取每五个元素的第四个元素，并保留索引
        fourth_elements_qing_zhuo = [(qing_zhuo_list[i], i) for i in range(3, len(qing_zhuo_list), 5)]

        if self.蜂腰 == "二五同調":
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements, fifth_elements_new, sickness="蜂腰")
        elif self.蜂腰 == "二四同調":
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements, fourth_elements, sickness="蜂腰")
        elif self.蜂腰 == "二四同濁":
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements_qing_zhuo, fourth_elements_qing_zhuo, True, False, False, "濁", "蜂腰")
        elif self.蜂腰 == "二四同濁調":
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements, fourth_elements, sickness="蜂腰")
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements_qing_zhuo, fourth_elements_qing_zhuo, True, False, False, "濁", "蜂腰")
        elif self.蜂腰 == "中濁四清":
            get_all_list = self.__feng_yao_compare_and_update(qing_zhuo_list, get_all_list, "濁", "蜂腰")
        else:
            get_all_list = self.__feng_yao_compare_and_update(qing_zhuo_list, get_all_list, "濁", "蜂腰")

        '''鶴膝'''

        if self.鹤膝 == "五與十五同調":
            if sheng_diao_list[4] == sheng_diao_list[14]:
                _0 = get_all_list[4]
                _5 = get_all_list[14]
                get_all_list[4] = f"{_0}-鶴膝"
                get_all_list[14] = f"{_5}-鶴膝"
        elif self.鹤膝 == "二四同清":
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements_qing_zhuo, fourth_elements_qing_zhuo, True, False, False, "清", "鶴膝")
        elif self.鹤膝 == "中清四濁":
            get_all_list = self.__feng_yao_compare_and_update(qing_zhuo_list, get_all_list, "清", "鶴膝")
        else:
            get_all_list = self.__feng_yao_compare_and_update(qing_zhuo_list, get_all_list, "清", "鶴膝")

        '''大韻'''

        # 提取每十个元素的第一个元素，并保留索引
        first_elements_yun = [(yun_list[i], i) for i in range(0, len(yun_list), 10)]

        # 获取每十个元素的第十个元素，并保留索引
        tenth_elements_yun = [(yun_list[i], i) for i in range(9, len(yun_list), 10)]

        get_all_list = self.__rhyme_or_feng_yao(get_all_list, first_elements_yun, tenth_elements_yun, False, True, sickness="大韻")

        '''小韻'''

        if self.小韵 == "字韻部不同":
            get_all_list = self.__xiao_yun_compare_and_update(yun_list, get_all_list)
        elif self.小韵 == "上下字韻部不同":
            start_with_0_extract_5_skip_5 = self.__extract_5_skip_5(yun_list)
            start_with_5_extract_5_skip_5 = self.__extract_5_skip_5(yun_list, 5)
            pprint(start_with_0_extract_5_skip_5)
            pprint(start_with_5_extract_5_skip_5)
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, start_with_0_extract_5_skip_5, start_with_5_extract_5_skip_5, xiao_yun=True, sickness="小韻")
        else:#上四下一非同韻部
            # 提取每十个元素的第四个元素，并保留索引
            fourth_elements_yun = [(yun_list[i], i) for i in range(3, len(yun_list), 10)]

            # 提取每十个元素的第六个元素，并保留索引
            sixth_elements_yun = [(yun_list[i], i) for i in range(5, len(yun_list), 10)]

            get_all_list = self.__rhyme_or_feng_yao(get_all_list, fourth_elements_yun, sixth_elements_yun, xiao_yun=True, sickness="小韻")


        '''旁紐'''

        if self.旁纽 == "韻母檢查-全聯":
            start_with_0_extract_5_skip_5 = self.__extract_5_skip_5(yun_list)
            start_with_5_extract_5_skip_5 = self.__extract_5_skip_5(yun_list, 5)
            pprint(start_with_0_extract_5_skip_5)
            pprint(start_with_5_extract_5_skip_5)
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, start_with_0_extract_5_skip_5,
                                                    start_with_5_extract_5_skip_5, xiao_yun=True, sickness="旁紐")
        elif self.旁纽 == "韻母檢查-半聯":
            get_all_list = self.__xiao_yun_compare_and_update(yun_list, get_all_list, '旁紐', 5)
        elif self.旁纽 == "主元音韻尾檢查-半聯" or "韻部檢查-半聯":
            get_all_list = self.__xiao_yun_compare_and_update(main_vowel_rhyme_tail_list, get_all_list, '旁紐', 5)
        elif self.旁纽 == "主元音韻尾檢查-全聯" or "韻部檢查-全聯":
            start_with_0_extract_5_skip_5 = self.__extract_5_skip_5(main_vowel_rhyme_tail_list)
            start_with_5_extract_5_skip_5 = self.__extract_5_skip_5(main_vowel_rhyme_tail_list, 5)
            get_all_list = self.__rhyme_or_feng_yao(get_all_list, start_with_0_extract_5_skip_5,
                                                    start_with_5_extract_5_skip_5, xiao_yun=True, sickness="旁紐")

        '''正紐'''
        start_with_0_extract_5_skip_5 = self.__extract_5_skip_5(shengmu_yuanyin_yunwei_list)
        start_with_5_extract_5_skip_5 = self.__extract_5_skip_5(shengmu_yuanyin_yunwei_list, 5)

        get_all_list = self.__rhyme_or_feng_yao(get_all_list, [item for sublist in start_with_0_extract_5_skip_5 for item in sublist],
                                                [item for sublist in start_with_5_extract_5_skip_5 for item in sublist], xiao_yun=True, sickness="正紐")

        return get_all_list

    @staticmethod#F
    def __rhyme_or_shang_wei(elements, get_all_list, group_elements_num, segmentation_num, sickness="上尾"):
        for i in range(0, len(elements) - 1, 2):
            if elements[i] == elements[i + 1] and elements[i] is not None:
                value = elements[i]
                for j in range(i, len(elements)):
                    if elements[j] == value:
                        idx = j * group_elements_num + segmentation_num
                        _item = get_all_list[idx]
                        get_all_list[idx] = f"{_item}-{sickness}"
        return get_all_list

    @staticmethod#F
    def __rhyme_or_feng_yao(get_all_list, elements_0, elements_1, qing_zhuo=False, rhyme=False, xiao_yun=False,
                            qing_zhuo_word="濁", sickness="蜂腰"):
        for i in range(min(len(elements_0), len(elements_1))):
            first_value, first_index = elements_0[i]
            fourth_value, fourth_index = elements_1[i]

            if first_value is None or fourth_value is None:
                continue  # 新增的跳过逻辑

            if qing_zhuo:  # 清濁匹配
                if first_value == qing_zhuo_word and fourth_value == qing_zhuo_word:
                    print(f"匹配: {first_value} 和 {fourth_value}")
                    get_all_list[first_index] = f"{get_all_list[first_index]}-{sickness}"
                    get_all_list[fourth_index] = f"{get_all_list[fourth_index]}-{sickness}"
            else:  # 聲調匹配或押韻匹配
                if rhyme:
                    if first_value != fourth_value:
                        print(f"不匹配: {first_value} 和 {fourth_value}")
                        get_all_list[first_index] = f"{get_all_list[first_index]}-{sickness}"
                        get_all_list[fourth_index] = f"{get_all_list[fourth_index]}-{sickness}"
                else:
                    if first_value == fourth_value:
                        print(f"匹配: {first_value} 和 {fourth_value}")
                        if xiao_yun:
                            get_all_list[first_index] = f"{get_all_list[first_index]}-{first_value}{sickness}"
                            get_all_list[fourth_index] = f"{get_all_list[fourth_index]}-{fourth_value}{sickness}"
                        else:
                            get_all_list[first_index] = f"{get_all_list[first_index]}-{sickness}"
                            get_all_list[fourth_index] = f"{get_all_list[fourth_index]}-{sickness}"
        return get_all_list

    @staticmethod
    def __1to5_(data):
        result = []
        for i in range(0, len(data), 5):
            # 提取每5个元素为一组
            group = data[i:i + 5]
            # 提取第1、2、3、4、5个元素
            extracted = [(group[j], i + j) for j in range(5) if j < len(group)]
            # 将每5个元素分成一个列表
            result.append(extracted)
        return result

    @staticmethod
    def __extract_5_skip_5(data, start_index=0):
        """
        提取元素的函数，可从指定索引开始，每次提取5个元素，然后跳过5个元素。

        :param data: 输入的数据列表
        :param start_index: 开始提取的索引（默认从0开始）
        :return: 处理后的结果列表
        """
        result = []
        for i in range(start_index, len(data), 10):  # 从指定索引开始，每次跳过5个元素，再提取5个
            # 提取从i开始的5个元素
            group = data[i:i + 5]
            # 提取第1、2、3、4、5个元素
            extracted = [(group[j], i + j) for j in range(5) if j < len(group)]
            # 将每5个元素分成一个列表
            result.append(extracted)
        return result

    @staticmethod
    def __1to10_(data):
        result = []
        for i in range(0, len(data), 10):  # 每次取10个元素
            # 提取每10个元素为一组
            group = data[i:i + 10]
            # 提取第1到10个元素
            extracted = [(group[j], i + j) for j in range(10) if j < len(group)]
            # 将每10个元素分成一个列表
            result.append(extracted)
        return result

    @staticmethod#F
    def __xiao_yun_compare_and_update(yun_list, get_all_list, sickness="小韻", _1towhat_=10):
        # 提取并分组
        if _1towhat_ == 10:
            grouped_yun = YongMingTi.__1to10_(yun_list)
        elif _1towhat_ == 5:
            grouped_yun = YongMingTi.__1to5_(yun_list)
        else:
            grouped_yun = YongMingTi.__1to10_(yun_list)

        for group in grouped_yun:
            element_indices = {}
            for element, original_index in group:
                # 新增：跳过 None 元素
                if element is None:
                    continue  # 直接跳过当前元素的后续处理

                if element in element_indices:
                    # 如果该元素已出现过，检查并更新对应位置
                    previous_index = element_indices[element]
                    suffix = f"-{element}{sickness}"
                    # 确保不重复添加后缀
                    if suffix not in get_all_list[previous_index]:
                        get_all_list[previous_index] += suffix
                    if suffix not in get_all_list[original_index]:
                        get_all_list[original_index] += suffix
                else:
                    # 记录非 None 元素及其索引
                    element_indices[element] = original_index

        return get_all_list

    @staticmethod#F
    def __feng_yao_compare_and_update(qing_zhuo_list, get_all_list, qing_zhuo_word="濁", sickness="蜂腰"):
        grouped_sheng_diao = YongMingTi.__1to5_(qing_zhuo_list)
        qing_zhuo_dict = {"清": "濁", "濁": "清"}

        for group_idx, group in enumerate(grouped_sheng_diao):
            # 检查 group 的长度和元素是否为 None
            if len(group) >= 5:
                # 提取需要检查的值（索引 0、1、3、4 的第一个元素）
                check_values = [
                    group[0][0], group[1][0],
                    group[3][0], group[4][0]
                ]

                third_value = group[2][0]  # 索引2的第一个元素

                # 关键条件判断（包含 None 过滤）
                if (
                        all(v is not None for v in check_values)  # 检查四个值均非 None
                        and (check_values[0] == check_values[1] == check_values[2] == check_values[3] == qing_zhuo_dict[
                    qing_zhuo_word])  # 四个值相等且等于目标值
                        and (third_value is not None)  # 第三个值非 None
                        and (third_value == qing_zhuo_word)  # 第三个值等于目标值
                ):
                # 更新 get_all_list
                    for idx in [0, 1, 3, 4]:
                        get_all_list[group[idx][1]] += f"-{sickness}{qing_zhuo_dict[qing_zhuo_word]}"
                    get_all_list[group[2][1]] += f"-{sickness}{qing_zhuo_word}"

        return get_all_list