from cadetapi.controllers.analysis.AnalysisModule import AnalysisModule as Analyzer
from cadetapi.controllers.rest.ApiStopword import StopwordApi
from cadetapi.controllers.analysis.Comment import Comment as CommentObject
from cadetapi.controllers.rest.ApiComment import CommentApi

class DatasetAnalysis():

    comments = list()

    def formatDbComment(self, db_comment, comment_id):
        course_comment = {}
        instructor_comment = {}
        for key in db_comment.keys():
            if 'comment' not in key:
                course_comment[key] = db_comment[key]
                instructor_comment[key] = db_comment[key]
            elif key == 'course_comments':
                course_comment['comment'] = db_comment[key]
                course_comment['comment_type'] = 'course'
            elif key == 'instructor_comments':
                instructor_comment['comment'] = db_comment[key]
                instructor_comment['comment_type'] = 'instructor'
        instructor_comment['comment_id'] = comment_id
        course_comment['comment_id'] = comment_id
        instructor_comment['sentiment'] = ''
        course_comment['sentiment'] = ''
        instructor_comment['topic_model_id'] = 0
        course_comment['topic_model_id'] = 0

        return course_comment, instructor_comment
    
    def getCommentObjects(self):
        for c_id in self.dataset_id:
            c_comment, i_comment = self.formatDbComment(CommentApi().get(comment_id = c_id), c_id)
            c_comment = CommentObject(c_comment)
            i_comment = CommentObject(i_comment)

            self.comments.append(c_comment)
            self.comments.append(i_comment)

    def runAnalysis(self):
        self.getCommentObjects()
        
        # get stop words from database
        stop_words = list()
        for item in StopwordApi().get():
            stop_words.append(item['stop_word'])
        
        # stop_words = DbStopword().FullList()
        self.Analyzer = Analyzer(self.comments, stop_words, self.num_topics, self.words_per_topic, self.iterations)

        self.Analyzer.runAnalysis() # This will take time !!!!
                                  # Once complete, we can get data 
        
        self.topic_model = self.Analyzer.getTopicModel()
        self.topic_sentiment_histogram = self.Analyzer.getTopicHistogram()
        self.courseCommentList = self.Analyzer.getCourseComments()
        self.instructor_sentiment_histogram = self.Analyzer.getInstructorSentimentHistogram()
        self.instructorCommentList = self.Analyzer.getInstructorComments()
        self.hasFinishedLoad = True

    def getCourseCommentList(self):
        return self.courseCommentList

    def getInstructorCommentList(self):
        return self.instructorCommentList

    def getInstructorSentimentHistogram(self):
        return self.instructor_sentiment_histogram

    def getTopicModel(self):
        return self.topic_model

    def getTopicSentimentHistogram(self):
        return self.topic_sentiment_histogram

    def __init__(self, dataset_id, num_topics = 3, words_per_topic = 3, iterations = 20):
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations 
        self.dataset_id = dataset_id

