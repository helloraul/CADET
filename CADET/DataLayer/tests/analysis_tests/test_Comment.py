from cadetapi.controllers.analysis.Comment import Comment as CommentObject
import unittest

class TestCommentObject(unittest.TestCase):

    # Create a single dictionary in the CommentObject input format
    def createCommentDict(self, anon_id, comment, comment_id, comment_type, course, instr_fname, instr_lname, sentiment, model, modality):
        return {
            'anon_id':anon_id,
            'comment':comment,
            'comment_id':comment_id,
            'comment_type':comment_type,
            'course_num_sect_id':course,
            'instructor_first_name':instr_fname,
            'instructor_last_name':instr_lname,
            'sentiment':sentiment,
            'topic_model_id':model,
            'course_modality':modality,
            }

    # Create multiple dictionaries for testing
    def createCommentDictList(self):
        return [
        self.createCommentDict(1, 'hello', 1, 'instructor', '101.101', 'First', 'Last', 'positive',1, 'classroom'),
        self.createCommentDict(0, '', -1, 'course', '100', 'Mr.', 'Smith', '', 0, ''),
        self.createCommentDict(-1, '42', 0, 'neither', 'class', '', '', 'negative', -1, 'idk')
        ]

    # Create a comment object for testing
    def createCommentObject(self, anon_id, comment, comment_id, comment_type, course, instr_fname, instr_lname, sentiment, model, modality):
        comment_object = CommentObject()
        comment_object.anon_id = anon_id
        comment_object.comment = comment
        comment_object.comment_id = comment_id
        comment_object.comment_type = comment_type
        comment_object.course_num_sect_id = course
        comment_object.instructor_first_name = instr_fname
        comment_object.instructor_last_name = instr_lname
        comment_object.sentiment = sentiment
        comment_object.topic_model_id = model
        comment_object.course_modality = modality
        return comment_object

    # Create a list of comment objects for testing
    def createCommentObjectList(self):
        return [
        self.createCommentObject(1, 'hello', 1, 'instructor', '101.101', 'First', 'Last', 'positive', 1, 'classroom'),
        self.createCommentObject(0, '', -1, 'course', '100', 'Mr.', 'Smith', '', 0, ''),
        self.createCommentObject(-1, '42', 0, 'neither', 'class', '', '', 'negative', -1, 'idk')
        ]

    # Take the dictionaries defined above, and use them to create comment objects
    # If all attributes in the comment object are the same as the original dict, the test passes
    def test_conversion_to_object(self):
        comment_dicts = self.createCommentDictList()
        converted_comments = self.createCommentObjectList()

        for index, comment_dict in enumerate(comment_dicts):
            converted_comment = CommentObject()
            converted_comment.convertFromCommentDict(comment_dict)
            assert converted_comment.__dict__ == converted_comments[index].__dict__

        # Test values that should never appear in the comment object
        test_object = CommentObject()
        test_object.convertFromCommentDict({'Comment':'Hi', 'comment':'bye'})
        assert 'Comment' not in test_object.__dict__

    # Test the creation of a comment dictionary
    def test_conversion_to_dict(self):
        comment_objects = self.createCommentObjectList()
        converted_comments = self.createCommentDictList()
        for index, comment_object in enumerate(comment_objects):
            converted_comment = comment_object.convertToCommentDict()
            assert converted_comment == converted_comments[index]

    # Make sure that you are able to set and return values
    def test_getters_setters(self):
        comments = ['', 'a', 'This is a course comment']
        instructor_first_names = ['', 'F', 'This is a really long first name']
        instructor_last_names = ['', 'L', 'This is a really long last name']
        course_num_sect_ids = ['', 22, 'A']
        topic_model_ids = ['', 22, 'A']
        sentiments = ['', 22, 'pos']
        comment_types = ['', 22, 'comment type']
        comment_ids = ['', 22, 'A']
        anon_ids = ['', 22, 'A']
        course_modality = ['', 22, 'A']

        comment_object = CommentObject()
        for i in range(0, len(comments)):
            comment_object.setComment(comments[i])
            comment_object.setCommentId(comment_ids[i])
            comment_object.setCommentType(comment_types[i])
            comment_object.setCourse(course_num_sect_ids[i])
            comment_object.setInstructor(instructor_first_names[i], instructor_last_names[i])
            comment_object.setModality(course_modality[i])
            comment_object.setSentiment(sentiments[i])
            comment_object.setTopicModelId(topic_model_ids[i])
            
            assert comment_object.getComment() == comments[i]
            assert comment_object.getCommentId() == comment_ids[i]
            assert comment_object.getCommentType() == comment_types[i]
            assert comment_object.getCourse() == course_num_sect_ids[i]
            assert comment_object.getInstructor() == (instructor_first_names[i], instructor_last_names[i])
            assert comment_object.getModality() == course_modality[i]
            assert comment_object.getSentiment() == sentiments[i]
            assert comment_object.getTopicModelId() == topic_model_ids[i]

if __name__ == '__main__':
    unittest.main()
