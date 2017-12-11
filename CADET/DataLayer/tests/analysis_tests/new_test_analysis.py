import multiprocessing
from multiprocessing import Process, Pipe, freeze_support
from cadetapi.controllers.analysis.AnalysisModule import AnalysisModule as Analyzer
from cadetapi.controllers.analysis.Comment import Comment as CommentObject
import unittest
from mock import patch, PropertyMock

class TestAnalysisModule(unittest.TestCase):

    instructor_comments = [
        CommentObject(comment_dict = {'comment':'hello', 'comment_type':'instructor',
            'instructor_first_name':'First', 'instructor_last_name':'Last', 'comment_id':0}),
        CommentObject(comment_dict = {'comment':'hi', 'comment_type':'instructor',
            'instructor_first_name':'Mr.', 'instructor_last_name':'Smith', 'comment_id':1}),
        CommentObject(comment_dict = {'comment':'see ya', 'comment_type':'instructor',
            'instructor_first_name':'Mrs.', 'instructor_last_name':'Smith', 'comment_id':2}),
        CommentObject(comment_dict = {'comment':'greetings', 'comment_type':'instructor',
            'instructor_first_name':'John', 'instructor_last_name':'Doe', 'comment_id':3}),
    ]

    course_comments = [
        CommentObject(comment_dict = {'comment':'goodbye', 'comment_type':'course',
            'instructor_first_name':'First', 'instructor_last_name':'Last', 'comment_id':0}), 
        CommentObject(comment_dict = {'comment':'bye', 'comment_type':'course',
            'instructor_first_name':'Mr.', 'instructor_last_name':'Smith', 'comment_id':1}),
        CommentObject(comment_dict = {'comment':'yo', 'comment_type':'course',
            'instructor_first_name':'Mrs.', 'instructor_last_name':'Smith', 'comment_id':2}),
        CommentObject(comment_dict = {'comment':'bye bye', 'comment_type':'course',
            'instructor_first_name':'John', 'instructor_last_name':'Doe', 'comment_id':3}) 
    ]

    all_comments = course_comments + instructor_comments

    def test_separateCommentTypes(self):
        with patch.object(Analyzer, 'comment_objects', new_callable=PropertyMock) as mock:
            mock.return_value = self.all_comments
            analyzer = Analyzer()
            analyzer.separateCommentTypes()
            course_output = analyzer.getCourseComments()
            assert course_output == self.course_comments
            instructor_output = analyzer.getInstructorComments()
            assert instructor_output == self.instructor_comments

    def test_processSentiment(self):
        # mock the function that determines the sentiment of the comments
        with patch('cadetapi.controllers.analysis.SentimentModule_twinward_api.sentiment', new_callable=PropertyMock) as mock:
            sentiments = ['positive', 'negative', 'neutral']
            for sentiment in sentiments:
                # force the sentiment to be evaluated
                mock.return_value = sentiment
                analyzer = Analyzer()
                parent_conn, child_conn = Pipe()
                p = Process(target=analyzer.processSentiment, args=(child_conn, self.course_comments))
                p.start()
                output = parent_conn.recv()
                p.join()
                for comment in self.course_comments:
                    # test that each comment's sentiment is that of the mocked value
                    assert output[comment.comment_id] == sentiment

    def test_InstructorComments(self):
        # mock the function that determines the sentiment of the comments
        with patch('cadetapi.controllers.analysis.SentimentModule_twinward_api.sentiment', new_callable=PropertyMock) as mock:
            sentiments = ['positive', 'negative', 'neutral']
            for index, sentiment in enumerate(sentiments):
                # force the sentiment to be evaluated
                mock.return_value = sentiment
                analyzer = Analyzer()
                parent_conn, child_conn = Pipe()
                p = Process(target=analyzer.processInstructorComments, args=(child_conn, self.instructor_comments))
                p.start()
                output = parent_conn.recv()
                p.join()
                instructor_sentiments = output[0]
                instructor_sentiment_histogram = output[1]
                for comment in self.instructor_comments:
                    # test that each comment's sentiment is that of the mocked value
                    assert instructor_sentiments[comment.comment_id] == sentiment
                    instr_name = comment.instructor_last_name + ', ' + comment.instructor_first_name

                    # {'instr_name': [#positive, #negative, #neutral]}
                    # with only 1 comment per instructor, the histogram should
                    # show only one comment associated with the current sentiment
                    assert instructor_sentiment_histogram[instr_name][index] == 1

                # test that the total number of comments in the histogram
                # == the total number of instructor comments
                count = 0
                for name in instructor_sentiment_histogram.keys():
                    count += instructor_sentiment_histogram.get(name)[0]
                    count += instructor_sentiment_histogram.get(name)[1]
                    count += instructor_sentiment_histogram.get(name)[2]
                assert count == len(self.instructor_comments)

if __name__ == '__main__':
    unittest.main()

