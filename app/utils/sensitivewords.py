import os
import chardet
import re
import ahocorasick
class SensitiveFilter:
    def merge_txt_files(self):
        merged_list = []
        folder_path = "C:\\Users\\Myf20\\PycharmProjects\\Localspecialty\\app\\utils\\Sensitive"
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                with open(os.path.join(folder_path, file), "rb") as f:
                    content = f.read()
                    encoding = chardet.detect(content)['encoding']
                    decoded_content = content.decode(encoding)
                    merged_list.extend(decoded_content.splitlines())
        return merged_list

    def build_actree(self,wordlist):
        actree = ahocorasick.Automaton()
        for index,word in enumerate(wordlist):
            actree.add_word(word,(index,word))
        actree.make_automaton()
        return actree
    # 构建敏感词库
    def replaceSensitive(self, txt):
        merged_list = self.merge_txt_files()
        actree = self.build_actree(wordlist=merged_list)
        sent_cp = txt
        for i in actree.iter(txt):
            sent_cp = sent_cp.replace(i[1][1], "**")
        count = txt.count("*")
        return count

