# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 21:39
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: get_word_count.py
# @Software: PyCharm
import jieba
import jieba.analyse
from collections import Counter


def count_from_str(content, top_limit=0):
    """
    :param content: 要被分词的文本数据
    :param top_limit: 要返回排名前多少的数据
    :return: 适用于Echarts的数据格式,直接以JSON返回前端即可
    """
    if top_limit <= 0:
        top_limit = 10
    tags = jieba.analyse.extract_tags(content, topK=100)
    words = jieba.cut_for_search(content)
    counter = Counter()
    for word in words:
        if word in tags:
            counter[word] += 1
    result = []
    for item in counter.most_common(top_limit):
        hashmap = {}
        hashmap.setdefault("name",item[0])
        hashmap.setdefault("value",item[1])
        result.append(hashmap)
    return result

if __name__ == '__main__':
    text = "从其那有座山，山里有座庙，庙里有个老和尚，老和尚给小和尚讲故事"
    res = count_from_str(text)
    print(res)