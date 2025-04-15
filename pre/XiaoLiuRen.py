from Error import 输入不合法
import pprint
from datetime import datetime
import dateutil.tz

from lunar_python import Solar, Lunar, LunarMonth
import re
from datetime import timedelta, timezone

THIRTY_EIGHT_ALPHABET={
     '崇':"濁",
     '從':"濁",
     '匣':"濁",
     '疑':"濁",
     '莊':"清",
     '溪':"清",
     '常':"濁",
     '清':"清",
     '以':"濁",
     '精':"清",
     '俟':"濁",
     '影':"清",
     '來':"濁",
     '章':"清",
     '知':"清",
     '澄':"濁",
     '日':"濁",
     '徹':"清",
     '並':"濁",
     '云':"濁",
     '定':"濁",
     '明':"濁",
     '心':"清",
     '滂':"清",
     '見':"清",
     '幫':"清",
     '書':"清",
     '生':"清",
     '曉':"清",
     '端':"清",
     '邪':"濁",
     '初':"清",
     '群':"濁",
     '昌':"清",
     '泥':"濁",
     '船':"濁",
     '娘':"濁",
     '透':"清"
}

YONG_MING_TI_DATA = {
    "使用時代:":2,
    "使用性質:":0,
    "使用作者:":0,
    "使用韻書:":7,
    "使用聲調:":0,
    "蜂腰問題:":4,
    "鶴膝問題:":2,
    "小韻問題:":2,
    "旁紐問題:":4,
    "前等待时:":3.0,
    "中等待时:":3.0,
    "后等待时:":3.0
}

YONG_MING_TI_LIST = [
    ["上古音", "兩漢六朝","中古音"],
    ["構擬","轉寫","推導"],
    ['高本漢', '董同龢', '王力體系', '李方桂', '周法高', '斯塔羅斯金①·上古前期', '斯塔羅斯金②·上古後期', '斯塔羅斯金③·詩經音', '白一平', '鄭張尚芳', '潘悟雲', '許思萊', '金理新', '白一平-沙加爾', '郭錫良（表稿）', '郭錫良（手冊）', '斯塔羅斯金·西漢', '斯塔羅斯金·東漢', '許思萊·東漢', '高本漢', '王力', '董同龢', '李方桂', '周法高', '陳新雄', '蒲立本·前期', '蒲立本·後期', '斯塔羅斯金·中古', '斯塔羅斯金·前期', '斯塔羅斯金·中期', '斯塔羅斯金·後期', '楊力', '金理新', '許思萊', '白一平-沙加爾', '高本漢', '王力', '張世祿', '嚴學宭', '董同龢', '李榮', '蒲立本', '邵榮芬', '鄭張尚芳', '潘悟雲', '楊劍橋', '麥耘','poem'],
    ['西漢', '東漢', '魏', '晉', '宋北魏後期', '北魏後期北齊', '齊梁陳北周隋',
     '廣韻-小學堂','集韻-小學堂','附釋文互註禮部韻略-小學堂',
     '增修互注禮部韻略-小學堂','中原音韻-小學堂','洪武正韻-小學堂','中州音韻-小學堂',
     "廣韻-基於poem","玉篇-基於poem","平水韻"],
    ["平上去入","平仄"],
    ["二五同調","二四同調","二四同濁","二四同濁調","中濁四清"],
    ["五與十五同調","二四同清","中清四濁"],
    ["字韻部不同","上下字韻部不同","上四下一非同韻部"],
    ["韻部檢查-半聯","主元音韻尾檢查-半聯","韻母檢查-半聯","韻部檢查-全聯","主元音韻尾檢查-全聯","韻母檢查-全聯"]]
#"韻部"
#'西漢', '東漢', '魏', '晉', '宋北魏後期', '北魏後期北齊', '齊梁陳北周隋'
PRE_DATA = {
    "1":"2",
    "2":"2",
    "3":"2",
    "4":"2",
    "5":"2",
}

