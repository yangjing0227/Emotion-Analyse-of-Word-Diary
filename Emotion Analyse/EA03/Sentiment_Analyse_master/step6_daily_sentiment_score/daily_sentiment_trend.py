#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
笔记情感趋势数据生成脚本

作者：基于用户原始 eva.py 脚本的优化版本
功能：
1. 读取包含“日期”和“正文”的 CSV 文件（假设为 my_data_fixed.csv）。
2. 使用 SnowNLP 对每条笔记的“正文”进行情感分析，获取情感得分（0-1）。
3. 按日期聚合，计算每日的平均情感得分。
4. 将每日情感趋势数据保存为新的 CSV 文件，用于绘图。
"""
import pandas as pd
from snownlp import SnowNLP
import numpy as np
import datetime

# --- 配置 ---
INPUT_FILE = "../step7_sentiment_trend_line_chart/my_data_fixed.csv"
OUTPUT_FILE = "daily_sentiment_trend.csv"
DATE_COLUMN = "日期"  # 确保此列名与您的CSV文件中的日期列名一致
TEXT_COLUMN = "正文"  # 确保此列名与您的CSV文件中的正文列名一致


def load_data(file_path):
    """
    加载数据并进行初步清洗。
    """
    print(f"--- 1. 正在加载文件: {file_path} ---")
    try:
        # 尝试以 UTF-8 编码读取文件，通常是中文环境的最佳选择
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # 如果 UTF-8 失败，尝试 GBK 编码（中国大陆常见的另一种编码）
        df = pd.read_csv(file_path, encoding='gbk')

    # 确保日期和正文列存在
    if DATE_COLUMN not in df.columns or TEXT_COLUMN not in df.columns:
        print(f"错误：CSV文件中未找到所需的列 '{DATE_COLUMN}' 或 '{TEXT_COLUMN}'。")
        print("请检查您的CSV文件列名是否正确。当前列名:", df.columns.tolist())
        return None

    # 清洗：移除任何缺失值或空字符串，确保情感分析的文本是有效的
    df = df.dropna(subset=[DATE_COLUMN, TEXT_COLUMN])
    df = df[df[TEXT_COLUMN].str.strip() != '']

    # 将日期列转换为标准的 datetime 对象
    # 假设您的日期格式已经是 YYYY-MM-DD 或 YYYY/MM/DD
    try:
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')
        df = df.dropna(subset=[DATE_COLUMN])  # 移除无法解析的日期
    except Exception as e:
        print(f"日期格式转换失败，请检查 '{DATE_COLUMN}' 列的格式。错误信息: {e}")
        return None

    print(f"成功加载 {len(df)} 条有效数据。")
    return df


def analyze_sentiment(df):
    """
    使用 SnowNLP 对文本进行情感分析。
    """
    print("--- 2. 正在进行情感分析 (SnowNLP) ---")

    # 定义情感分析函数
    def get_sentiment(text):
        if pd.isna(text) or not str(text).strip():
            return np.nan
        try:
            # SnowNLP 的 s.sentiments 返回 0-1 的得分，越接近 1 越积极
            return SnowNLP(str(text)).sentiments
        except Exception as e:
            # 捕获可能的 SnowNLP 内部错误
            print(f"情感分析失败（文本: {text[:20]}...）: {e}")
            return np.nan

    # 对 '正文' 列应用情感分析函数
    df['sentiment_score'] = df[TEXT_COLUMN].apply(get_sentiment)

    # 移除分析失败或空文本导致的 NaN 值
    df = df.dropna(subset=['sentiment_score'])

    print(f"成功计算 {len(df)} 条记录的情感得分。")
    return df


def aggregate_daily_trend(df):
    """
    按日期聚合数据，计算每日平均情感得分。
    """
    print("--- 3. 正在按日期聚合平均情感得分 ---")

    # 按日期分组，并计算平均得分
    daily_trend = df.groupby(DATE_COLUMN)['sentiment_score'].mean().reset_index()

    # 结果列重命名和格式化
    daily_trend.columns = ['date', 'average_sentiment_score']

    # 日期格式化为 YYYY-MM-DD 字符串，以确保绘图工具兼容性
    daily_trend['date'] = daily_trend['date'].dt.strftime('%Y-%m-%d')

    # 对结果按日期排序
    daily_trend = daily_trend.sort_values(by='date').reset_index(drop=True)

    # 计算全局平均值，供绘图时作对比线使用
    overall_average = daily_trend['average_sentiment_score'].mean()
    print(f"计算完成，总平均情感得分为: {overall_average:.4f}")

    return daily_trend


def save_data(df, file_path):
    """
    将处理后的情感趋势数据保存到 CSV 文件。
    """
    print(f"--- 4. 正在保存趋势数据到文件: {file_path} ---")
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("保存成功！您现在可以使用此文件进行可视化绘图。")


if __name__ == "__main__":

    # 1. 加载数据
    data_df = load_data(INPUT_FILE)

    if data_df is None:
        print("程序终止：数据加载或清洗失败。")
    else:
        # 2. 情感分析
        sentiment_df = analyze_sentiment(data_df)

        if len(sentiment_df) == 0:
            print("程序终止：未找到有效文本进行情感分析。")
        else:
            # 3. 聚合趋势
            trend_df = aggregate_daily_trend(sentiment_df)

            # 4. 保存结果
            save_data(trend_df, OUTPUT_FILE)

            # 打印前几行结果，供用户快速查看
            print("\n--- 每日情感趋势数据 (前 10 行) ---")
            print(trend_df.head(10).to_markdown(index=False, numalign="left", stralign="left"))