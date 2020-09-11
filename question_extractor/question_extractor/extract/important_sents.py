"""
To pick out the n-most important sentences from a text based
of tf-idf and a similarity score.

"""

from nltk import word_tokenize
from nltk.stem import PorterStemmer
import pickle
from .answer_evaluator import get_bleu_score
from django.conf import settings
import os
from nltk.corpus import stopwords


def get_important(sents, number):
    # Sort sentences based on score
    sorted_sents, word_scores = sort_sents(sents)
    # Pick top n sentences applying similarity as a factor
    top_sents = get_top(sorted_sents, number)
    # Return
    return top_sents, word_scores


def sort_sents(sents):
    sent_scores = {}
    # Stemmer
    porter = PorterStemmer()
    # Stop words
    stop_words = set(stopwords.words('english'))
    word_scores = {}


    filtered_sents = []
    doc_length = 0
    fdist = {}
    # Trained idf-model import
    idf_model_file = open(os.path.join(settings.BASE_DIR, 'question_extractor/extract/models/idf_model'), 'rb')
    idf_model = pickle.load(idf_model_file)
    # Get max idf
    max_idf = max(idf_model.values())

    # Make frequency distribution for t-f score
    symbols = ".;:@&*<>,-_`~()[]{}"
    for sent in sents:
        # Split into words
        word_tokens = word_tokenize(sent)
        # Filter sentence by stemming, lowering, removing stop words, and removing symbols
        filtered_sent = [porter.stem(w).lower() for w in word_tokens if
                         w.lower() not in stop_words and w not in symbols]
        doc_length += len(filtered_sent)
        # See i in frequency distribution, if not append
        for word in filtered_sent:
            if word in fdist.keys():
                fdist[word] += 1
            else:
                fdist[word] = 1
        filtered_sents.append(filtered_sent)
    i = 0

    while i < len(filtered_sents):
        sent = filtered_sents[i]
        sent_before_filter = sents[i]

        # Filter out short sentences (not important)
        if len(sent) >= 2 and len(sent_before_filter) > 3:
            # Find tf-idf scores
            score, word_scores = tf_idf(sent, fdist, doc_length, idf_model, max_idf, word_scores)
            # Append
            sent_scores[sent_before_filter] = score

        i += 1

    return sent_scores, word_scores


def tf_idf(sent, tf_dic, doc_length, idf_model, max_idf, words_scores):
    score = 0.0
    # Score each word
    for word in sent:
        # If no score to word already
        if word not in words_scores.keys():
            # Find tf score
            tf = tf_dic[word] / doc_length
            # Try give idf, if not in idf model give max
            try:
                idf = idf_model[word]
            except:
                idf = max_idf / 4
                print('in')

            # Total score
            word_score = tf * idf
            words_scores[word] = word_score

        else:
            word_score = words_scores[word]

        score += word_score

    # Normalize score
    score = score / len(sent)
    return score, words_scores


def get_top(sent_scores, number):
    top = []
    # Sort list with top being most important
    srt = sorted(sent_scores.items(), key=lambda x: -x[1])

    i = 1
    # Try append top scored sent
    try:
        if '?' not in srt[0][0]:
            top.append(srt[0][0])
        else:
            top.append(srt[1][0])
    # If it did not work not enough or long enough sents were provided
    except(IndexError):
        return 400

    # Look for similarity
    while i < len(srt) and len(top) != number:
        var = 0

        for sent in top:
            sent = sent.split()
            can = srt[i][0].split()
            bleu = get_bleu_score(sent, can)
            # If similarity is above 85% or it is a question,
            # Do not append
            if bleu > 0.35 or '?' in srt[i][0]:
                print(srt[i][0], can, bleu)
                var = 1

        if var == 0:
            top.append(srt[i][0])
        i += 1
    return top
