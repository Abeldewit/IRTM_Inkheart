import re
import numpy as np
import matplotlib.pyplot as plt
import spacy
import itertools

from main_functions import *
from preprocess import *
from named_entity import *
from Book import Book
import pickle


def main():
    # Read in the three books
    book_1, book_2, book_3 = read_data()
    
    # Create the book objects
    # B1 = Book(book_1)
    # B1.extract_ne()
    # B1.resolve_cor()

    print("Finished creating book 1")
    B2 = Book(book_2)

    # B2.extract_ne()
    B2.resolve_cor(num=2)

    with open(f'./books/B2', 'wb') as f:
            pickle.dump(B2, f)

    print("Finished creating book 2")
    # B3 = Book(book_3)
    # B3.extract_ne()
    # B3.resolve_cor()
    print("Finished creating book 3")

    # for num, book in enumerate([B1, B2, B2]):
    #     with open(f'./books/B{num}', 'wb') as f:
    #         pickle.dump(book, f)




if __name__ == '__main__':
    main()