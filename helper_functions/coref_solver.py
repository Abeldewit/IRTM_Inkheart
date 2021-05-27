import spacy
import neuralcoref
import itertools

nlp = spacy.load('en_core_web_sm')
coref = neuralcoref.NeuralCoref(nlp.vocab, conv_dict={"Meggie": ["girl"], "Mo": ["father", "her father"]})
nlp.add_pipe(coref, name='neuralcoref')


def create_doc(text):
    """
    Creates a Spacy doc which can be used to access the coreferences
    """
    doc = nlp(text)
    return doc


def create_mention_dict(doc, names):
    """
    Creates a dictionary with the coreference mentions for a given set of names
    Acts like a filter for the many coreferences that are created
    """
    mention_dict = {}

    for cluster in doc._.coref_clusters:
        main = cluster.main
        mentions = cluster.mentions
        
        for name, ment in itertools.product(names, mentions):
            if name == ment.text:
                if name not in mention_dict.keys():
                    mention_dict[name] = mentions
