from catalogue import create
from main_functions import ne_extract
import nltk
from nltk import word_tokenize
from nltk import pos_tag
import itertools
from coref_solver import *
import time
from tqdm import tqdm

class Book:
    def __init__(self, chapters):
        self._book = list(itertools.chain.from_iterable(chapters.values()))
        self._chapters = chapters
        self._process = self._preprocess(chapters)
        self.char_sents = None
        self.docs = {}
    
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

    def extract_ne(self):
        self.char_sents = ne_extract(self._chapters)

    def resolve_cor(self, num=100):
        for n, chap in tqdm(self._chapters.items()):
            if n > num:
                break
            self.docs[n] = create_doc(' '.join(chap))

    def get_book(self):
        return self._book     

    def get_chap(self, chap_num=None):
        if chap_num is None:
            return self._chapters
        return self._chapters[chap_num]

    def get_proc_num(self, chap_num=None):
        if chap_num is None:
            return self._process
        return self._process[chap_num]

    def get_coref(self, doc=None):
        if doc is None:
            return self.docs
        return self.docs[doc]
