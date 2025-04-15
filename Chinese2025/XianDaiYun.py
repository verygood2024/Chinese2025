from .现代韵书搜索 import 现代韵书搜索

class XianDaiYun(现代韵书搜索):
    方法映射 = {
        "sheng_diao":"返回声调",
        "yun_bu":"返回韵部",
        "ping_ze":"平仄"
    }

    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")