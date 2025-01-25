import sqlite3
import sys
import warnings

class 查询:
    @staticmethod
    def 单列查询(需要查询的表名,需要查询的列名,以此列查询,输入内容):
        try:
            conn = sqlite3.connect("reconstructions_list.sqlite", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f"SELECT {需要查询的列名} FROM {需要查询的表名} WHERE {以此列查询} = ?", (输入内容,))
            返回值 = cursor.fetchall()

            if not 返回值:
                cursor.close()
                conn.close()
                return [None]

            cursor.close()
            conn.close()
            return 返回值
        except Exception as e:
            warnings.warn(f"数据库连接失败: {e}", SyntaxWarning)
            sys.exit()

    @staticmethod
    def 查找表名(序号):
        try:
            conn = sqlite3.connect("reconstructions_list.sqlite", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            cursor.close()
            conn.close()
            for table in tables:
                if f"_{序号}_" in table[0]:
                    return table[0]
            warnings.warn(f"没有此表", SyntaxWarning)
            sys.exit()
        except Exception as e:
            warnings.warn(f"数据库连接失败: {e}", SyntaxWarning)
            sys.exit()
