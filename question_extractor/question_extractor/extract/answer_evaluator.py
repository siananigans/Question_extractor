"""
File to take user answer and actual answer and to compare the two.
Also used to compare sentences within important sentences to ensure sentences are not too alike.

Compare using bleu score.

Returns a decimal(e.g 0.50 of 'correctness'.)
1 is identical and 0 is complete mismatch.

"""


from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk import PorterStemmer



def get_bleu_score(sent, can):

    stemmer = PorterStemmer()
    ref = []
    i = 0
    a = 0.35
    b = 0.30
    c = 0.20
    d = 0.15
    if len(sent) < 4:
        # work out weights for sentences less than 4
        if len(sent) == 1:
            a = 1.0
            b = 0.0
            c = 0.0
            d = 0.0
        elif len(sent) == 2:
            a = 0.5
            b = 0.5
            c = 0.0
            d = 0.0
        else:
            a = 0.34
            b = 0.33
            c = 0.33
            d = 0.0

    # Stem and lower words in both answers
    while i < len(sent):
        sent[i] = stemmer.stem(sent[i].lower())
        i += 1

    i = 0
    while i < len(can):
        can[i] = stemmer.stem(can[i].lower())
        i += 1

    ref.append(sent)
    # Smoothing so 0 is not gives for incorrect word in sent
    chencherry = SmoothingFunction()
    # bleu score
    bleu = sentence_bleu(ref, can, weights=[a, b, c, d], smoothing_function=chencherry.method1)
    return bleu


"""

REFACTORING

def n_grams( n, sent):
    lst = []

    for i in range(len(sent) - n + 1):
        lst.append(sent[i: i + n])
        i += n

    return lst

def get_bleu_score(u_a, c_a):

    i = 1
    n_gram_count = []
    u_a = u_a.split()
    c_a = c_a.split()

    while i <= 4:
        count = 0.0
        n_gram_user = n_grams(i, u_a)
        n_grams_correct = n_grams(i, c_a)



        for elem in n_gram_user:
            if elem in n_grams_correct:
                count += 1.0

        i += 1
        if len(n_gram_user) != 0.0:
            n_gram_count.append(count/len(n_gram_user))
        else:
            n_gram_count.append(0.0)


    bp = min(1, (len(u_a)/len(c_a)))

    count = 1.0

    print(n_gram_count)
    for gram in n_gram_count:
        count = count * gram

    bleu_score = (count ** 0.25) * bp
    return bleu_score



  """

