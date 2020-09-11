"""
Splits text into sentences using sentence model
created using NLTK corpus.
"""

import pickle
import os
from django.conf import settings

def get_sents(text):
    with open(os.path.join(settings.BASE_DIR, 'question_extractor/extract/models/sentence_model'), 'rb') as sent_model:
        tokenizer = pickle.load(sent_model)

    sents = tokenizer.tokenize(text)

    return sents
