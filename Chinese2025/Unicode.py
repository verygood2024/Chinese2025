import unicodedata

def is_chinese(ch):
    """判断一个字符是否属于统一汉字：
       包括基本汉字及扩展 A、B、C、D、E、F、G、H 和 I 区。
    """
    code = ord(ch)
    return (
        0x4E00 <= code <= 0x9FFF or   # 基本汉字
        0x3400 <= code <= 0x4DBF or   # 扩展 A 区
        0x20000 <= code <= 0x2A6D6 or # 扩展 B 区
        0x2A700 <= code <= 0x2B734 or # 扩展 C 区（Unicode 5.2）
        0x2B740 <= code <= 0x2B81F or # 扩展 D 区
        0x2B820 <= code <= 0x2CEAF or # 扩展 E 区
        0x2CEB0 <= code <= 0x2EBEF or # 扩展 F 区
        0x30000 <= code <= 0x3134A or # 扩展 G 区（Unicode 13.0）
        0x31350 <= code <= 0x323AF or # 扩展 H 区（Unicode 15.0）
        0x2EBF0 <= code <= 0x2EE5D    # 扩展 I 区（Unicode 15.1）
    )

def valid_text(text):
    """
    检查文本中所有字符是否都为下列三类之一：
      1. 统一汉字（包含基本汉字及所有扩展区）
      2. 标点符号（通过 unicodedata.category 判断，类别以 'P' 开头）
      3. 空白字符（如空格、换行、制表符等，通过 ch.isspace() 判断）
    """
    for ch in text:
        if is_chinese(ch):
            continue
        if unicodedata.category(ch).startswith('P'):
            continue
        if ch.isspace():
            continue
        # 如果字符既不是统一汉字、也不是标点或空白，则返回 False
        return False
    return True

def extract_chinese_characters(text):
    """
    从文本中提取所有统一汉字（包含基本汉字及各扩展区）。
    返回一个列表，每个元素为一个中文字符。
    """
    return [ch for ch in text if is_chinese(ch)]

def extract_punctuation(text):
    """
    从文本中提取所有 Unicode 定义的标点符号。
    根据 unicodedata.category 判断，类别以 'P' 开头的视为标点符号。
    返回一个列表，每个元素为一个标点字符。
    """
    return [ch for ch in text if unicodedata.category(ch).startswith('P')]
