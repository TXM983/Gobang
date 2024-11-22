from openai import OpenAI
import os
from docx import Document
import win32com.client as win32

# 设置API密钥
client = OpenAI(api_key='sk-proj-T3OhHqrITTPywZWBn4jZT3BlbkFJljHH509oaHsX8aXluBWr')


# 读取.docx文档内容
def read_docx(file_path):
    doc = Document(file_path)
    document = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return document


# 读取.doc文档内容
def read_doc(file_path):
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(file_path)
    document = doc.Content.Text
    doc.Close()
    word.Quit()
    return document


# 读取文档内容
def read_document(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.docx':
        return read_docx(file_path)
    elif ext.lower() == '.doc':
        return read_doc(file_path)
    else:
        raise ValueError("Unsupported file format: {}".format(ext))


# 定义提取内容的函数
def extract_information(document):
    prompt = f"""
    从以下文档中提取出所有的关键人物、事件和日期信息：

    文档内容：
    {document}

    请提取出以下信息：
    1. 关键人物：
    2. 事件：
    3. 日期：
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=200,
    #     temperature=0.5
    # )

    return response['choices'][0]['text'].strip()


# 主程序
if __name__ == "__main__":
    file_path = 'C:\\Users\\ZY\\Documents\\WXWork\\1688855826372118\\Cache\\File\\2024-06\\1月1日一科收省厅4期.doc'  # 确保路径和文件名正确
    document = read_document(file_path)
    extracted_info = extract_information(document)
    print(extracted_info)
