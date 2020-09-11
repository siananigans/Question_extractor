"""
File to chunk sentences in the format
(word, type, entity-position)
e.g (sian, NN, B-NP)

"""
import pickle


def chunk_sentences(sents):
    chunked_sents = []
    with open('../models/chunk_model', 'rb') as f:
        model = pickle.load(f)


    for sent in sents:
        chunked_sents.append(parse(sent, model))
    return(chunked_sents)



def parse(sentence, unigram):
    pos_tags = [pos for (word,pos) in sentence]
    tagged_pos_tags = unigram.tag(pos_tags)
    chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
    conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
    #return nltk.chunk.conlltags2tree(conlltags)
    return(conlltags)
