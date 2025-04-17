from .FanYongMingTi import FanYongMingTi

class 繁體永明躰檢測(FanYongMingTi):
    方法映射 = {
        "檢測":"detection",
        "已有檢測":"list_detection"
    }

    def __getattr__(self, name):
        if name in self.方法映射:
            return getattr(self, self.方法映射[name])
        raise AttributeError(f"没有方法 {name}")