import nltk
from nltk import word_tokenize
from nltk import pos_tag
import itertools

class Book:
    def __init__(self, chapters):
        self._book = list(itertools.chain.from_iterable(chapters.values()))
        self._chapters = chapters
        self._process = self._preprocess(chapters)
    
    def __str__(self):
        return self._book[:10]

    
    def _preprocess(self, chapters):
        process = {}

        for num, chap in chapters.items():
            chapter = " ".join(list(chap))            
            tok = word_tokenize(chapter)
            pos = pos_tag(tok)

            process[num] = pos
        return process


    def get_chap_num(self, chap_num):
        return self._chapters[chap_num]

    def get_proc_num(self, chap_num):
        return self._process[chap_num]

    def get_book(self):
        return self._chapters
    
    def get_process(self):
        return self._process
