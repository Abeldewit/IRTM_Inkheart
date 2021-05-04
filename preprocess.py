import re

## Read in a book ##
def read_book(num):
    names = ['1_Inkheart.txt', '2_Inkspell.txt', '3_Inkdeath.txt']
    with open('./books/'+names[num], 'r') as f:
        book = f.read().splitlines()
        f.close()
    book = [line for line in book if line != '']
    return book

## Chapter separation ##
# For each book, seperate it in chapters
def chop_chapters(book, reg=r'[0-9]+'):
    chapters = {}

    first_line = 0
    chap_count = 0
    for count, line in enumerate(book):
        tmp = re.match(reg, line)
        if tmp is not None:
            chapters[chap_count] = book[first_line:count]
            first_line = count
            chap_count += 1
        elif count == len(book)-1:
            chapters[chap_count] = book[first_line:count+1]
            first_line = count
            chap_count += 1
    return chapters


## Book name removal ##
# The name of the book is a recurring line which we don't want to take into account
def remove_book_name(book, name):
    return [line for line in book if name not in line]


## Chapter name removal ##
# In the third book, each chapter begins with the name of the chapter
# something that we also don't want to include in our text processing
def remove_chapter_name(chap_dict):
    for chap_num, chapter in chap_dict.items():
        chap_dict[chap_num] = chapter[2:]
    return chap_dict


## Quote removal ##
# In the first two books, each chapter starts with a poem or quote
# The author is always quoted with '- [author]' so we can separate it easily
def remove_quotes(chap_dict):
    for ch_count, chapter in chap_dict.items():
        for count, line in enumerate(chapter):
            if line[0] == '-':
                # We set the chapter to the text WITHOUT the poem
                chap_dict[ch_count] = chapter[count+1:]
                # No need to check more lines in this chapter
                break
    return chap_dict

