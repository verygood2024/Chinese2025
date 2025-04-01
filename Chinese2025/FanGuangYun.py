from .繁體廣韻搜索 import 繁體廣韻搜索

class FanGuangYun(繁體廣韻搜索):
    方法映射 = {
    "yun_bu": "返回韻部",
    "sheng_niu": "返回聲紐", 
    "sheng_diao": "返回聲調",
    "ping_ze": "返回平仄",
    "fan_qie": "返回反切",
    "fan_qie_shang": "返回反切上字",
    "fan_qie_xia": "返回反切下字",
    "kai_he": "返回開合",
    "deng_di": "返回等第",
    "nie": "返回攝",
    "qing_zhuo": "返回清濁",
    "yin_yun":"音韻地位",
    "zi_dian":"返回表字典",
    "shi_yi":"釋義",
    "bu_chong_shi_yi":"補充釋義"
    }


    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")