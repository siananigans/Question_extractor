"""
File to train my chunking model.
Uses nltk's Bigram chunker and train and test data.

"""
import nltk.chunk
import nltk.corpus
import nltk.tag
import pickle

def parse(sentence, unigram):
    pos_tags = [pos for (word, pos) in sentence]
    tagged_pos_tags = unigram.tag(pos_tags)
    chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
    conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]

    return nltk.chunk.conlltags2tree(conlltags)

def tag_chunks(chunk_sents):
    tag_sents = [nltk.chunk.tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in tag_sents]



def chunk_model(train_sents, test_sents):
    train_chunks = tag_chunks(train_sents)
    test_chunks = tag_chunks(test_sents)
    ub_chunker = nltk.tag.BigramTagger(train_chunks)

    with open('../models/chunk_model', 'wb') as f:
        pickle.dump(ub_chunker, f)

    print('Result:',  ub_chunker.evaluate(test_chunks))



def main():
    conll_train = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    conll_test = nltk.corpus.conll2000.chunked_sents('test.txt', chunk_types=['NP'])

    result = chunk_model(conll_train, conll_test)



if __name__ == '__main__':
    main()


