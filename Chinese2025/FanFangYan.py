from .繁體方言搜索 import 繁體方言搜索
class FanFangYan(繁體方言搜索):
    方法映射 = {
    "diao_zhi": "返回調值",
    "diao_lei": "返回調類",
    "fa_yin": "返回發音",
    "sheng_mu": "返回聲母",
    "yun_mu": "返回韻母",
    }


    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")