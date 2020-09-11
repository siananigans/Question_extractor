"""
Testing the accuracy of picking out important sentences using TF-IDF model and bleu score.
------------------------------------------------------------------------------------------

Uses articles on BBC to create an IDF model. Uses that model and our important sentences
function to pick out the most important sentences in that article. We then compare these
to a corresponding summary of the article to find a percentage correctness.

We then compute the percentage of correct important sentences gathered if a random
sentence is picked. This is done for comparison.

"""


import sys
sys.path.append('..')
import os
from important_sents import get_important
from Training.idf_trainer import calculate_idf
from file_extractor import text_from_file
from sentence_divider import get_sents
import random



def idf_test():

    # Our test data
    article_directory = '../test_files/bbc-news-summary/News_articles/'
    summary_directory = '../test_files/bbc-news-summary/Summaries/tech/'

    # Use idf_trainer to train idf test model based on test data
    calculate_idf(article_directory, 'idf_model_test')

    total = 0
    count = 0
    count2 = 0

    for article in os.listdir(article_directory+'tech'):
        # Get text from article
        text = text_from_file(article_directory+'tech/' + article)
        # Get sents
        article_sents = get_sents(text)
        # Get text from summary file
        summ = text_from_file(summary_directory+article)
        # Get summary sents
        summ_sents = get_sents(summ)
        # Randomly generated summary sents
        dummy_important = dummy(article_sents, len(summ_sents))
        # Get important sentences using our algorithm and test model
        important, throw = get_important(article_sents, len(summ_sents), 'idf_model_test')

        total += len(important)

        # Compare
        for sent in summ_sents:
            i = 0
            while i < len(important):
                if sent == important[i]:
                    count += 1
                elif sent == dummy_important[i]:
                    count2 += 1
                i += 1

    # Display
    right = (count / total) * 100
    right2 = (count2 / total) * 100
    print('Percentage of random sentences correct: ' + str(right2) + '\nPercentage of TF-IDF sentences correct: ' + str(right))


def dummy(sents, num):
    i = 0
    limit = num
    important = []

    # Pick random number from length of article
    while len(important) <= limit:
        num1 = random.randint(0, len(sents)-1)
        if sents[num1] not in important:
            important.append(sents[num1])
        i += 1

    return important

def main():
    idf_test()

if __name__ == '__main__':
    main()

"""
1st iteration:

Percentage of random sentences correct: 32.8472755180353
Percentage of TF-IDF sentences correct: 37.5527352234t7242

2nd after bug fixes:

Percentage of random sentences correct: 32.8472755180353
Percentage of TF-IDF sentences correct: 45.459196725505244

3rd after more bug fixes:

Percentage of random sentences correct: 31.571254567600487
Percentage of TF-IDF sentences correct: 53.422655298416565

4rth after more bug fixes:

Percentage of random sentences correct: 31.893448524118075
Percentage of TF-IDF sentences correct: 55.02759779217663


"""