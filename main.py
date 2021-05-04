import re
import numpy as np
import matplotlib.pyplot as plt
import spacy

from preprocess import *


def main():
    # We read every book and its chapters
    book1 = read_book(0)
    book2 = read_book(1)
    book3 = read_book(2)

    # We remove the book name references
    book2 = remove_book_name(book2, 'Ink 2 - Inkspell')
    book3 = remove_book_name(book3, 'Ink 3 - Inkdeath')

    # We divide each book in chapters (where book 3 has different chapter names)
    ch1 = chop_chapters(book1)
    ch2 = chop_chapters(book2)
    ch3 = chop_chapters(book3, reg=r'CHAPTER [0-9]+')

    # For the first two books we remove the quote/poem
    ch1 = remove_quotes(ch1)
    ch2 = remove_quotes(ch2)

    # And for the third book we remove the chapter names
    ch3 = remove_chapter_name(ch3)

if __name__ == '__main__':
    main()