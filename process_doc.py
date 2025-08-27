import docx
import pandas as pd
import re


def process_word_to_excel(doc_path, output_excel_path):
    """
    处理Word文档，提取标题、日期和正文，并保存为Excel文件。
    """
    doc = docx.Document(doc_path)

    titles = []
    dates = []
    texts = []

    current_title = ""
    current_text = ""

    # 正则表达式用于匹配常见的日期格式
    date_pattern = re.compile(r'(\d{4}[年\-\/]\d{1,2}[月\-\/]\d{1,2}[日]?|\d{1,2}[/\-]\d{1,2}[/\-]\d{4})')

    for paragraph in doc.paragraphs:
        # 检查是否为黑体段落
        is_bold_title = any(run.bold for run in paragraph.runs)

        if is_bold_title:
            # 如果已经有数据，先保存上一段的记录
            if current_title:
                titles.append(current_title)

                # 寻找当前正文中的日期
                match = date_pattern.search(current_text)
                if match:
                    dates.append(match.group(0))
                    # 去掉正文中的日期
                    texts.append(date_pattern.sub('', current_text).strip())
                else:
                    dates.append("")
                    texts.append(current_text.strip())

            # 开始处理新的记录
            current_title = paragraph.text.strip()
            current_text = ""
        else:
            # 将非黑体段落内容添加到正文
            current_text += paragraph.text + "\n"

    # 处理最后一段内容
    if current_title:
        titles.append(current_title)
        match = date_pattern.search(current_text)
        if match:
            dates.append(match.group(0))
            texts.append(date_pattern.sub('', current_text).strip())
        else:
            dates.append("")
            texts.append(current_text.strip())

    # 打印列表长度以进行调试（可选）
    print(f"Titles length: {len(titles)}")
    print(f"Dates length: {len(dates)}")
    print(f"Texts length: {len(texts)}")

    # 创建DataFrame并保存为Excel
    df = pd.DataFrame({
        '标题': titles,
        '日期': dates,
        '正文': texts
    })

    df.to_excel(output_excel_path, index=False)
    print(f"文件处理完成，已保存至：{output_excel_path}")


# 使用示例：
word_file = '荆楚名校笔记.docx'
excel_file = '荆楚名校笔记_处理结果.xlsx'

process_word_to_excel(word_file, excel_file)