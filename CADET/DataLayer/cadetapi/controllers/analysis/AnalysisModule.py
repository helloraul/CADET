from Comment import Comment
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import requests
import SentimentModule_twinward_api as sentimentAnalyzer

#import SentimentModule as sentimentAnalyzer
import multiprocessing
from multiprocessing import Process, Pipe, freeze_support

"""
AnalysisModule: for updating & processing student comments. We process the following data results:

1. topicModel -> dictionary{topic_id#, list(words in that topic)}
2. topic_sentiment_histogram -> dictionary{topic_id, list(num_pos_comments, num_neg_comments, num_neu_comments)}
3. instructor_sentiment_histogram -> dictionary{instructor_name, list(num__pos_comments, num_neg_comments, num_neu_comments)}
4. instructorCommentList -> updated list of Comment objs for each instructor -with sentiment, topic_id, instructorName 
5. commentList -> updated list of Comment objs for the course- with sentiment & topic_id

All results are procesed from the 'runAnalysis()' method which will execute processes in paralel 

LDA - Latent Dirichlet allocation  (https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)

"""

class AnalysisModule():
	#multiprocessing.set_start_method('spawn')
	tokenizer = RegexpTokenizer(r'\w+')
	stop_words = set(stopwords.words('english'))
	stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove if you need punctuation
	stop_words.update(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','u','x','y','z','0','1','2','3','4','5','6','7','8','9'])
	with open("stop_words.txt") as f:        #get stop_words from file 
	    file_stop_words = [line.rstrip('\n') for line in f ]
	stop_words.update(file_stop_words)
	
	text = ''
	comments = []
	
	commentList = list()
	topic_sentiment_histogram={} #dictionary with < topic_id, list(num_pos, num_neg) > mapping

	
	instructor_comments ={}
	instructor_sentiment_histogram = {}
	instructorCommentList = list()
	topicModel = {}
	
	num_topics = 5
	words_per_topic = 6
	iterations = 30
	

#runAnalysis:
#   init processes for computing topic model and getting sentiment	
	def runAnalysis(self):
		
		self.qList, childPipe = Pipe()
		
		self.instructorListPipe, commentPipe= Pipe()  
		ctx1 = multiprocessing.get_context('spawn')
		ctx2 = multiprocessing.get_context('spawn')
		self.sentiment_process = ctx1.Process(target=self.processSentiment, args=(childPipe,) )
		self.sentiment_process.daemon=True

		self.sentiment_process.start()
		
		if self.instructor_comments is not None: # if data is available
			self.instructor_process = ctx2.Process(target=self.processInstructorComments, args=(commentPipe,))
			self.instructor_process.start()
                
		freeze_support()
		
		self.processLDAModel()  #get LDA topic model obj 
		self.processTopicSentimentHistogram()  # process the topic_sentiment_histogram

		
		

#	ProcessTopicModel 
#		Here we clean the text and compute for the LDA model 	
	def processLDAModel(self):
	
		print("Generating Topic Model ... ")		
		doc_set = self.text.split(" ")  # get list of total words
		
		#p_stemmer = PorterStemmer()
		#texts = [p_stemmer.stem(i) for i in tokens] #removes stemmed words
		
		texts = []
        ##################----START TOPIC MODEL (LDA) ----########################################
		for i in doc_set:
			# clean and tokenize document string
			raw = i.lower()
			tokens = self.tokenizer.tokenize(raw)

			# remove stop words from tokens
			cleaned_tokens = [i for i in tokens if not i in self.stop_words]
			
			# stem tokens
			#stemmed_tokens = [p_stemmer.stem(i) for i in cleaned_tokens]
			
			# add tokens to new list
			texts.append(cleaned_tokens)
	
		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)#assign a unique integer id to each token (also does word count)
	
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts if text]
		
		#gensim.models.ldamodel.LdaModel
	
		self.ldamodel = gensim.models.ldamodel.LdaModel(corpus, self.num_topics, id2word = dictionary, passes=self.iterations)
		print("...Finished Topic Model")
		#print(self.ldamodel.print_topics(self.num_topics, self.words_per_topic))
		####################----FINISHED TOPIC MODEL (LDA) -----#####################################
		
		
	
