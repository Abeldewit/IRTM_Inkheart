import re
import nltk
from nltk.corpus import stopwords
import itertools
from collections import defaultdict

def chunkSentences(text):
    """
    Tokenize the text and give it POS tags so you can extract
    the named entities
    """
    sentences = nltk.sent_tokenize(text)
    tokenizedSentences = [nltk.word_tokenize(sent) for sent in sentences]
    taggedSentences = [nltk.pos_tag(sent) for sent in tokenizedSentences]
    chunkedSentences = nltk.ne_chunk_sents(taggedSentences, binary=True)

    return chunkedSentences

def extractEnitityNames(tree, _entityNames = None):
    """
    Loop through the nltk tree to find all named enities
    The tree allows NE's to have multiple words, solving the conjunction problem (most of the time)
    """
    if _entityNames is None:
        _entityNames = []
    try:
        label = tree.label()
    except AttributeError:
        pass
    else:
        if label == 'NE':
            _entityNames.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                extractEnitityNames(child, _entityNames=_entityNames)
    return _entityNames


def buildDict(chunkedSentences, _entityNames=None):
    """
    Extract all entities present in each sentence
    """
    if _entityNames is None:
        _entityNames = []

    for tree in chunkedSentences:
        extractEnitityNames(tree, _entityNames=_entityNames)
    return _entityNames


def getMajorCharacters(entityNames, _threshold=10):
    """
    There are many Named Enities that only occur once or twice, 
    hence we filter for NE's that have occured at least 10 times 
    (or some other threshold, if passed)
    """
    return {name for name in entityNames if entityNames.count(name) > _threshold}


def removeStopwords(entityNames, customStopWords=None):
    """
    The nltk pos tagger has some difficulties with standard English words
    that are at the beginning of a sentence 
    (e.g. "Try that new shampoo" -> ('Try', NE))
    Hence, we remove stopwords from the possible character list, 
    the stopwords are extended with custom words that were added manually
    """
    filterNames = []
    if customStopWords is None:
        with open("./customStopWords.txt", "r") as f:
            customStopWords = f.read().split(', ')

    for name in entityNames:
        if (name not in stopwords.words('english')) and (name not in customStopWords):
            filterNames.append(name)

    return filterNames

def splitIntoSentences(text):
    """
    Split sentences on .?! "" and not on abbreviations of titles.
    Used for reference: http://stackoverflow.com/a/8466725
    """
    sentenceEnders = re.compile(r"""
    (?:
      (?<=[.!?])
    | (?<=[.!?]['"])
    )
    (?<!  Mr\.   )
    (?<!  Mrs\.  )
    (?<!  Ms\.   )
    (?<!  Jr\.   )
    (?<!  Dr\.   )
    (?<!  Prof\. )
    (?<!  Sr\.   )
    \s+
    """, re.IGNORECASE | re.VERBOSE)
    return sentenceEnders.split(text)


def compareLists(sentences, characters):
    """
    TODO write definition
    """
    characterSentences = defaultdict(list)

    for sentence, name in itertools.product(sentences, characters):
        if re.search(r"\b(?=\w)%s\b(?!\w)" % re.escape(name),
                         sentence, re.IGNORECASE):
                characterSentences[name].append(sentence)
    return characterSentences

def create_name_dict(ne_books):
    """
    Goes through all the Named Enitity lists per book and saves when
    a name occurs. This allows for understanding of which characters
    appear in which book, and which characters span multiple books (probably the main characters)
    """
    names = [list(book.keys()) for book in ne_books]

    all_names = itertools.chain.from_iterable(names)

    name_dict = {}
    for name in all_names:
        if name in name_dict.keys():
            pass

        book_occurence = []

        if name in names[0]:
            book_occurence.append(0)
        if name in names[1]:
            book_occurence.append(1)
        if name in names[2]:
            book_occurence.append(2)

        name_dict[name] = book_occurence

    return name_dict