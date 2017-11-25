from AnalysisModule import AnalysisModule as Analyzer
from Comment import Comment as CommentObject

class Processor():

    num_topics = 0
    words_per_topic = 0
    iterations = 0
    text = ''
    instructor_comments = {}
    comment_list = list()


    def init(self, comment_list, num_topics = 5, words_per_topic = 6, iterations = 30):
        
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations
        self.comment_list = comment_list

    def process(self):

        self.Analyzer = Analyzer(self.comment_list, self.num_topics, self.words_per_topic, self.iterations)

        self.Analyzer.runAnalysis() # This will take time !!!!
                                  # Once complete, we can get data 
        
        self.topic_model = self.Analyzer.getTopicModel()
        self.topic_sentiment_histogram = self.Analyzer.getTopicHistogram()
        self.courseCommentList = self.Analyzer.getCourseComments()
        self.instructor_sentiment_histogram = self.Analyzer.getInstructorSentimentHistogram()
        self.instructorCommentList = self.Analyzer.getInstructorComments()
        self.hasFinishedLoad = True

