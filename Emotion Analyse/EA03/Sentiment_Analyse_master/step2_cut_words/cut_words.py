#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:51:48 2017
@author: Ming JIN
"""
import jieba
import sys
import pymysql


# 修正后的词典加载函数，能够安全处理各种格式不正确的行。
def load_dicts_safely():
    """
    安全地加载用户词典文件，并处理格式不正确的行。
    """
    dict_files = [
        "SogouLabDic.txt",
        "dict_baidu_utf8.txt",
        "dict_pangu.txt",
        "dict_sougou_utf8.txt",
        "dict_tencent_utf8.txt",
        "my_dict.txt"
    ]
    for file_path in dict_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()

                    if len(parts) >= 2:
                        word = parts[0]
                        freq_str = parts[1]

                        try:
                            freq = int(freq_str)
                            tag = parts[2] if len(parts) > 2 else None
                            jieba.add_word(word, freq=freq, tag=tag)

                        except ValueError:
                            print(f"警告: 文件 '{file_path}' 中存在格式不正确的行（词频非数字），已跳过: {line.strip()}")

                   # else:
                       # if line.strip():
                            #print(f"警告: 文件 '{file_path}' 中存在格式不正确的行（字段数量不足），已跳过: {line.strip()}")
        except FileNotFoundError:
            print(f"警告: 用户词典文件 '{file_path}' 未找到。")
        except Exception as e:
            print(f"处理文件 '{file_path}' 时发生未知错误: {e}")


load_dicts_safely()

# 加载停用词
try:
    with open('Stopword.txt', 'r', encoding='utf-8') as f:
        stopwords = {line.rstrip() for line in f}
except FileNotFoundError:
    print("警告: Stopword.txt 未找到。将不使用停用词。")
    stopwords = set()


def get_data_from_single_table():
    """
    连接数据库，从 MY_SENTIMENT_TABLE 表获取数据，进行分词并写入文件。
    """
    print("连接MySql数据库...")

    db = None
    try:
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Yj12345688.',
            db='MY_SENANA',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()

        table_name = "MY_SENTIMENT_TABLE"
        print(f"正在解析表 '{table_name}' 的数据...")

        # 注意：现在我们从 'content' 列获取数据
        sql_get_comments = f"SELECT content FROM {table_name} WHERE content IS NOT NULL"
        cursor.execute(sql_get_comments)

        all_content = cursor.fetchall()

        if not all_content:
            print(f"警告: 表 '{table_name}' 中没有内容，跳过处理。")
            return

        # 使用 'w' 模式清空并写入文件，避免多次运行时重复追加
        with open("data_full.dat", "w", encoding='utf-8') as fo:
            for row in all_content:
                text_content = row['content']

                if not isinstance(text_content, str) or not text_content.strip():
                    continue

                seg = jieba.cut(text_content)

                result_words = [word for word in seg if word.strip() and word not in stopwords]

                fo.write(" ".join(result_words))
                fo.write('\n')

    except pymysql.MySQLError as e:
        print(f"数据库操作失败: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        if db:
            db.close()

    print("解析完成!")


if __name__ == '__main__':
    print("进程开始...")
    get_data_from_single_table()
    print("Done!")
