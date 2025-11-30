import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP
import os

# --- 配置项 ---
# 请将此路径替换为您本地 my_data_fixed.csv 文件的实际路径
CSV_PATH = 'my_data_fixed.csv'
OUTPUT_CHART_FILENAME = 'sentiment_trend_chart_optimized.png'

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号 '-' 显示为方块的问题


# --- 核心功能函数 ---

def calculate_sentiment_score(text):
    """
    使用 SnowNLP 计算文本的情感得分。得分在 0 到 1 之间。
    """
    try:
        s = SnowNLP(str(text))
        return s.sentiments
    except Exception as e:
        # 捕获异常，确保程序不会崩溃
        print(f"Error calculating sentiment: {e}")
        return np.nan


def generate_trend_chart(csv_path, output_filename):
    """
    从 CSV 读取数据，计算每日平均情感得分，并绘制趋势折线图。
    """
    if not os.path.exists(csv_path):
        print(f"错误：文件未找到，请检查路径是否正确：{csv_path}")
        return

    print("--- 1. 正在加载数据... ---")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except Exception as e:
        print(f"读取 CSV 文件时发生错误: {e}")
        return

    if '日期' not in df.columns or '正文' not in df.columns:
        print("错误：CSV 文件中必须包含 '日期' 和 '正文' 两列。")
        return

    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
    df.dropna(subset=['日期', '正文'], inplace=True)

    print(f"成功加载 {len(df)} 条有效数据。")

    print("--- 2. 正在计算情感得分... ---")
    df['Sentiment_Score'] = df['正文'].apply(calculate_sentiment_score)
    df.dropna(subset=['Sentiment_Score'], inplace=True)

    print("--- 3. 正在按日期聚合平均分... ---")
    daily_sentiment = df.groupby('日期')['Sentiment_Score'].mean().reset_index()
    daily_sentiment.columns = ['Date', 'Avg_Sentiment']
    daily_sentiment.sort_values(by='Date', inplace=True)

    # 检查聚合后的数据量，如果小于 1，则无法绘图
    if len(daily_sentiment) < 1:
        print("错误：聚合后没有足够的日期数据来绘制趋势图。请检查您的日期列。")
        return

    print(f"已生成 {len(daily_sentiment)} 个日期的情感平均分。")
    print("--- 4. 正在绘制情感趋势折线图（优化缩放和样式）... ---")

    # --- 绘图优化部分 ---
    plt.figure(figsize=(16, 7))  # 调整图表尺寸，使其更宽

    # 绘制折线图
    plt.plot(daily_sentiment['Date'],
             daily_sentiment['Avg_Sentiment'],
             marker='o',
             linestyle='-',
             color='#00a896',  # 优化颜色：深松石绿
             linewidth=3,  # 增加线条粗细
             markersize=8,  # 增加标记大小
             label='每日平均情感得分'
             )

    # 1. 动态 Y 轴缩放，放大波动效果
    min_score = daily_sentiment['Avg_Sentiment'].min()
    max_score = daily_sentiment['Avg_Sentiment'].max()  # 修复：确保 max_score 变量被正确定义

    # 设定 Y 轴下限：取最低分再减去一个缓冲值（0.03），但最低不低于 0.40
    y_limit_min = max(0.40, min_score - 0.03)
    plt.ylim(y_limit_min, 1.0)  # 设置 Y 轴范围

    # 2. 绘制整体平均线（对比色）
    overall_avg = daily_sentiment['Avg_Sentiment'].mean()
    plt.axhline(overall_avg,
                color='#ff6b6b',  # 优化颜色：珊瑚红
                linestyle='--',
                linewidth=1.5,
                label=f'整体平均 ({overall_avg:.4f})'
                )

    # 3. 突出显示高/低点 (修复 Index Error 的关键部分)
    # 使用 idxmax/idxmin 找到索引，再用 .loc[] 访问该索引对应的行数据，然后用 .iloc[0] 取值

    # 查找最高点
    max_idx = daily_sentiment['Avg_Sentiment'].idxmax()
    max_date = daily_sentiment.loc[max_idx, 'Date']

    # 查找最低点
    min_idx = daily_sentiment['Avg_Sentiment'].idxmin()
    min_date = daily_sentiment.loc[min_idx, 'Date']

    # 注意：最高点和最低点可能在同一天，这是正常的。

    # 绘制最高点
    plt.scatter(max_date, max_score, color='green', s=120, zorder=5, label=f'最高点 ({max_score:.4f})', marker='^')
    # 绘制最低点
    plt.scatter(min_date, min_score, color='red', s=120, zorder=5, label=f'最低点 ({min_score:.4f})', marker='v')

    # 4. 图表美化
    plt.title('个人笔记情感趋势分析 (每日平均情感得分)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('日期', fontsize=14)
    plt.ylabel(f'平均情感得分 (缩放至 {y_limit_min:.2f} - 1.0)', fontsize=14)
    plt.grid(axis='y', linestyle='-', alpha=0.4)

    # 更新图例位置，避免遮挡
    plt.legend(fontsize=12, loc='best')

    # 优化 X 轴标签显示
    plt.xticks(daily_sentiment['Date'][::max(1, len(daily_sentiment['Date']) // 15)],
               rotation=45, ha='right')
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_filename, dpi=300)
    print(f"--- 5. 优化后的情感趋势折线图已成功保存为：{output_filename} ---")
    # plt.show()


if __name__ == '__main__':
    generate_trend_chart(CSV_PATH, OUTPUT_CHART_FILENAME)