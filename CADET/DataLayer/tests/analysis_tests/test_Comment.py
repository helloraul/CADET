from cadetapi.controllers.analysis.Comment import Comment as CommentObject
import unittest

inputs = [  
    # Test standard comment dictionary
    {
        'anon_id': 1,                       'comment':'hello',              'comment_id':42, 
        'comment_type':'instructor',        'course_modality':'classroom',  'topic_model_id':1,
        'course_num_sect_id':'101.123',     'sentiment':'positive',         'instructor_first_name':'Mr.',
        'instructor_last_name':'Smith' 
    },
    # Test if 'comment' and 'course_num_sect_id' is stored as a string and if others are stored as integers
    {
        'anon_id': '1',                     'comment':42,                   'comment_id':'42', 
        'topic_model_id':'1',               'course_num_sect_id':101.123 
    },
    # Test if undefined attributes are passed through
    {
        'comment':'hello',                  'Comment':'Comment',            'Comment_ID':'42',
    }
]

expected_outputs = [
    # Same output as input
    {
        'anon_id': 1,                       'comment':'hello',              'comment_id':42, 
        'comment_type':'instructor',        'course_modality':'classroom',  'topic_model_id':1,
        'course_num_sect_id':'101.123',     'sentiment':'positive',         'instructor_first_name':'Mr.',
        'instructor_last_name':'Smith' 
    },
    # Invert integers and strings. 'comment_type' is set to default ('')
    {
        'anon_id': 1,                       'comment':'42',                 'comment_id':42, 
        'topic_model_id':1,                 'course_num_sect_id':'101.123', 'comment_type':'', 
    },
    # 'Comment' and 'Comment_ID' are not stored. Default 'comment_type' and 'comment_id' are.
    {
        'comment':'hello',                  'comment_type':'',              'comment_id':0
    }
]
    
class TestCommentObject(unittest.TestCase):

    def test_dictionary_input(self):
        for index, input_dict in enumerate(inputs):
            assert CommentObject(input_dict).__dict__ == expected_outputs[index]

    def test_init(self):
        # default values
        assert CommentObject().__dict__ == {'comment':'', 'comment_id':0, 'comment_type':''}

        # set initial values
        assert CommentObject(comment = 'hi', comment_id = 22, comment_type = 'course').__dict__ == \
            {'comment':'hi', 'comment_id':22, 'comment_type':'course'}

        # dictionary overwrites initial value
        assert CommentObject(comment_dict = {'comment':'hello'}, comment = 'hi').__dict__ == \
            {'comment':'hello', 'comment_id':0, 'comment_type':''}

if __name__ == '__main__':
    unittest.main()
