import os
import json

def export_to_json(data, file_name):
    file_name_without_extension = os.path.splitext(file_name)[0]
    
    if not os.path.exists('json'):
        os.mkdir('json')
    
    json_file_path = os.path.join('json', file_name_without_extension + '.json')
    
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {json_file_path}")

# 詞彙題 output
def vocabulary_question(passages):
    print("詞彙題:")
    for passage in passages:
        print("passage-id:", passage['id'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            print("questions-text:", question['text'])
            options = question['options']
            formatted_options = ['(%s) %s' % (chr(65 + i), option) for i, option in enumerate(options)]
            print("questions-options:", ' '.join(formatted_options))
            print()

# 綜合測驗 output
def comprehensive_test(passages):
    print("綜合測驗:")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            options = question['options']
            formatted_options = ['(%s) %s' % (chr(65 + i), option) for i, option in enumerate(options)]
            print("questions-options:", ' '.join(formatted_options))
            print()

# 文意選填 output
def cloze_test(passages):
    print("文意選填:")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            options = question['options']
            formatted_options = ['(%s) %s' % (chr(65 + i), option) for i, option in enumerate(options)]
            print("questions-options:", ' '.join(formatted_options))
            print()

# 篇章結構 output
def text_structure(passages):
    print("篇章結構:")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            options = question['options']
            formatted_options = ['(%s) %s' % (chr(65 + i), option) for i, option in enumerate(options)]
            print("questions-options:", ' '.join(formatted_options))
            print()

# 閱讀測驗 output
def reading_test(passages):
    print("閱讀測驗:")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            print("questions-text:", question['text'])
            options = question['options']
            formatted_options = ['(%s) %s' % (chr(65 + i), option) for i, option in enumerate(options)]
            print("questions-options:", ' '.join(formatted_options))
            print()

# 混合題 output
def mixed_questions(passages):
    print("混合題")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            print("questions-text:", question['text'])
            print()

# 非選擇題 output
def non_choice_questions(passages):
    print("非選擇題")
    for passage in passages:
        print("passage-id:", passage['id'])
        print("passage-content:", passage['content'])
        print()
        for question in passage['questions']:
            print("questions-id:", question['id'])
            print("questions-text:", question['text'])
            print()