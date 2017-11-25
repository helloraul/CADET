from cadetapi.controllers.analysis.Processor import Processor 
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
        for c_id in self.dataset_ids:
            c_comment, i_comment = self.formatDbComment(CommentApi().get(comment_id = c_id), c_id)
            c_comment = CommentObject(c_comment)
            i_comment = CommentObject(i_comment)

            self.comments.append(c_comment)
            self.comments.append(i_comment)

    def runAnalysis(self):
        self.getCommentObjects()
        self.processor.init(self.comments, self.num_topics, self.words_per_topic, self.iterations)
        self.processor.process()

    def getCourseCommentList(self):
        return self.processor.getCourseCommentList()

    def getInstructorCommentList(self):
        return self.processor.getInstructorCommentList()

    def getInstructorSentimentHistogram(self):
        return self.processor.getInstructorSentimentHistogram()

    def getTopicModel(self):
        return self.processor.getTopicModel()

    def getTopicSentimentHistogram(self):
        return self.processor.getTopicSentimentHistogram()

    def __init__(self, dataset_ids, num_topics = 3, words_per_topic = 3, iterations = 20):
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations 
        self.dataset_ids = dataset_ids
        self.processor = Processor()

