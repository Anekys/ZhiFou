# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 21:39
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: word_tools.py
# @Software: PyCharm
import jieba
import jieba.analyse
from collections import Counter
from wordcloud import WordCloud


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
        hashmap.setdefault("name", item[0])
        hashmap.setdefault("value", item[1])
        result.append(hashmap)
    return result


def generate_png(words):
    word_img = WordCloud(scale=3, background_color="white",
                         font_path="SIMYOU.TTF",
                         ).generate(words)
    word_img.to_file("./static/images/wordcloud.png")


def cut_words(content):
    tags = jieba.analyse.extract_tags(content, topK=100)
    words = jieba.cut_for_search(content)
    str_list = []
    for word in words:
        str_list.append(word)
    return " ".join(str_list)


if __name__ == '__main__':
    text = "从前有座山，山里有座庙，庙里有个老和尚，老和尚给小和尚讲故事"
    res = cut_words(text)
    print(res)