XLR_DATA = {
"起卦历法": 0,
"起卦时间": 0,
"起卦时区": 0,
"起卦方式": 0,
"时辰问题": 0,
"闰月问题": 0,
"计算吉值": 0,
"三宫定义": 0,
"起卦算法": 0,
"数值问题": 0,
"时刻问题": 0,
"始范围":0,
"末范围":10,
"始范围2":0,
"末范围2":10
}

XLR_DATA_WU_XING = {
"五行输入": 0,
"五行取数": 0,
"阴阳时问题":0,
"单输入问题":0,
"单双数问题":0,
"取数计算":0,
"范围输入":0
}

XLR_DATA_WU_XING_JI_LU = {
"五行记录": 0
}

ZHI_DICT_NUM = {
"子":1,
"丑":2,
"寅":3,
"卯":4,
"辰":5,
"巳":6,
"午":7,
"未":8,
"申":9,
"酉":10,
"戌":11,
"亥":12
}

TIAN_GAN_DICT = {
0:("甲","木","阳"),
1:("甲","木","阳"),
2:("乙","木","阴"),
3:("丙","火","阳"),
4:("丁","火","阴"),
5:("戊","土","阳"),
6:("己","土","阴"),
7:("庚","金","阳"),
8:("辛","金","阴"),
9:("壬","水","阳"),
10:("癸","水","阴")
}

DI_ZHI_DICT = {
1: ("子", "阳", "水", "鼠"),
2: ("丑", "阴", "土", "牛"),
3: ("寅", "阳", "木", "虎"),
4: ("卯", "阴", "木", "兔"),
5: ("辰", "阳", "土", "龙"),
6: ("巳", "阴", "火", "蛇"),
7: ("午", "阳", "火", "马"),
8: ("未", "阴", "土", "羊"),
9: ("申", "阳", "金", "猴"),
10: ("酉", "阴", "金", "鸡"),
11: ("戌", "阳", "土", "狗"),
12: ("亥", "阴", "水", "猪")
}

ZAO_WAN_DI_ZHI_DICT ={
1: ("子", "阴", "水", "鼠"),
2: ("丑", "阴", "土", "牛"),
3: ("寅", "阴", "木", "虎"),
4: ("卯", "阴", "木", "兔"),
5: ("辰", "阴", "土", "龙"),
6: ("巳", "阴", "火", "蛇"),
7: ("午", "阳", "火", "马"),
8: ("未", "阳", "土", "羊"),
9: ("申", "阳", "金", "猴"),
10: ("酉", "阳", "金", "鸡"),
11: ("戌", "阳", "土", "狗"),
12: ("亥", "阳", "水", "猪")
}

WAN_ZAO_DI_ZHI_DICT ={
1: ("子", "阳", "水", "鼠"),
2: ("丑", "阳", "土", "牛"),
3: ("寅", "阳", "木", "虎"),
4: ("卯", "阳", "木", "兔"),
5: ("辰", "阳", "土", "龙"),
6: ("巳", "阳", "火", "蛇"),
7: ("午", "阴", "火", "马"),
8: ("未", "阴", "土", "羊"),
9: ("申", "阴", "金", "猴"),
10: ("酉", "阴", "金", "鸡"),
11: ("戌", "阴", "土", "狗"),
12: ("亥", "阴", "水", "猪")
}

YUE_GAN_DICT = {
"甲":("甲","木","阳"),
"乙":("乙","木","阴"),
"丙":("丙","火","阳"),
"丁":("丁","火","阴"),
"戊":("戊","土","阳"),
"己":("己","土","阴"),
"庚":("庚","金","阳"),
"辛":("辛","金","阴"),
"壬":("壬","水","阳"),
"癸":("癸","水","阴")
}

YUE_ZHI_DICT = {
1:("寅", "阳", "木", "虎"),
2:("卯", "阴", "木", "兔"),
3:("辰", "阳", "土", "龙"),
4:("巳", "阴", "火", "蛇"),
5:("午", "阳", "火", "马"),
6:("未", "阴", "土", "羊"),
7:("申", "阳", "金", "猴"),
8:("酉", "阴", "金", "鸡"),
9:("戌", "阳", "土", "狗"),
10:("亥", "阴", "水", "猪"),
11:("子", "阳", "水", "鼠"),
12:("丑", "阴", "土", "牛")
}

