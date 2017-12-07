from cadetapi.controllers.analysis.AnalysisModule import AnalysisModule as Analyzer
from cadetapi.controllers.analysis.Comment import Comment as CommentObject
from cadetapi.controllers.rest.ApiComment import CommentApi
from cadetapi.controllers.database.DbControl import DbStopword
from cadetapi.controllers.database.DbControl import DbResult

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
        comment_ids = DbResult().GetCommentIDs(self.result_set_id) #get from result_set_id
        for c_id in comment_ids:
            c_comment, i_comment = self.formatDbComment(CommentApi().get(comment_id = c_id), c_id)
            c_comment = CommentObject(c_comment)
            i_comment = CommentObject(i_comment)

            self.comments.append(c_comment)
            self.comments.append(i_comment)

    def runAnalysis(self):
        self.getCommentObjects()
        
        # get stop words from database
        stop_words = DbStopword().FullList()

        self.Analyzer = Analyzer(self.comments, stop_words, self.num_topics, self.words_per_topic, self.iterations)

        self.Analyzer.runAnalysis() # This will take time !!!!
                                  # Once complete, we can get data 
        
        self.topic_model = self.Analyzer.getTopicModel()
        self.topic_sentiment_histogram = self.Analyzer.getTopicHistogram()
        self.courseCommentList = self.Analyzer.getCourseComments()
        self.instructor_sentiment_histogram = self.Analyzer.getInstructorSentimentHistogram()
        self.instructorCommentList = self.Analyzer.getInstructorComments()
        self.hasFinishedLoad = True
        self.formatCourseCommentResults()
        self.formatInstructorCommentResults()
        self.results = {
                'topics_stats':self.topic_results,
                'instructor_stats':self.instructor_results
                }


        
    def formatCourseCommentResults(self):
        data = []
        for comment in self.courseCommentList:
            data.append([comment.getTopicModelId(), comment.getSentiment(), comment.getCommentId()])
        data.sort(key=lambda x: x[0])

        topics_stats = []
        for comment in data:
            if len(topics_stats) <= comment[0]:
                topics_stats.append({'comments': {'positive':[], 'negative':[], 'neutral':[]}, 'topic_words':[]})
            topics_stats[comment[0]]['comments'][comment[1]].append(comment[2])

        for topic_id in self.topic_model.keys():
            if len(topics_stats) <= topic_id:
                topics_stats.append({'comments': {'positive':[], 'negative':[], 'neutral':[]}, 'topic_words':[]})
            topics_stats[topic_id]['topic_words'].extend(self.topic_model[topic_id])
        self.topic_results = topics_stats

    def formatInstructorCommentResults(self):
        instructor_stats = []
        for instructor in self.instructor_sentiment_histogram.keys():
            instructor_stats.append({
                'instructor_first_name':instructor.split(', ')[1],
                'instructor_last_name':instructor.split(',')[0],
                'comments':{
                    'positive':[],
                    'negative':[],
                    'neutral':[]
                    }
                })
        
        for comment in self.instructorCommentList:
            fname, lname = comment.getInstructor()
            for index, x in enumerate(instructor_stats):
                if fname == instructor_stats[index]['instructor_first_name'] and lname == instructor_stats[index]['instructor_last_name']:
                    instructor_stats[index]['comments'][comment.getSentiment()].append(comment.getCommentId())
                    if 'course_num_sect_id' not in instructor_stats[index].keys():
                        instructor_stats[index]['course_num_sect_id'] = comment.getCourse()
        self.instructor_results = instructor_stats

    def getResults(self):
        return self.results

    def getInstructorResults(self):
        return self.instructor_results

    def getTopicResults(self):
        return self.topic_results

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

    def __init__(self, result_set_id, num_topics = 3, words_per_topic = 3, iterations = 20):
        self.num_topics = num_topics
        self.words_per_topic = words_per_topic
        self.iterations = iterations 
        self.result_set_id = result_set_id

