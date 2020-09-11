"""
This is a tester for the answer evaluator to get the weightings and

smoothing of the bleu score well for our use case.

"""

import sys
sys.path.append('..')
from answer_evaluator import get_bleu_score


def bleu_test(sentence, refs):

    for ref in refs:
        print("\nSentences to compare:")
        print("1. " + sentence[0])
        print("2. " + ref)

        bleu = get_bleu_score(sentence[0].split(), ref.split())
        print("\nTheir score:")
        print(bleu)


def main():

    refs = ['This is a sample sentence for the bleu score', 'A complete opposite piece of text here for the bleu score',
            'sian', 'This is a test sentence for the bleu score']
    sent = ['This is a test sentence for the bleu score']

    bleu_test(sent, refs)


if __name__ == '__main__':
    main()

"""
---------MANUAL CALCULATION OF BLEU SCORE TO COMPARE-------------

sentence = This is a test sentence for the bleu score


refs = ['This is a sample sentence for the bleu score', 'A complete opposite piece of text here for the bleu score',
            'sian', 'This is a test sentence for the bleu score']


sentence n-grams:

1-gram = [This, is, a, test, sentence, for, the, bleu, score]
2-gram = [This is, is a, a test, test sentence, sentence for, for the, the bleu, bleu score]
3-gram = [This is a, is a test, a test sentence, test sentence for, sentence for the, for the bleu, the bleu score]
4-gram = [This is a test, is a test sentence, a test sentence for, test sentence for the, sentence for the bleu, for the bleu score]


first ref:
bleu = 0.6675


second ref:
bleu = 0.2865

third ref:
0.0

fourth ref:
1.0


"""
