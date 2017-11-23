from AnalysisModule import AnalysisModule as Analyzer
from Comment import Comment as CommentObject
#from PyQt5.QtCore import QThread


class Processor():

    num_topics = 0
    words_per_topic = 0
    iterations = 0
    text = ''
    instructor_comments = {}
    comments = list()


    def init(self, comment_list, num_topics = 5, words_per_topic = 6, iterations = 30):
        
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations
        self.comment_list = comment_list
        # add all comments to a single string
        for comment_object in comment_list:
            self.comments.append([comment_object.comment, comment_object.comment_id])
            self.text += comment_object.comment
            self.text += ' '
            if comment_object.instructor_comments:
                name = comment_object.instructor_first_name + ' ' + comment_object.instructor_last_name
                if name in self.instructor_comments:
                    self.instructor_comments.get(name).append([comment_object.instructor_comments, comment_object.comment_id])
                else:
                    self.instructor_comments[name] = []
                    self.instructor_comments.get(name).append([comment_object.instructor_comments, comment_object.comment_id])

    def process(self):

        self.Analyzer = Analyzer(self.comments, self.text, self.instructor_comments, self.num_topics, self.words_per_topic, self.iterations)

        self.Analyzer.runAnalysis() # This will take time !!!!
                                  # Once complete, we can get data 
        
        self.topic_model = self.Analyzer.getTopicModel()
        self.topic_sentiment_histogram = self.Analyzer.getTopicHistogram()
        self.commentList = self.Analyzer.getCommentList()
        self.instructor_sentiment_histogram = self.Analyzer.getInstructorSentimentHistogram()
        self.instructorCommentList = self.Analyzer.getInstructorComments()
        self.hasFinishedLoad = True

