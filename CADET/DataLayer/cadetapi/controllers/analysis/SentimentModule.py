#File: sentiment_mod.py


import random
#from nltk.corpus import movie_reviews

import pickle

from nltk.classify import ClassifierI
from statistics import mode
from statistics import StatisticsError
from nltk.tokenize import word_tokenize



class VoteClassifier(ClassifierI):
	 
	
    def __init__(self, *classifiers):
        self._classifiers = classifiers
		

    def classify(self, features):
        votes = []
        for c in self._classifiers:
		   
            v = c.classify(features)
            votes.append(v)  
        try:
            if len(set(votes)) != len(votes):
                return mode(votes)
            else:
                return votes[0]
        except StatisticsError:
            return votes[0]
	
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
			
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


documents_f = open("../resources/Trained_Classifiers/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()




word_features5k_f = open("../resources/Trained_Classifiers/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features



featuresets_f = open("../resources/Trained_Classifiers/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
#print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]



open_file = open("../resources/Trained_Classifiers/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("../resources/Trained_Classifiers/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()



open_file = open("../resources/Trained_Classifiers/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


#open_file = open("../resources/Trained_Classifiers/LogisticRegression_classifier5k.pickle", "rb")
#LogisticRegression_classifier = pickle.load(open_file)
#open_file.close()

open_file = open("../resources/Trained_Classifiers/movie_BernoulliNB_classifier5k.pickle", "rb")
movie_BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("../resources/Trained_Classifiers/movie_originalnaivebayes.pickle", "rb")
movie_classifier = pickle.load(open_file)
open_file.close()

open_file = open("../resources/Trained_Classifiers/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()


open_file = open("../resources/Trained_Classifiers/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("../resources/Trained_Classifiers/movie_reviews_NaiveBayes.pickle", "rb")
NaiveBayes_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(BernoulliNB_classifier,
								  movie_classifier,
								  movie_BernoulliNB_classifier,
								  BernoulliNB_classifier,
								  MNB_classifier,
								  classifier,
								  LinearSVC_classifier,
								  NaiveBayes_classifier)
								  

def sentiment(text):
    feats = find_features(text)
    print("Got into the snetimentModule")
    if voted_classifier.classify(feats) == 'pos':
        return "positive"
    elif voted_classifier.classify(feats) == 'neg':
        return "negative"
    else:
        return "neutral"

#    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
	
