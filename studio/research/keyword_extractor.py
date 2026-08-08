import re


class KeywordExtractor:
    def extract(self, text: str) -> list[str]:
        words = re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text.casefold())
        counts = {word: words.count(word) for word in set(words)}
        return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
