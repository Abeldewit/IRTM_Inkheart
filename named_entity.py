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
    The tree allows NE's to have multiple words, solving the conjunction problem
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
    if customStopWords is None:
        with open("./customStopWords.txt", "rb") as f:
            words = str(f.read())
            
            customStopwords = words.split(", ")

    for name in entityNames:
        if name in stopwords.words('english') or name in customStopwords:
            entityNames.remove(name)
            
    return entityNames

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
                         sentence):
                characterSentences[name].append(sentence)
    return characterSentences