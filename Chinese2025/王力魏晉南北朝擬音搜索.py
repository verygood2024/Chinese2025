import warnings
import re

from 查询 import 查询
from 繁體廣韻搜索 import 繁體廣韻搜索

class 中古擬音搜索:
    def __init__(self):
        pass

    @staticmethod
    def __獲取音韻地位(list_a):
        result = {}

        for a in list_a:
            result[a] = {}
            b = 繁體廣韻搜索("nk2028").返回表字典(a)
            total = int(b["总行数"])
            data_list = b["数据"]

            for i in range(total):
                e = data_list[i]
                if "字頭" in e:
                    del e["字頭"]  # 删除"字頭"键

                f = e["音韻地位"]  # 音韻地位
                擬音查詢結果 = 查询().单列查询("王力魏晉南北朝音韻地位", "wangli_js", "音韻地位", f)

                # 提取拟音字符串，如果查询结果不为空，则取第一个元组的第一个元素，否则设为空字符串
                擬音 = 擬音查詢結果[0][0] if 擬音查詢結果 else ""

                e["王力擬音"] = 擬音  # 直接存字符串
                result[a][f] = e  # 直接赋值

        return result

    @staticmethod
    def __構造擬音釋義列表(獲取音韻地位返回的字典):
        擬音釋義字典 = {}

        for 字頭, 音韻項 in 獲取音韻地位返回的字典.items():
            擬音釋義字典[字頭] = []  # 初始化列表

            for 音韻地位, 詳細數據 in 音韻項.items():
                擬音 = 詳細數據["王力擬音"]
                釋義 = 詳細數據["廣韻釋義"]
                補充釋義 = 詳細數據["釋義補充"]

                # 如果釋義或補充釋義是null，則設為None
                if 釋義 is None:
                    釋義 = None
                if 補充釋義 is None:
                    補充釋義 = None

                # 添加 [拟音, 释义, 补充释义] 到列表
                擬音釋義字典[字頭].append([擬音, 釋義, 補充釋義])

        return 擬音釋義字典

    @staticmethod
    def 返回擬音(字头):
        return 中古擬音搜索.__構造擬音釋義列表(中古擬音搜索.__獲取音韻地位(list(字头))) if re.match(r'^[\u4e00-\u9fa5]+$', 字头) else warnings.warn("只允许输入汉字.", UserWarning)
