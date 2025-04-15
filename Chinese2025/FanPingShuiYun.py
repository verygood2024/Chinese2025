from .繁體平水韻搜索 import 繁體平水韻搜索

class FanPingShuiYun(繁體平水韻搜索):
    方法映射 = {
        "yun_bu": "返回韻部",
        "yun_mu": '返回韻目',
        "sheng_diao": "返回聲調",
        "ping_ze": "返回平仄",
        "zi_dian": "返回表字典",
    }

    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")