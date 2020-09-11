"""
Extracts text from any file.

"""

from textract import process


def text_from_file(file_path):
    try:
        text = (process(file_path).decode('utf-8'))

    except:
        text = open(file_path, encoding='utf-8')

    text = str(text)
    text = text.replace('\n', ' ')
    text = text.replace('•', '.')

    return text
