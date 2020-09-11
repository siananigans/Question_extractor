"""
Testing TF-IDF model to make sure it presents the right score.
------------------------------------------------------------------

Takes manually calculated idf-tf scores and sends same sentences
used to calculate them into the idf-tf program.

"""
import sys
sys.path.append('..')
from Training.idf_trainer import calculate_idf
from important_sents import get_important


def idf_tf_tester(answers):
    ls = []

    # Test data
    directory = "../test_files/idf_tf_testing/"

    # Idf trainer to train my test model
    calculate_idf(directory, 'idf_model_test')

    # Test file
    file_path = directory+'testing/doc1.txt'
    file = open(file_path, 'r')

    text = file.readline().strip()
    ls.append(text)

    # Get idf scores for the words in the test doc based on our model
    impor, scores = get_important(ls, 1, 'idf_model_test')

    # Validate if scores are same as manually calculated
    count = 0
    for word in scores.keys():
        score = round(scores[word], 3)
        if score == answers[word]:
            print('Same score for word: ' + str(word))
            count += 1
        else:
            print('Not the same score for word: ' + str(word))

    print("Algorithm is " + str(count/len(scores)*100) +"% correct.")


def main():
    # My words and scores (Calculated below)
    answers = {
        'test': 0.119,
        'idf-tf': 0.088,
        'calcul': 0.0
    }

    idf_tf_tester(answers)

if __name__ == '__main__':
    main()


"""
-----------MANUAL CALCULATION TO COMPARE------------

DOC1
_____________________________________
Three words that are not stop words:

test
idf-tf
calculation

Number of docs:

3

*test*

Appears: 1
num of words: 4
tf = 1/4 = 0.25

num of docs: 3
Appears in 1 doc

idf = log(3/1) = 0.47712125472

tf-idf of test:

0.47712125472 * 0.25 = 0.11928031368



*idf-tf*

Appears: 2
Num of words: 4

tf = 2/4 = 0.5

idf = log(3/2) = 0.17609125905


tf-idf = 0.08804562952



*calculate (calcul when stemmed)*

tf = 1/4 = 0.25

idf = log(3/3) = 0

tf-idf of calcul:

0

"""