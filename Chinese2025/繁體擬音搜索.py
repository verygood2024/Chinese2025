from pprint import pprint, pformat
import sys
import warnings
import re

from .Error import 输入不合法
from .查询 import 查询
from .繁體廣韻搜索 import 繁體廣韻搜索

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


class 繁體擬音搜索:
    def __init__(self, 源="王力汉语语音史魏晋"):
        self.列名 = 列字典.get(str(源))
        if self.列名 is None:
            raise 输入不合法(源, pformat(sorted(列字典), compact=True))
        self.廣韻搜索器 = 繁體廣韻搜索("nk2028")  # 复用实例
        self.擬音緩存 = {}  # 新增音韵地位缓存

    def __獲取音韻地位(self, list_a):
        """带缓存的音韵地位处理"""
        result = {}
        for 字頭 in list_a:
            原始數據 = self.廣韻搜索器.返回表字典(字頭)
            result[字頭] = {}

            for entry in 原始數據["数据"]:
                音韻地位 = entry["音韻地位"]

                # 缓存检查逻辑
                if 音韻地位 not in self.擬音緩存:
                    擬音結果 = 查询.单列查询(
                        "基礎擬音",
                        self.列名,
                        "音韻地位",
                        音韻地位
                    )
                    self.擬音緩存[音韻地位] = 擬音結果[0][0] if 擬音結果 else ""

                # 构建处理项
                處理项 = {
                    k: v
                    for k, v in entry.items()
                    if k != "字頭"
                }
                處理项.update({
                    "擬音": [
                        self.擬音緩存[音韻地位],
                        音韻地位[-1] if 音韻地位 else ""
                    ]
                })

                result[字頭][音韻地位] = 處理项
        return result

    @staticmethod
    def __構造擬音釋義列表(音韻數據):
        """结构转换优化"""
        return {
            字頭: [
                [  # 结构化结果列表
                    項["擬音"][0],
                    項["擬音"][1],
                    項["釋義"],
                    項["釋義補充"],
                    音韻地位
                ]
                for 音韻地位, 項 in 數據.items()
            ]
            for 字頭, 數據 in 音韻數據.items()
        }

    def 返回擬音(self,字头):
        if re.match(r'^[\u4e00-\u9fa5]+$', 字头):
            return 繁體擬音搜索.__構造擬音釋義列表(self.__獲取音韻地位(list(字头)))
        else:
            raise 输入不合法(字头, 提示="只允许输入汉字.")
        #return 繁體擬音搜索.__構造擬音釋義列表(self.__獲取音韻地位(list(字头))) if re.match(r'^[\u4e00-\u9fa5]+$', 字头) else warnings.warn("只允许输入汉字.", UserWarning)
