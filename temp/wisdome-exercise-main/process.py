import re

class ExerciseProcessor:
    def __init__(self):
        # 初始化 passage_id 以從0開始給予每個 passage 一個唯一的ID
        self.passage_id = 0
    
    def clean_unwanted_patterns(self, texts):
        # 定義要去除的模式
        patterns_to_remove = [
            r'第\d+至\d+題為題組',
            r'\d+年學測', # 匹配 `xxx年學測`
            r'第 \d+ 頁', # 匹配 `第 x 頁 `
            r'共 \d+ 頁', # 匹配 `共 x 頁 `
            r'- \d+ -',   # 匹配 `- x -`
            r'英文考科',
            r'請記得在答題卷簽名欄位以正楷簽全名'
        ]

        for pattern in patterns_to_remove:
            texts = [re.sub(pattern, '', passage) for passage in texts]

        return texts

    def vocabulary_question(self, text):
    
        # 使用正則表達式提取問題和答案選項
        pattern = r'(\d+)\.\s(.*?)(?:\n\(A\) (.*?) \(B\) (.*?) \(C\) (.*?) \(D\) (.*?)(?=\n\d+\.|$))'
        matches = re.findall(pattern, text, re.DOTALL)
        
        # 生成問題字典的列表
        questions = [
            {
                "id": int(match[0]),  # 問題的ID
                "text": match[1].replace("\n", " "),  # 問題文本
                "options": [match[2], match[3], match[4], match[5].split("\n")[0]]  # 選項
            }
            for match in matches
        ]

        # 創建 passage 字典，包含ID、內容和問題
        new_passage = {
            'id': self.passage_id,
            'content': '',  
            'questions': questions
        }

        # 增加 passage_id 以供下次使用
        self.passage_id += 1
        return [new_passage]
    
    def comprehensive_test(self, text):
        # 提取內容的模式
        contents_pattern = r'第\d+至\d+題為題組\n(.*?)(?=\n\d+\. \(A\))'
        question_pattern = r'第(\d+)至(\d+)題為題組'
        options_pattern = r'(\d+)[.](.*?)(?=\n\d+\.|\n-|$)'
        option_text_pattern = r'\(A\)\s(.*?)\s\(B\)\s(.*?)(?=\s\(C\)|$)\s?\(C\)?\s?(.*?)\s?\(D\)?\s?(.*?)$'
        
        # 提取內容、問題組和選項
        contents = re.findall(contents_pattern, text, re.DOTALL)
        question_group = re.findall(question_pattern, text)

        # 移除掉與contents重複的字串避免搜索錯誤
        remaining_text = re.sub(contents_pattern, '', text, flags=re.DOTALL)

        question_options = re.findall(options_pattern, remaining_text, re.DOTALL)

        # 清理內容
        contents = self.clean_unwanted_patterns(contents)

        # 提取各選項的細節
        options = [
            (question_id, re.search(option_text_pattern, option_text, re.DOTALL).groups()) 
            for question_id, option_text  in question_options
        ]

        passages = []

        for i, (start, end) in enumerate(question_group):
            start, end = int(start), int(end)
            
            # 過濾出當前問題組的選項
            questions = [
                {
                    "id": int(question_id),
                    "text": '',
                    "options": [option_text[0].split('\n')[0], 
                                option_text[1].split('\n')[0], 
                                option_text[2].split('\n')[0], 
                                option_text[3].split('\n')[0]]
                }
                for question_id, option_text in options if start <= int(question_id) <= end
            ]

            passage = {
                'id': self.passage_id,
                'content': contents[i].replace("\n", " "),
                'questions': questions
            }
            
            passages.append(passage)
            self.passage_id += 1

        return passages
    
    def cloze_test(self, text):
        # 定義正則表達式模式
        contents_pattern = r'第\d+至\d+題為題組\n(.*?)\n\(A\)'
        question_pattern = r'第(\d+)至(\d+)題為題組'
        option_pattern = r'\((\w)\) ([^\)]+?)\s*(?=\(|$)'

        # 使用正則表達式查找相應的匹配項
        contents = re.findall(contents_pattern, text, re.DOTALL)
        question_group = re.findall(question_pattern, text)

        # 移除掉與contents重複的字串避免搜索錯誤
        remaining_text = text[len(contents[-1]):] # 這邊可優化

        options = re.findall(option_pattern, remaining_text)

        # 移除不必要的內容
        options = [(opt[0], opt[1].split("\n")[0]) for opt in options]

        passages = []
        for i, (start, end) in enumerate(question_group):
            start, end = int(start), int(end)
            
            questions = []
            for q_id in range(start, end+1):
                question = {
                    "id": q_id,
                    "text": '',
                    "options": options[q_id-start][1]
                }

                content = contents[i].replace("\n", " ")
                questions.append(question)

            passage = {
                'id': self.passage_id,
                'content': content,
                'questions': questions
            }

            passages.append(passage)
            self.passage_id += 1
        
        

        return passages
    
    def text_structure(self, text):
        # 定義正則表達式模式
        contents_pattern = r'第\d+至\d+題為題組\n(.*?)\n\(A\)'
        question_pattern = r'第(\d+)至(\d+)題為題組'
        option_pattern = r'\((\w)\) ([^\)]+?)\s*(?=\(|$)'
        
        # 使用正則表達式查找相應的匹配項
        contents = re.findall(contents_pattern, text, re.DOTALL)
        question_group = re.findall(question_pattern, text)
        options = re.findall(option_pattern, text)
        
        # 移除選項中的換行和後續內容
        options = [(opt[0], opt[1].split("\n")[0]) for opt in options]
        
        passages = []

        for i, (start, end) in enumerate(question_group):
            start, end = int(start), int(end)

            questions = []
            for q_id in range(start, end+1):
                question = {
                    "id": q_id,
                    "text": '',
                    "options": options[q_id-start][1]
                }

                content = contents[i].replace("\n", " ")
                questions.append(question)

            passage = {
                'id': self.passage_id,
                'content': content,
                'questions': questions
            }

            passages.append(passage)
            self.passage_id += 1

        return passages  
    
    def reading_test(self, text):
        contents_pattern = r'第(\d+)至(\d+)題為題組\n(.*?)(?=\n\1\.\s.*?\(A\))'
        options_pattern = r'(\d+)\.\s(.*?)(?=\n\d+\.|$)'
        option_detail_pattern = r'\(A\)\s(.*?)\s\(B\)\s(.*?)\s\(C\)\s(.*?)\s\(D\)\s(.*?)(?=\n|$)'

        # 使用正則表達式捕獲題組內容和題組起始號碼和結束號碼
        content_matches = re.findall(contents_pattern, text, re.DOTALL)
        remaining_text = re.sub(contents_pattern, '', text, flags=re.DOTALL)
        question_matches = re.findall(options_pattern, remaining_text, re.DOTALL)

        question_options = []

        for q_id, q_str in question_matches:        
            question_text = re.search(r'(.*?)(?=\n\(A\))', q_str, re.DOTALL)[1]
            option_match = re.search(option_detail_pattern, q_str, re.DOTALL)
            
            options = option_match.groups() if option_match else ("", "", "", "")
            question_options.append([q_id, question_text, options])

        passages = []
        for (start, end, content) in content_matches:
            start, end = int(start), int(end)
            questions = [
                {
                    "id": int(q_id),  # 問題的ID
                    "text": q_text.replace("\n", " "),  # 問題文本
                    "options": list(option)  # 選項
                }
                for q_id, q_text, option in question_options if start <= int(q_id) <= end
            ]

            content = self.clean_unwanted_patterns([content])[0]
            
            passage = {
                'id': self.passage_id,
                'content': content.replace("\n", " "),
                'questions': questions
            }
            
            passages.append(passage)
            self.passage_id += 1
            
        return passages

    def mixed_questions(self, text):

        contents_pattern = r'規定用筆作答。\n(.*?)\n-\s*\d+\s*-'
        # 提取題目區域的內容
        content_match = re.search(contents_pattern, text, re.DOTALL)

        # 移除掉與content_match[0]重複的字串避免搜索錯誤
        remaining_text = re.sub(contents_pattern, '', text, flags=re.DOTALL)


        # 根據題目分隔的模式捕獲所有問題
        question_blocks = re.findall(r'(\d+[.-].*?)(?=\d+[.-]|背 面 尚 有 試 題|$)', remaining_text, re.DOTALL)

        questions = []
        for block in question_blocks:
            # 為每個問題分配ID和文本
            match = re.search(r'(\d+)[.-](.*)', block, re.DOTALL)
                
            question_id, question_text = match.groups()

            question = {
                "id": int(question_id),
                "text": question_text.replace("\n", " "),
                "options": [] 
            }
            questions.append(question)

        # 提取題目區域的內容
        content = self.clean_unwanted_patterns([content_match[1]])[0].replace("\n", " ").strip()

        passage = {
            'id': self.passage_id,
            'content': content,
            'questions': questions
        }

        self.passage_id += 1
        return [passage]
    
    def non_choice_questions(self, text):
        translation_passage = self._get_translation_passage(text)
        composition_passage = self._get_composition_passage(text)

        return [translation_passage, composition_passage]

    def _get_translation_passage(self, text):
        question_pattern = r'一 、 中 譯 英 （ 占 \d+分 ）\n(.*?)\n二 、 英 文 作 文 （ 占 \d+分 ）'
        question_text = re.findall(question_pattern, text, re.DOTALL)[0]

        translation_questions_id = 100

        question = {
            "id": translation_questions_id,
            "text": question_text,
            "options": []
        }

        passage = {
            'id': self.passage_id,
            'content': '',
            'questions': [question]
        }

        self.passage_id +=1
        return passage
    
    def _get_composition_passage(self, text):
        question_pattern = r'二 、 英 文 作 文 （ 占 \d+分 ）\n(.*?)$'
        question_text = re.findall(question_pattern, text, re.DOTALL)[0]

        composition_questions_id = 200

        question = {
            "id": composition_questions_id,
            "text": question_text,
            "options": []
        }

        passage = {
            'id': self.passage_id,
            'content': '',
            'questions': [question]
        }

        return passage