SHI_CHEN_DICT = {
0: ("子", "阳", "水", "鼠"),
1: ("丑", "阴", "土", "牛"),
2: ("丑", "阴", "土", "牛"),
3: ("寅", "阳", "木", "虎"),
4: ("寅", "阳", "木", "虎"),
5: ("卯", "阴", "木", "兔"),
6: ("卯", "阴", "木", "兔"),
7: ("辰", "阳", "土", "龙"),
8: ("辰", "阳", "土", "龙"),
9: ("巳", "阴", "火", "蛇"),
10: ("巳", "阴", "火", "蛇"),
11: ("午", "阳", "火", "马"),
12: ("午", "阳", "火", "马"),
13: ("未", "阴", "土", "羊"),
14: ("未", "阴", "土", "羊"),
15: ("申", "阳", "金", "猴"),
16: ("申", "阳", "金", "猴"),
17: ("酉", "阴", "金", "鸡"),
18: ("酉", "阴", "金", "鸡"),
19: ("戌", "阳", "土", "狗"),
20: ("戌", "阳", "土", "狗"),
21: ("亥", "阴", "水", "猪"),
22: ("亥", "阴", "水", "猪"),
23: ("子", "阳", "水", "鼠"),
24: ("子", "阳", "水", "鼠"),
}

HOU_TIAN_WU_XING = {
    "金": (9, 4),
    "木": (3, 8),
    "水": (1, 6),
    "火": (7, 2),
    "土": (5, 10)
}

XIAN_TIAN_WU_XING = {
    "金":(7,8),
    "木":(1,2),
    "水":(9,10),
    "火":(3,4),
    "土":(5,6)
}

SI_XIANG_WU_XING = {
    "金":9,
    "木":8,
    "水":6,
    "火":7,
    "土":5
}

def utc(时区):
    local_timezone = dateutil.tz.tzlocal()
    now = datetime.now(local_timezone)
    offset = now.strftime('%z')
    formatted_offset = f"UTC{offset[:3]}:{offset[3:]}"
    if (时区 == formatted_offset) or (时区 is None):
        return UTC_TIME[UTC_TIME.index(formatted_offset)]
    elif 时区 != formatted_offset:
        return 时区

class TimeZoneConversionT:
    def __init__(self, current_time, to_utc_offset):
        a = TimeZoneConversionF(current_time, to_utc_offset)
        self.to_zone = a.parse_timezone_offset(to_utc_offset)
        self.converted_time = a.convert_timezone(current_time)

    def get_zone_time(self):
        return self.converted_time

class TimeZoneConversionF:
    def __init__(self, current_time,to_utc_offset):
        self.to_zone = self.parse_timezone_offset(to_utc_offset)
        self.converted_time = self.convert_timezone(current_time)

    @staticmethod
    def parse_timezone_offset(offset_str):
        if not re.match(r'^UTC[+-]\d{2}:\d{2}$', offset_str):
            raise ValueError("Invalid time zone format. Use 'UTC±HH:MM'.")

        sign = 1 if offset_str[3] == '+' else -1
        hours, minutes = map(int, offset_str[4:].split(':'))
        return timezone(timedelta(hours=sign * hours, minutes=sign * minutes))

    def convert_timezone(self, time):
        to_time = time.astimezone(self.to_zone)
        return to_time

def min_ke(converted_time,ke):
    minutr = converted_time % 15
    if minutr == 0:
        if ke == 0:
            minutr = 0
        else:
            minutr = 1
    return minutr

