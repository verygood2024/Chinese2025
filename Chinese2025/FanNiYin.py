from .繁體擬音搜索 import 繁體擬音搜索

class FanNiYin(繁體擬音搜索):
    方法映射 = {
        "ni_yin":"返回擬音"
    }

    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")