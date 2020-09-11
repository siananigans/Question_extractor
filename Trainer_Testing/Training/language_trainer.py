import sys

sys.path.append('..')
from sentence_divider import get_sents
from important_sents import get_important
from tag_sents import sent_tagger
from chunk_sents import chunk_sentences
import pickle
from file_extractor import text_from_file
from html_extractor import extract
import os
from nltk import word_tokenize

language_file = open('../models/scraped_languages', 'rb')
languages = pickle.load(language_file)
model = open("../models/language_model", 'wb')
locations_model = {}

def check_for_language(sents):
    # Check location database
    nw_languages = []
    nouns = ['NN', 'NNP', 'NNS', 'NNPS']
    for sent in sents:
        for word in sent:
            if word[1] in nouns:
                if word[0].lower() not in nw_languages:
                    # Check for location
                    if word[0].lower() in languages:
                        nw_languages.append(word[0].lower())

    print(nw_languages)
    pickle.dump(nw_languages, model)


def split_doc(text):
    sentences = get_sents(text)
    tagged_sents = sent_tagger(sentences)

    return tagged_sents


def main():
    """ Take text & process it
        Then send in words to check location.
        Write to location model.
        location dict: 0 is not location 1 is location
    """
    # Send in website data

    websites = open('../test_files/websites/urls.txt', 'r')
    websites = websites.readlines()
    total_sents = []

    for url in websites:
        text = extract(url)
        sents = split_doc(text)
        # check_for_location(sents)
        total_sents = total_sents + sents

    # Send in file data

    directory = "../test_files/CASE_Notes/"
    for d in os.listdir(directory):
        for file in os.listdir(directory + d):
            text = text_from_file(directory + d + '/' + file)
            sents = split_doc(text)
            # check_for_location(sents)
            total_sents = total_sents + sents

    print("Number of sentences to be iterated: " + str(len(total_sents)))
    #print(total_sents)
    check_for_language(total_sents)

    # Write to file
    pickle.dump(locations_model, model)


if __name__ == '__main__':
    main()