class Calendar:
    def __init__(self, li_fa, shi_chen, run_yue,shi=None,ke=0,function=0,时区=None):
        self.li_fa = li_fa
        self.shi_chen_issue = shi_chen
        self.run_yue = run_yue
        self.utc = utc(时区)
        self.convert_time = datetime.now().astimezone().replace()
        self.shi = shi
        self.ke = ke
        self.function = function

        if self.shi is not None:
            self.converted_time = self.shi
        else:
            a = TimeZoneConversionT(self.convert_time, self.utc)
            self.converted_time = a.get_zone_time()

    def function_selection(self):
        function_selection = {
            0: self.gregorian_calendar,
            1: self.chinese_calendar,
            2: self.taoism_calendar,
        }

        return function_selection[self.li_fa]()

    @staticmethod
    def time_partition(minute_, second, d_):
        if minute_ <= 59 and second <= 59:
            pass
        else:
            d_.next(1)
        return d_

    def gregorian_calendar(self):
        d = Solar.fromDate(self.converted_time)
        a0,a1,a2,a3=SHI_CHEN_DICT[self.converted_time.hour]

        if a0 == "子":
            if self.shi_chen_issue == 0:
                self.converted_time = d.next(1)
            elif self.shi_chen_issue == 1:
                pass
            else:
                self.converted_time = Calendar.time_partition(self.converted_time.minute, self.converted_time.second, d)
        if self.function == 0:
            return self.converted_time.year, self.converted_time.month, self.converted_time.day, SHI_CHEN_DICT[self.converted_time.hour]
        else:
            minutr = min_ke(self.converted_time.minute,self.ke)
            return self.converted_time.hour,minutr,self.converted_time.minute,self.converted_time.minute

    def chinese_calendar(self):
        return ChineseCalendar(self.converted_time, self.shi_chen_issue,self.run_yue,self.ke,self.function).get_lunar_date()

    def taoism_calendar(self):
        if self.function == 0:
            lunar_year, lunar_month, lunar_day, lunar_hour = self.chinese_calendar()
            lunar = Lunar.fromYmd(lunar_year, lunar_month, lunar_day)
            tao = lunar.getTao()
            dao_year = tao.getYear()
            return dao_year, lunar_month, lunar_day, lunar_hour
        else:
            lunar_year,lunar_hour, lunar_ke, lunar_min = self.chinese_calendar()
            return lunar_year,lunar_hour, lunar_ke, lunar_min

class ChineseCalendar:
    def __init__(self, current_time, shi_chen, run_yue,ke_function,function=0):

        self.converted_time = current_time
        self.shi_chen = shi_chen
        self.run_yue = run_yue


        self.d = Lunar.fromDate(self.converted_time)
        self.lunar_year = self.d.getYear()
        self.lunar_month = self.d.getMonth()
        self.lunar_day = self.d.getDay()
        self.lunar_hour = self.d.getHour()
        self.lunar_min = self.d.getMinute()
        self.lunar_sec = self.d.getSecond()
        self.a0 = self.d.getTimeZhi()
        self.run_yue_month = LunarMonth.fromYm(self.lunar_year, self.lunar_month)
        self.judgement_runyue()
        self.judgement_shichen()
        self.function = function
        self.ke_function = ke_function
        self.ke = min_ke(self.lunar_min,self.ke_function)



    def get_lunar_date(self):
        if self.function == 0:
            return self.lunar_year, self.lunar_month, self.lunar_day, self.a0
        else:
            return self.lunar_year,self.lunar_hour,self.ke,self.lunar_min

    def judgement_shichen(self):
        if self.a0 == "子":
            if self.shi_chen == 0:
                self.converted_time = self.d.next(1)
                self.lunar_year = self.converted_time.getYear()
                self.lunar_month = self.converted_time.getMonth()
                self.lunar_day = self.converted_time.getDay()
            elif self.shi_chen == 1:
                pass
            else:
                self.converted_time = Calendar.time_partition(self.converted_time.minute, self.converted_time.second, self.d)
                self.lunar_year = self.converted_time.getYear()
                self.lunar_month = self.converted_time.getMonth()
                self.lunar_day = self.converted_time.getDay()

    def judgement_runyue(self):
        if self.run_yue_month.isLeap():
            if self.run_yue == 0:
                pass
            elif self.run_yue == 1:
                f = self.run_yue_month.getDayCount()
                self.run_yue_month.next(1)
                t = self.run_yue_month.getDayCount()

                if f == t:
                    self.lunar_year = self.run_yue_month.getYear()
                    self.lunar_month = self.run_yue_month.getMonth()
                else:
                    if f == 30:
                        self.lunar_year = self.run_yue_month.getYear()
                        self.lunar_month = self.run_yue_month.getMonth()
                        self.lunar_day = 1
                    else:
                        self.lunar_year = self.run_yue_month.getYear()
                        self.lunar_month = self.run_yue_month.getMonth()