#	processTopicSentimentHistogram
#		function to calculate a sentiment histogram for each topic, as well as
#		init the topic_model dictionary
	def processTopicSentimentHistogram(self):

		if self.instructor_comments is not None:	
			data = list()
			data = self.instructorListPipe.recv() # get results from multiProcessed method (processInstructorComments)
		
			self.instructor_sentiment_histogram = data[0]
			self.instructorCommentList = data[1]
			self.instructor_process.join()
			self.instructor_process.terminate()


		self.commentList = self.qList.recv() #get comments with sentiments (from processSentiment)
		self.sentiment_process.join()
		self.sentiment_process.terminate()  
		
		topic_dictionary = {}  # <topic_id, list_of_words_in_that_topic>
		
		for topic_id in range(0, self.num_topics):   # initialize topic_sentiment_histogram
			self.topic_sentiment_histogram[topic_id] = [0,0,0]
			topic_dictionary[topic_id] = list(dict(self.ldamodel.show_topic(topic_id, self.words_per_topic)).keys())
			print( topic_dictionary.get(topic_id) )
				
		self.topic_sentiment_histogram[-1] = [0,0,0] 
		indexer = 0
		
		###########---now we compute a sentiment histogram for each topic---############
		
		for comment in self.comments: # asign topic id number to a comment
			                          #for each comment, which topic shares the greatest # of words in commen 
			count_similarities = -1
			topic_id = -1
			
			for i in range(0, self.num_topics):  # for each topic 
				topic_words = topic_dictionary.get(i) # get the list of words from each topic_id

				temp_count = -1
				for word in topic_words:  #for each word in each topic 
					temp_count += comment.lower().count(word)						
					
				if temp_count > count_similarities:
					count_similarities = temp_count
					topic_id = i 

					
			self.commentList[indexer].setTopicModelId(topic_id)

			
			topic_id = self.commentList[indexer].getTopicModelId()
			sentiment_class = self.commentList[indexer].getSentimentClass()
			if(sentiment_class == 'positive'):
				self.topic_sentiment_histogram.get(topic_id)[0] = self.topic_sentiment_histogram.get(topic_id)[0]+1
			elif(sentiment_class == 'negative'):
				self.topic_sentiment_histogram.get(topic_id)[1] = self.topic_sentiment_histogram.get(topic_id)[1]+1
			else: # neutral
				self.topic_sentiment_histogram.get(topic_id)[2] = self.topic_sentiment_histogram.get(topic_id)[2]+1

			indexer+=1
	
		self.topicModel = topic_dictionary
	
	
#
#	processSentiment:
#	    Get sentiment classification for each comment 
#		Results stored in a list and piped back to origioal piped method call
#

	def processSentiment(self, conn): 
		
		print("Processing overall comments ...")
		indexer = 0
		cList=[]
		
		for comment in self.comments:
			#print("first comment = ", comment)
			sentiment = sentimentAnalyzer.sentiment(comment)

			##print("in processSentiment = ", sentiment)
			cList.append(Comment(comment=comment))
			cList[indexer].setSentimentClass(sentiment)
				
			indexer+=1
		conn.send(cList)	
		conn.close()
		print("Finish: processing overall comments...")
	
	
#
#	ProcessInstructorComments:
#		Here we calculate a sentiment histogram for each insturctor by analyzing their respective comments
#		Results are stored in a list and Piped back the origional Piped method call 
#		-Method runs in paralel to getTopicModel and multiProcessSentiment
#
	def processInstructorComments(self, comment_P): 
		import SentimentModule_twinward_api as sentimentAnalyzer
		print("Processing Instructor Comments ... ")
		
		instructorCommentList =[]
		instructor_sentiment_histogram = {}
		
		for instructor in self.instructor_comments.keys():  #for each instructor
		
			instructor_sentiment_histogram[instructor] = [0] * 3 #initialize array size=3
			
			for comment in self.instructor_comments.get(instructor): #for each comment about the instructor
				
				sentiment = sentimentAnalyzer.sentiment(comment) #get sentiment
				##print("in Instructor processing = ",sentiment)
				instructor_comment = Comment(comment=comment)    #create comment obj with sentiment and insturctor name
				instructor_comment.setSentimentClass(sentiment)
				instructor_comment.setInstructorName(instructor)
				instructorCommentList.append(instructor_comment) # add comment obj to list
			    
				#update sentiment histogram for each instructor
				if sentiment == "positive":  
					instructor_sentiment_histogram.get(instructor)[0] = instructor_sentiment_histogram.get(instructor)[0] + 1
				elif sentiment == "negative":
					instructor_sentiment_histogram.get(instructor)[1] = instructor_sentiment_histogram.get(instructor)[1] + 1
				else: #neutral
					instructor_sentiment_histogram.get(instructor)[2] = instructor_sentiment_histogram.get(instructor)[2] + 1
		
		data = []
		data.append(instructor_sentiment_histogram)
		data.append(instructorCommentList)
		
		comment_P.send(data)
		comment_P.close()
		
		print("Finished: Instructor comments...")	
    
	
	def getInstructorSentimentHistogram(self):
		return self.instructor_sentiment_histogram 
	
	def getTopicHistogram(self):
		return self.topic_sentiment_histogram
		
	def getCommentList(self):
		return self.commentList
		
	def getInstructorComments(self):
		return self.instructorCommentList
	
	def getTopicModel(self):
		return self.topicModel
		
	
	def __init__(self, comments, text, instructor_comments=None, num_topics=5, words_per_topic=6, iterations=30):
	
		#instructor_comments -> dictionary { instructorName, list(comments_about_instructor) }
		#comments -> list of comment-objs about the overall course (not about instructors)
		#text -> comments in one continuous string 
		
		self.comments = comments 
		self.text = text 

		self.instructor_comments = instructor_comments
		self.num_topics = num_topics
		self.words_per_topic = words_per_topic
		self.iterations = iterations
	
	    
