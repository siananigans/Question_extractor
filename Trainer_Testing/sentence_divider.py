"""
Splits text into sentences using sentence model
created using NLTK corpus.
"""
import pickle

def get_sents(text):
    with open('../models/sentence_model', 'rb') as sent_model:
        tokenizer = pickle.load(sent_model)

    sents = tokenizer.tokenize(text)

    return sents
