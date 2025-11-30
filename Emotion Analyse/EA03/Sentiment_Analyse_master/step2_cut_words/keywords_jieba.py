#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:51:48 2017
@author: Ming JIN
"""
from jieba import analyse

# 提取关键词的函数
tfidf = analyse.extract_tags

# 使用 'utf-8' 编码打开文件
# 使用 with 语句是更好的实践，它能确保文件在使用完毕后自动关闭
with open("data_full.dat", 'r', encoding='utf-8') as f_in:
    for line in f_in:
        text = line.strip()  # 移除行首尾的空格和换行符

        # 检查行是否为空，如果为空则跳过
        if not text:
            continue

        # 提取关键词，移除 'allowPOS' 参数以避免 TypeError
        # tfidf 默认会提取名词、动词等，满足大部分需求
        keywords = tfidf(text)

        # 将关键词列表转换为字符串
        result = " ".join(keywords)

        # 以追加模式（"a+"）打开文件，确保每次都写入新行
        # 同样，使用 with 语句
        with open("data_keywords.dat", "a+", encoding='utf-8') as f_out:
            f_out.write(result)
            f_out.write('\n')

print("Keywords Extraction Done!")
