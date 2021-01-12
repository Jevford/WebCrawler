import re
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.corpus import words, stopwords

def split_text(text):
    text_list = re.split('[^a-zA-Z0-9]+', text.lower())
    return text_list



def tokenizer(text):
    stop_words = set(stopwords.words('english'))
    token_dict = defaultdict(int)
    stemmer = PorterStemmer()
    text_list = split_text(text)
    stem_list = [stemmer.stem(token) for token in text_list]
    for word in stem_list:
        if (word != "") and (word not in stop_words):
            token_dict[word] += 1
    return token_dict