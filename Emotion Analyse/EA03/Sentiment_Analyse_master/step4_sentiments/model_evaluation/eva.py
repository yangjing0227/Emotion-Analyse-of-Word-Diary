#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:59:46 2018
@author: Ming JIN
"""
# from snownlp import sentiment
# import numpy as np
from snownlp import SnowNLP

# from snownlp.sentiment import Sentiment

comment = []

array1 = []
array2 = []

count_num = 0

# 使用 with 语句和正确的编码来打开文件
with open("data_full.dat", 'r', encoding='utf-8') as f_in:
    # 每次运行时都清空旧的 eva_result.dat 文件，确保数据准确
    with open("eva_result.dat", "w", encoding='utf-8') as f_out:
        for line_data in f_in:
            comment = line_data.strip()  # 移除行尾的换行符

            # 检查空行
            if not comment:
                continue

            s = SnowNLP(comment)
            rates = s.sentiments

            if (rates >= 0.5):
                eva_label = 1
            else:
                eva_label = -1

            eva = str(eva_label)
            f_out.write(eva)
            f_out.write('\n')

# 同样，使用正确的编码来读取其他文件，并移除每一行的空白字符
with open("eva_label.dat", 'r', encoding='utf-8') as f1:
    for line1 in f1:
        array1.append(line1.strip())

with open("eva_result.dat", 'r', encoding='utf-8') as f2:
    for line2 in f2:
        array2.append(line2.strip())

# 获取两个列表中的最小长度，确保循环不会越界
count_sum = min(len(array1), len(array2))

if count_sum == 0:
    print("错误: 用于评估的文件为空，无法进行比较。")
else:
    # 更改循环范围为动态长度，避免 IndexError
    for i in range(count_sum):
        if (array1[i] == array2[i]):
            count_num += 1

    correct_rate = count_num / count_sum
    print(f"模型的正确率为: {correct_rate}")

