import nltk
from preprocess import *
from named_entity import *
import re

def read_data():
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

    # Lastly we remove the first 'chapter' as this is introductory
    ch1.pop(0)
    ch2.pop(0)
    ch3.pop(0)

    return ch1, ch2, ch3

def ne_extract(book, _num=''):
    print("NE Extraction: " + str(_num))
    # Create one big string from the whole book
    text = " ".join(list(itertools.chain.from_iterable(list(book.values())[1:-1])))
    # Split the sentences
    sentences = nltk.sent_tokenize(text)

    # Tokenize and tag the sentences...
    tokenizedSentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    taggedSentences = [nltk.pos_tag(sentence) for sentence in tokenizedSentences]
    # ...and then create an nltk.tree.Tree from the sentences
    chunkedSentences = nltk.ne_chunk_sents(taggedSentences, binary=True)

    # Create a list of all the named entities
    entityNames = buildDict(chunkedSentences)
    entityNames = removeStopwords(entityNames)          # Remove the stop words
    majorCharacters = getMajorCharacters(entityNames)   # And get occurences > 10

    # Split the whole text in sentences using RegEx
    sentenceList = splitIntoSentences(text)

    # Compare the list of characters with each sentence
    # returns a dict of all sentences for each character
    characterSentences = compareLists(sentenceList, majorCharacters)

    return characterSentences 