"""
File to train sentence model using our test files of websites and
CASE notes.

"""
import sys
sys.path.append('..')
import nltk
import os
import pickle
from html_extractor import extract
from file_extractor import text_from_file


def main():

    # Note directory
    directory = '../test_files/CASE_Notes/'

    count = 0
    # import tokenizer
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

    # Train on Websites
    websites = open('../test_files/websites/urls.txt', 'r')
    websites = websites.readlines()
    for url in websites:
        count += 1
        # Extract using html imported extractor
        text = extract(url)
        tokenizer.train(text)

    # Train on Files
    for d in os.listdir(directory):
        for filename in os.listdir(directory + d):
            count += 1
            # Extract using text extractor imported function
            s = text_from_file(directory + d + '/' + filename)
            tokenizer.train(s)

    # Write model to file
    out = open('../models/sentence_model', 'wb')
    pickle.dump(tokenizer, out)
    out.close()

    print("Finished training sentence tokenizer with " + str(count) + " documents.")

if __name__ == '__main__':
    main()