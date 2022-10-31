class Translator:
    def __init__(self, relevant_words):
        self.relevant_words = relevant_words

def get_keywords(filename):
    word_list = list()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                word_list.append(line.lower())
    return word_list
