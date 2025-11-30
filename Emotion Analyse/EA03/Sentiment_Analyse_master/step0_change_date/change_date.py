import pandas as pd

# 尝试用 UTF-8、GBK 或 GB2312 读取
def read_csv_with_encoding(file_path):
    try:
        # 优先尝试 UTF-8 编码，这是最常见的
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        print("尝试 UTF-8 失败，尝试 GBK...")
        try:
            # 尝试 GBK 编码
            return pd.read_csv(file_path, encoding='gbk')
        except UnicodeDecodeError:
            print("尝试 GBK 失败，尝试 GB2312...")
            try:
                # 最后尝试 GB2312
                return pd.read_csv(file_path, encoding='gb2312')
            except UnicodeDecodeError:
                print("所有常见编码均失败，请手动检查文件编码。")
                return None

file_path = 'my_data.csv'
df = read_csv_with_encoding(file_path)

if df is not None:
    print("文件读取成功！")
    # 这里可以继续你的数据处理和保存逻辑
    # 比如：
    # df['日期'] = df['日期'].str.replace('年', '-').str.replace('月', '-').str.replace('日', '')
    # df.to_csv('my_data_fixed.csv', index=False, encoding='utf-8')





df = pd.read_csv('my_data.csv')



# 将 '2023年12月16日' 转换为 '2023-12-16'

df['日期'] = df['日期'].str.replace('年', '-').str.replace('月', '-').str.replace('日', '')



df.to_csv('my_data_fixed.csv', index=False)