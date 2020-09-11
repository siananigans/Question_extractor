"""
File calls other functions to split, tag and chunk important sentences.
Then finds the most important entity in the sentences and puts a
corresponding question word (who, where etc).
Document.answers_questions() has entity(answer) and question in a dictionary.

"""
from sentence_divider import get_sents
from important_sents import get_important
from tag_sents import sent_tagger
from chunk_sents import chunk_sentences
from names_dataset import NameDataset
import re
from nltk.stem import PorterStemmer
import pickle
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


class Document:
    def __init__(self, text, num):
        self.text = text
        self.num = num
        self.answers_questions = {}
        self.position = 0

    def question_extractor(self):
        # Split into sentences
        sentences = get_sents(self.text)
        # Get number of important sentences from document
        important_sents, word_scores = get_important(sentences, self.num)
        # Error handling
        if type(important_sents) == int:
            self.answers_questions = important_sents

        else:
            # Tag sentences
            tagged_sents = sent_tagger(important_sents)
            # Chunk sents
            chunked_sents = chunk_sentences(tagged_sents)

            # Stop duplicate entities being used
            entity_lst = []

            for sent in chunked_sents:
                # Initialize object
                sent = Question_Sentence(sent, word_scores)
                # Find important entity and assign a question word
                # Sends in entity list to stop duplicates
                sent.wh_finder(entity_lst)
                # Append new entity
                entity_lst.append(sent.entity)
                # Form the question
                sent.form_question()
                # form the answer
                sent.form_answer()
                # Append both as key:value in dict
                self.answers_questions[sent.answer] = sent.question


class Question_Sentence:

    def __init__(self, sent, word_scores):
        self.answer = sent
        self.entity = ""
        self.wh_word = ""
        self.question = ""
        self.i = 0
        self.type = ''
        self.word_scores = word_scores

    def wh_finder(self, entity_lst):
        # Stemmer
        porter = PorterStemmer()

        # All our question words
        wh_words = ['who', 'when', 'where', 'what', 'how many', 'what language', 'what percentage',
                    'which', 'what time']

        # Language model to detect languages
        language_model = open('../models/language_model', 'rb')
        language_model = pickle.load(language_model)
        # Location model to detect locations
        location_model = open('../models/location_model', 'rb')
        location_model = pickle.load(location_model)
        # Names dataset
        m = NameDataset()  # Names Dataset

        i = 0
        word_scores = self.word_scores
        maxxy = -10

        while i < len(self.answer):
            # Stem and lower words
            word = porter.stem(self.answer[i][0].lower())
            if word in language_model:
                # Checking for languages, usually tagged as JJ. Tag as NN.
                self.answer[i] = (self.answer[i][0], 'NN', self.answer[i][2])
            # Check for non-stop word and Nouns and digits
            if word not in stop_words and (
                    self.answer[i][1] == 'NNP' or self.answer[i][1] == 'NNPS' or self.answer[i][1]
                    == 'NN' or self.answer[i][1] == 'NNS' or self.answer[i][1] == 'CD') and re.match(r'[\w]', word):
                # Maxxy is the highest score word, so get the most important
                if word_scores[word] > maxxy:
                    if self.answer[i][0] not in entity_lst:
                        maxxy = word_scores[word]
                        j = i
                    # Make sure sentence is not excluded due to duplicate entity
                    else:
                        replace = i

            i += 1

        try:
            j = j
        except:
            j = replace

        word = self.answer[j]
        self.entity = word[0]
        self.position = j

        # If word is noun phrase, plural or noun
        if word[1] == 'NNP' or word[1] == 'NNPS' or word[1] == 'NN' or word[1] == 'NNS':
            # Four options; Location(Where), Language(What language), Name(who), other(what)

            # Location
            if word[0].lower() in location_model:
                self.wh_word = wh_words[2]
                self.type = 'location'

            # Language of some kind
            elif word[0].lower() in language_model:
                self.wh_word = wh_words[5]
                self.type = 'language'

            # Name
            elif m.search_first_name(word[0].lower()) or m.search_last_name(word[0].lower()):
                self.wh_word = wh_words[0]
                self.type = 'name'

            else:
                self.wh_word = wh_words[3]
                self.type = 'thing'

        # if word is digits.
        elif word[1] == 'CD':
            # Time
            if re.match(r'([12][\d][:.][0-6][\d])+(am|pm)?', word[0]):  # Time
                self.wh_word = wh_words[8]  # What time
                self.type = 'time'
            # Date
            elif re.match(r'[1,2,3][\d][/.][01][\d]?[\d]?[/.][10][\d][\d]?[\d]?', word[0]):  # Date

                self.wh_word = wh_words[1]  # When
                self.type = 'date'
            # %
            elif '%' in word[0]:
                self.wh_word = wh_words[6]  # What %
                self.type = '%'
            # Day of month or placement
            elif re.match(r'[\d][\d]?(st|nd|rd|th)', word[0]):
                # Date with month
                months = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                          "october", "november", "december"]
                if self.answer[j + 1][0].lower() in months or self.answer[j + 2][0].lower() in months:
                    self.wh_word = wh_words[1]  # When
                    self.type = 'day_of_month'

                else:
                    self.wh_word = wh_words[7]  # Which
                    self.type = 'placement'

            # How many if  non of above
            else:
                self.wh_word = wh_words[4]  # How many
                self.type = 'quantity'

    # Take wh word and sent and form the question
    def form_question(self):

        # sentence
        answer = self.answer
        # position of beginning of entity
        i = self.position
        # noun list
        nouns = ['NN', 'NNS', 'NNPS', 'NNP', 'CD']

        if self.type != 'quantity' and self.type != 'time' and self.type != 'placement' and i != len(answer) - 1:

            # Go back to find beginning of entity
            while answer[i][2] != 'B-NP':
                i -= 1

            # Search for first meaningful word
            while answer[i][1] not in nouns:
                i += 1

            tmp = i
            # Start of sentence is beginning to the noun
            start = answer[:i]

            q = ''
            # Make start of question
            for word in start:
                q += word[0] + ' '

            # Go to next word in entity
            if i != len(answer) - 1:
                i += 1

            # Take out full
            while i < len(answer) - 1 and answer[i][2] == 'I-NP':
                i += 1

            self.entity = answer[tmp:i]
            words = [word[0] for word in answer[i:]]

        # Entity is last in sentence
        elif i == len(answer) - 1:
            start = answer[:i]
            q = ''
            for word in start:
                q += word[0] + ' '

            self.entity = [answer[i]]
            words = []
        # Entity is digit (Don't want to take out whole chunk)
        else:
            self.entity = [answer[i]]
            start = answer[:i]
            q = ''
            for word in start:
                q += word[0] + ' '

            words = [word[0] for word in answer[i + 1:]]

        # If start, capitalize
        if q == '':
            self.wh_word = self.wh_word.capitalize()

        # Question word
        q += '{' + self.wh_word + ',' + str(len(self.entity)) + '} '
        # End of sentence
        for word in words:
            if word != '.':
                q += word + ' '

        # Add ? to end
        question = q.strip() + '?'
        self.question = question

    # Get chunked sents and form the actual sent from it.
    def form_answer(self):
        chunked_ans = self.entity
        s = ''
        for word in chunked_ans:
            if word[0] == '’' or word[0] == 's':
                s += word[0]

            else:
                s += ' ' + word[0]
        s = s.strip()
        self.answer = s
