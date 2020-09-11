"""
Gets the idf score of words in test collection and writes scores to file.
idf[word] = log(num_of_docs/num_of_docs_words_is_in)

"""
import sys
sys.path.append('..')
import os
from nltk import word_tokenize, PorterStemmer
import pickle
import math
from html_extractor import extract
from file_extractor import text_from_file
from _collections import defaultdict


freq_dist = defaultdict(int)


def calculate_idf(directory, exit, file=''):
    count = 0

    # get website data
    if file != '':
        websites = file.readlines()
        file.close()
        for url in websites:
            count += 1
            text = extract(url.strip())
            word_lst = word_tokenize(text)
            make_fdist(word_lst)


    # get file data

    for d in os.listdir(directory):
        for file in os.listdir(directory + d):
            count += 1
            text = text_from_file(directory + d + '/' + file)
            word_lst = word_tokenize(text)
            make_fdist(word_lst)

    idf_table = {}

    # Calculate idf for word and write to dict
    for word in freq_dist.keys():
        idf_table[word] = math.log(count / (freq_dist[word]), 10) # To Base 10
        #print(count, freq_dist[word], word, idf_table[word])

    # Write to file
    with open(exit, 'wb') as f:
        pickle.dump(idf_table, f)


def make_fdist(words):
    # Make frequency distrobution
    seen = []
    ps = PorterStemmer()
    for word in words:
        word = word.lower()
        word = ps.stem(word)
        if word not in seen:
            freq_dist[word] += 1
            seen.append(word)

"""

REFACORING

def calculate_idf():
    count = 0
    StopWords = set(stopwords.words("english"))
    ps = PorterStemmer()
    freq_dist = {}
    for d in os.listdir(directory):
        for filename in os.listdir(directory + d):
            count += 1
            print(directory + d + "/" + filename)
            try:
                s = (process(directory + d + "/" + filename).decode('utf-8'))
                text = str(s)
                words = word_tokenize(text)
                seen = []
                for word in words:
                    word = word.lower()
                    word = ps.stem(word)
                    if word not in seen:
                        if word in freq_dist:
                            freq_dist[word] += 1
                        else:
                            freq_dist[word] = 1
                        seen.append(word)
            except:
                print("Could not read file")


    idf_table = {}
    for word in freq_dist.keys():
        idf_table[word] = math.log(count / float(freq_dist[word]))
        print(count, freq_dist[word], word, idf_table[word])

    with open('/home/sian/Documents/project_V2/models/idf_model', 'wb') as f:
        pickle.test.txtdump(idf_table, f)

"""


def main():
    file = open('../test_files/websites/urls.txt', 'r')
    directory = "../test_files/CASE_Notes/"
    exit_file = "../models/idf_model"

    calculate_idf(directory, exit_file, file)


if __name__ == '__main__':
    main()
