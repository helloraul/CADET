import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import os

documents=[]
all_words=[]
#  j is adject, r is adverb, and v is verb
allowed_word_types = ["J","R","V"]
#allowed_word_types = ["J"]


file_path = 'C:/Users/mcnambm1/nltk_data/corpora/movie_reviews/pos/'
print("Reading and parsing files ...")
for file in os.listdir(file_path):  #Get all positive review files
	review = open(file_path+file, "r").read()
	
	documents.append( (review, 'pos') )
	words = word_tokenize(review)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowed_word_types:
			all_words.append(w[0].lower())
	
file_path = 'C:/Users/mcnambm1/nltk_data/corpora/movie_reviews/neg/'

for file in os.listdir(file_path):  #Get all negative review files
	review = open(file_path+file, "r").read()
	
	documents.append( ( review, 'neg' ) )	
	words = word_tokenize(review)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowed_word_types:
			all_words.append(w[0].lower())

print("Finished reading")
save_documents = open("../resources/Trained_Classifiers/movieReviewDocuments.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:1000]

save_word_features = open("../resources/Trained_Classifiers/movie_word_features.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


def find_features(document):
	words = word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

featuresets = [(find_features(review), category) for (review, category) in documents]
random.shuffle(featuresets)

save_featuresets = open("../resources/Trained_Classifiers/movie_featuresets.pickle", "wb")
pickle.dump(featuresets, save_featuresets)
save_featuresets.close()

print(len(featuresets))

testing_set = featuresets[1000:]
training_set = featuresets[:1000]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

###############
save_classifier = open("../resources/Trained_Classifiers/movie_originalnaivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifier = open("../resources/Trained_Classifiers/movie_MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifier = open("../resources/Trained_Classifiers/movie_BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("../resources/Trained_Classifiers/movie_LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("../resources/Trained_Classifiers/movie_LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()


##NuSVC_classifier = SklearnClassifier(NuSVC())
##NuSVC_classifier.train(training_set)
##print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

save_classifier = open("../resources/Trained_Classifiers/movie_SGDC_classifier5k.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()
print("Finished")



