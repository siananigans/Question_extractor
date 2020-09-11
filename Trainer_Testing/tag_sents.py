"""
Pos-Tag sentences eg Nouns, Adjectives etc
"""
import nltk


def sent_tagger(sents):
    tagged_sents = []
    for sent in sents:
        tokens = nltk.word_tokenize(sent)
        tag_sent = nltk.pos_tag(tokens)
        tagged_sents.append(tag_sent)
    return(tagged_sents)


def main():
    # Testing
    sentences = ["sian is the best", "Would you like me to be 7ft tall, or not?", '2am']
    sent_tagger(sentences)


if __name__ == '__main__':
    main()
