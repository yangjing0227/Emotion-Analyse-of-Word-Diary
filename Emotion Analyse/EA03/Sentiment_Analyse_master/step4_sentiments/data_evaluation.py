#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:59:46 2018
@author: Ming JIN
"""
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 修正字体路径，使用原始字符串r''来避免转义问题
# 请确保你的电脑上存在此路径和字体文件
font_path = r'D:\Weibo-Analyst-master\Weibo-Analyst-master\step3_word_cloud\Songti.ttc'
font = FontProperties(fname=font_path, size=14)

pos_count = 0
neg_count = 0

# 使用 with 语句，并修正文件路径和编码
file_path = "D:/Weibo-Analyst-master/Weibo-Analyst-master/step4_sentiments/model_evaluation/data_keywords.dat"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_data in f:
            comment = line_data.strip()

            # 检查空行，如果为空则跳过
            if not comment:
                continue

            s = SnowNLP(comment)
            rates = s.sentiments

            if (rates >= 0.5):
                pos_count += 1
            elif (rates < 0.5):
                neg_count += 1

except FileNotFoundError:
    print(f"错误: 文件 '{file_path}' 未找到。请检查路径。")
    # 如果文件不存在，退出程序
    exit()
except UnicodeDecodeError:
    print(f"错误: 无法用 'utf-8' 编码读取文件 '{file_path}'，请检查文件编码。")
    exit()

# 检查是否有数据，避免除以零错误
total_count = pos_count + neg_count
if total_count == 0:
    print("错误: 文件中没有可用于情感分析的有效数据。")
else:
    # 定义饼图的标签
    labels = '积极情绪\n(占比)', '消极情绪\n(占比)'
    # 计算百分比
    fracs = [pos_count, neg_count]
    explode = [0.1, 0]  # 突出积极情绪部分

    plt.axes(aspect=1)
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6,
            textprops={'fontproperties': font})  # 应用中文字体

    plt.title("荆楚名校笔记情感分析饼图", fontproperties=font, fontsize=20)
    plt.savefig("emotions_pie_chart.jpg", dpi=360)
    plt.show()

