# -*- coding: utf-8 -*-
# @Time    : 2022/9/3 15:48
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: sort.py
# @Software: PyCharm

def sort_answer_by_time_desc(answer_list) -> None:
    pointer_a, pointer_b = 0, len(answer_list) - 1
    while pointer_a < pointer_b:
        # 交换两数
        answer_list[pointer_a], answer_list[pointer_b] = answer_list[pointer_b], answer_list[pointer_a]
        pointer_a += 1
        pointer_b -= 1