历法字典 = {
    "新历":0,
    "农历":1,
    "道历":2,
}

时间字典 = {
    "时区":0,
    "平太阳时":1,
    "真太阳时":2
}

UTC_TIME = [
"UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:00", "UTC-09:30", "UTC-08:00", "UTC-07:00",
"UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC-03:00", "UTC-02:00", "UTC-01:00", "UTC+00:00",
"UTC-00:00", "UTC+01:00", "UTC+02:00", "UTC+03:00", "UTC+03:30", "UTC+04:00", "UTC+04:30",
"UTC+05:00", "UTC+05:30", "UTC+05:45", "UTC+06:00", "UTC+06:30", "UTC+07:00", "UTC+08:00",
"UTC+08:45", "UTC+09:00", "UTC+09:30", "UTC+10:00", "UTC+10:30", "UTC+11:00", "UTC+12:00",
"UTC+12:45", "UTC+13:00", "UTC+14:00"
]

算法字典 = {
    "顺首":0,
    "复首":1,
    "0":0,
    "1":1
}

时辰字典 = {
    "子时视明日":0,
    "子时视本日":1,
    "子时中而分界":2,
    "0":0,
    "1":1,
    "2":2
}

闰月字典 = {
    "作本月":0,
    '作下月':1,
    "中而分界":2,
    "0":0,
    "1":1,
    "2":2
}

数值字典 = {
    "0取10":0,
    "0取0":1,
    "0": 0,
    "1": 1,
}

时刻字典 = {
    "0刻取0刻":0,
    "0刻取1刻":1,
    "0": 0,
    "1": 1,
}

class XiaoLiuRen:
    def __init__(self,历法,时间,时区,算法,时辰,闰月,数值,时刻,吉值=True,三宫=False):
        self.历法_str = 历法字典.get(str(历法),False)
        if  self.历法_str is False:
            raise 输入不合法(self.历法_str, pprint.pformat(sorted(历法字典), compact=True))

        self.时间_str = 时间字典.get(str(时间), False)
        if self.时间_str is False:
            raise 输入不合法(self.时间_str, pprint.pformat(sorted(时间字典), compact=True))

        if (str(时区) not in UTC_TIME) or (时区 is None):
            raise 输入不合法(时区, pprint.pformat(sorted(UTC_TIME), compact=True))

        self.算法_str = 算法字典.get(算法, False)
        if self.算法_str is False:
            raise 输入不合法(self.算法_str, pprint.pformat(sorted(算法字典), compact=True))

        self.时辰_str = 时辰字典.get(时辰, False)
        if self.时辰_str is False:
            raise 输入不合法(self.时辰_str, pprint.pformat(sorted(时辰字典), compact=True))

        self.闰月_str = 闰月字典.get(str(闰月), False)
        if self.闰月_str is False:
            raise 输入不合法(self.闰月_str, pprint.pformat(sorted(闰月字典), compact=True))

        self.数值_str = 数值字典.get(str(数值), False)
        if self.数值_str is False:
            raise 输入不合法(self.数值_str, pprint.pformat(sorted(数值字典), compact=True))

        self.时刻_str = 时刻字典.get(str(时刻), False)
        if self.时刻_str is False:
            raise 输入不合法(self.时刻_str, pprint.pformat(sorted(时刻字典), compact=True))

        if 三宫 is True:
            raise 输入不合法(三宫, "三宫还不支持True")

        self.吉值 = 吉值

    def ri_yue_shi(self):
        pass

    def __闰月问题(self):
