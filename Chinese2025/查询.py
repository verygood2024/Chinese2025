import os
import sqlite3
import sys
import warnings
import json

class 查询:
    @staticmethod
    def 单列查询(需要查询的表名,需要查询的列名,以此列查询,输入内容):
        try:
            conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reconstructions_list.sqlite"), check_same_thread=False)
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
    def 多列查询(需要查询的表名, 以此列查询, 输入内容, pretty=False):
        try:
            conn = sqlite3.connect(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "reconstructions_list.sqlite"),
                check_same_thread=False
            )
            cursor = conn.cursor()

            # 获取表的所有列名
            cursor.execute(f"PRAGMA table_info({需要查询的表名})")
            列名列表 = [row[1] for row in cursor.fetchall()]
            if not 列名列表:
                cursor.close()
                conn.close()
                result = {"总行数": 0, "数据": []}
            else:
                # 使用传入的列作为查询条件
                cursor.execute(f"SELECT * FROM {需要查询的表名} WHERE {以此列查询} = ?", (输入内容,))
                结果列表 = cursor.fetchall()
                cursor.close()
                conn.close()

                # 每一行转换为一个字典
                数据列表 = [dict(zip(列名列表, 行数据)) for 行数据 in 结果列表]
                result = {
                    "总行数": len(数据列表),
                    "数据": 数据列表
                }

            # 如果需要格式化输出，则返回格式化后的 JSON 字符串
            if pretty:
                return json.dumps(result, ensure_ascii=False, indent=4)
            else:
                return result
        except Exception as e:
            warnings.warn(f"数据库连接失败: {e}", SyntaxWarning)
            sys.exit()

    @staticmethod
    def 查找表名(序号):
        try:
            conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reconstructions_list.sqlite"), check_same_thread=False)
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
