from .注释 import 注释

class ZhuShi(注释):
    方法映射 = {
        "gu_ti":"古体",
        "yun_bu":"韵部",
        "yun_mu":"韵目",
        "sheng_diao":"声调",
        "ping_ze":"平仄"
    }

    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")