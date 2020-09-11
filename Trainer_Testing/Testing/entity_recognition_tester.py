"""
Testing file to see if manually chosen entities and their corresponding
wh-word are given to a sentence.


As of 28/04/20:

 Percentage of correct sentences 100.0


"""
import sys
sys.path.append('..')
from extract_qs import Document

def get_question(sents_dict):

    s = ''
    # Make text from sents
    for sent in sents_dict.keys():
        s += sent + ' '

    s = s.strip()
    # initialize Document object
    doc = Document(s, len(sents_dict))

    # Extract qs
    doc.question_extractor()

    # Questions answers dict
    q_a = doc.answers_questions
    score = 0

    # Get entity and question word
    for key in q_a.keys():
        entity = key
        sent = q_a[key]
        brack = sent.find('{')
        tmp = brack
        while sent[brack] != '}':
            brack += 1
        word = sent[tmp+1:brack]
        wh_word = word.split(',')[0]

        s = entity + ' ' + wh_word
        for k in sents_dict:
            if s == sents_dict[k]:
                score += 1

    score = (score /len(sents_dict)) * 100

    print("Percentage of correct sentences " + str(score))


def main():
    test_sents = {'This is a sentence to test the entity recognition.': 'entity recognition what',
                  'Ireland is a place in the world.': 'Ireland Where',
                  'There are 35847 pieces in the thing.': '35847 how many', 'At 12.12 we had lunch under the tree.': '12.12 what time',
                  'On 12/12/1990 we had a lot to eat.': '12/12/1990 when', 'The 17th second was the hardest to beat.': '17th which',
                  'The computer had many languages installed on it including java.': 'java what language',
                  'Programming can be difficult when concurrency is involved.': 'concurrency what',
                  'The lecturer last week spoke about fairness and its respective solutions.': 'fairness what',
                  'Dennis Ritchie created the programming language C.' : 'Dennis Ritchie Who'}

    get_question(test_sents)


if __name__ == '__main__':
    main()
