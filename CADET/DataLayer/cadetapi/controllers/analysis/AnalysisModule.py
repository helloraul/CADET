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

1. 
2. topic_sentiment_histogram -> dictionary{topic_id, list(num_pos_comments, num_neg_comments, num_neu_comments)}
3. instructor_sentiment_histogram -> dictionary{instructor_name, list(num__pos_comments, num_neg_comments, num_neu_comments)}
4. instructorCommentList -> updated list of Comment objs for each instructor -with sentiment, topic_id, instructorName 
5. commentList -> updated list of Comment objs for the course- with sentiment & topic_id

All results are procesed from the 'runAnalysis()' method which will execute processes in paralel 

LDA - Latent Dirichlet allocation  (https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)

"""

class AnalysisModule():

    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove if you need punctuation
    stop_words.update(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','u','x','y','z','0','1','2','3','4','5','6','7','8','9'])
    with open("stop_words.txt") as f:        #get stop_words from file 
        file_stop_words = [line.rstrip('\n') for line in f ]
    stop_words.update(file_stop_words)

    comment_objects = []
    text = ''
    instructor_comments_dict = {}

    courseCommentList = list()
    instructorCommentList = list()

    topic_sentiment_histogram = {}
  
    topic_model = {}

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
        self.sentiment_process = ctx1.Process(target=self.processSentiment, 
                                        args=(childPipe, self.courseCommentList))
        self.sentiment_process.daemon=True

        self.sentiment_process.start()
        
        if self.instructorCommentList is not None: # if data is available
            self.instructor_process = ctx2.Process(target=self.processInstructorComments,
                                        args=(commentPipe, self.instructorCommentList))
            self.instructor_process.start()
        
        freeze_support()
        
        self.processLDAModel()  #get LDA topic model obj 
        self.updateAttributes()
        self.processTopicSentimentHistogram()  # process the topic_sentiment_histogram

    def updateAttributes(self):
        course_sentiments = self.qList.recv()
        for comment_object in self.courseCommentList:
            comment_object.setSentiment(course_sentiments[comment_object.getCommentId()])
        self.sentiment_process.join()
        self.sentiment_process.terminate()

        data = self.instructorListPipe.recv()
        instructor_sentiments = data[0]
        self.instructor_sentiment_histogram = data[1]
        for comment_object in self.instructorCommentList:
            comment_object.setSentiment(instructor_sentiments[comment_object.getCommentId()])
        self.instructor_process.join()
        self.instructor_process.terminate()

#       ProcessTopicModel 
#               Here we clean the text and compute for the LDA model    
    def processLDAModel(self):
    
        print("Generating Topic Model ... ")            
        doc_set = self.text.split(" ")  # get list of total words
        
        texts = []

        for i in doc_set:
            # clean and tokenize document string
            raw = i.lower()
            tokens = self.tokenizer.tokenize(raw)

            # remove stop words from tokens
            cleaned_tokens = [i for i in tokens if not i in self.stop_words]
            
            # add tokens to new list
            texts.append(cleaned_tokens)

        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(texts)#assign a unique integer id to each token (also does word count)

        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in texts if text]
        
        self.ldamodel = gensim.models.ldamodel.LdaModel(corpus, self.num_topics,
                        id2word = dictionary, passes=self.iterations)
        print("...Finished Topic Model")
        
        

    def processTopicSentimentHistogram(self):

        topic_dictionary = {}  # <topic_id, list_of_words_in_that_topic>
        
        for topic_id in range(0, self.num_topics):   # initialize topic_sentiment_histogram
            self.topic_sentiment_histogram[topic_id] = [0,0,0]
            topic_dictionary[topic_id] = list(dict(self.ldamodel.show_topic(topic_id,
                                            self.words_per_topic)).keys())
            print(topic_dictionary.get(topic_id))
                        
        self.topic_sentiment_histogram[-1] = [0,0,0] 
        indexer = 0 
        ###########---now we compute a sentiment histogram for each topic---############

        #for each comment, which topic shares the greatest # of words in commen 
        for comment_object in self.courseCommentList: # asign topic id number to a comment
            comment = comment_object.comment
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

                            
            self.courseCommentList[indexer].setTopicModelId(topic_id)
            
            topic_id = self.courseCommentList[indexer].getTopicModelId()
            sentiment_class = comment_object.getSentiment()
            if(sentiment_class == 'positive'):
                self.topic_sentiment_histogram.get(topic_id)[0] += 1 
            elif(sentiment_class == 'negative'):
                self.topic_sentiment_histogram.get(topic_id)[1] += 1
            else: # neutral
                self.topic_sentiment_histogram.get(topic_id)[2] += 1
            indexer += 1
        self.topic_model = topic_dictionary
            
 

    def processSentiment(self, conn, courseCommentList): 
       
        print("Processing overall comments ...")
        sentiment_dict = {}

        for comment_object in courseCommentList:
            sentiment = sentimentAnalyzer.sentiment(comment_object.comment)
            sentiment_dict[comment_object.comment_id] = sentiment

        conn.send(sentiment_dict)        
        conn.close()
        print("Finish: processing overall comments...")

    def separateCommentTypes(self):
        for comment_object in self.comment_objects:
            if comment_object.comment_type == 'Instructor':
                self.instructorCommentList.append(comment_object)
                
                # create a dictionary mapping comments to their intended instructor
                # instructor_name: {'comment': instructor_comment, 'comment_id': comment_id}
                name = comment_object.instructor_first_name + ' ' + comment_object.instructor_last_name
                comment_dict = {'comment':comment_object.getComment(),
                                 'id':comment_object.getCommentId()}
                if name in self.instructor_comments_dict:
                    self.instructor_comments_dict.get(name).append(comment_dict)
                else:
                    self.instructor_comments_dict[name] = []
                    self.instructor_comments_dict.get(name).append(comment_dict)

            elif comment_object.comment_type == 'Course':
                self.courseCommentList.append(comment_object)
            self.text += comment_object.comment
            self.text += ' '

    def processInstructorComments(self, conn, instructorCommentList):

        print("Processing Instructor Comments")
        instructor_sentiment_histogram = {} 
        sentiment_dict = {}
        for comment_object in instructorCommentList:
            sentiment = sentimentAnalyzer.sentiment(comment_object.comment)
            sentiment_dict[comment_object.comment_id] = sentiment
            name = comment_object.instructor_first_name + ' ' + comment_object.instructor_last_name
            if name not in instructor_sentiment_histogram:
               instructor_sentiment_histogram[name] = [0]*3
            if sentiment == 'positive':
                instructor_sentiment_histogram.get(name)[0] += 1
            elif sentiment == 'negative':
                instructor_sentiment_histogram.get(name)[1] += 1
            else:
                instructor_sentiment_histogram.get(name)[2] += 1
            
        data = []
        data.append(sentiment_dict)
        data.append(instructor_sentiment_histogram)
        conn.send(data)
        conn.close()
        print('Finished processing instructor comments')

    def getInstructorSentimentHistogram(self):
            return self.instructor_sentiment_histogram 
    
    def getTopicHistogram(self):
            return self.topic_sentiment_histogram
            
    def getCourseComments(self):
            return self.courseCommentList
            
    def getInstructorComments(self):
            return self.instructorCommentList
    
    def getTopicModel(self):
            return self.topic_model

    def __init__(self, comments, num_topics=5, words_per_topic=6, iterations=30):
    
        #instructor_comments -> dictionary { instructorName, list(comments_about_instructor) }
        #comments -> list of comment-objs about the overall course (not about instructors)
        
        self.comment_objects = comments 
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations
        self.separateCommentTypes() 

