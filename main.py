import os
import re
import json
import datetime
import pdfplumber

import output
from process import ExerciseProcessor

PATTERNS  = {
    "vocabulary_question": r'詞 彙 題 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "comprehensive_test": r'綜 合 測 驗 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "cloze_test": r'文 意 選 填 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "text_structure": r'篇 章 結 構 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "reading_test": r'閱 讀 測 驗 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "mixed_questions": r'混 合 題 （ 占 \d+分 ）(.*?)(?=\n[^\n]+? （ 占 \d+分 ）)',
    "non_choice_questions": r'非 選 擇 題 （ 占 \d+分 ）(.*?)(?=\n- \d+ -)'
}

def extract_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # 從第二頁讀取到最後一頁
        texts = [page.extract_text() for page in pdf.pages[1:]]
    return '\n'.join(filter(None, texts))

def export_to_json(data, file_name):
    file_name_without_extension = os.path.splitext(file_name)[0]
    
    if not os.path.exists('json'):
        os.mkdir('json')
    
    json_file_path = os.path.join('json', file_name_without_extension + '.json')
    
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {json_file_path}")

def process_text(text):
    extracted_texts = {}

    for key, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.S)
        if match:
            extracted_texts[key] = match[1].strip()
        else:
            print(f"Failed to extract the {key.replace('_', ' ')} text from the provided content.")
    return extracted_texts

def main():
    current_directory = os.getcwd()
    file_name = "112學年度學科能力測驗－英文.pdf"
    pdf_path = os.path.join(current_directory + "\pdf", file_name)
    print(file_name)

    today = datetime.datetime.today()
    date = today.strftime("%Y-%m-%d")
    
    exercise = {
        "source": pdf_path,
        "date": date,
        "passages": []
    }

    full_text = extract_pdf_text(pdf_path)
    extracted_texts = process_text(full_text)

    # 初始化 ExerciseProcessor 類
    processor = ExerciseProcessor()

    for key, text in extracted_texts.items():
        try:
             # 使用 getattr 從 `processor` 中獲取名為 `key` 的方法，
            passages = getattr(processor, key)(text)
            for passage in passages:
                exercise['passages'].append(passage)

            # 使用相對應的輸出副程式
            getattr(output, key)(passages)

        except Exception as e:
            print(key, e)

    export_to_json(exercise, file_name)

if __name__ == "__main__":
    main()