import os
import chardet
import ahocorasick


class SensitiveFilter:
    _actree = None

    @classmethod
    def _get_actree(cls):
        """构建敏感词AC自动机（只构建一次，缓存复用）"""
        if cls._actree is not None:
            return cls._actree

        folder_path = os.path.join(os.path.dirname(__file__), "Sensitive")
        merged_list = []
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(folder_path, file)
                with open(file_path, "rb") as f:
                    content = f.read()
                    encoding = chardet.detect(content)["encoding"]
                    decoded_content = content.decode(encoding)
                    merged_list.extend(decoded_content.splitlines())

        actree = ahocorasick.Automaton()
        for index, word in enumerate(merged_list):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        cls._actree = actree
        return cls._actree

    def replaceSensitive(self, txt):
        """检测文本中的敏感词，返回匹配到的敏感词数量"""
        actree = self._get_actree()
        matches = list(actree.iter(txt))
        return len(matches)
