import string

"""
Comment: [container class]

Class that contains information regarding each student comment (and the
comment itself) For each comment activly store: sentiment, topic_model_id,
instructor_name
"""

class Comment():

    anon_id = 0
    comment = ''
    comment_id = 0
    comment_type = ''
    course_modality = ''
    course_num_sect_id = ''
    instructor_first_name = ''
    instructor_last_name = ''
    sentiment = ''
    topic_model_id = 0


    def show(self):
        print('Course: ' + self.course_num_sect_id)
        print('Instructor: ' + self.instructor_first_name + ' ' + self.instructor_last_name)
        print('Comment type: ' + self.comment_type)
        print('Comment: ' + self.comment)
        print('Sentiment: ' + self.sentiment)
        print('Comment ID: ' + str(self.comment_id))

    def convertFromCommentDict(self, comment_dict):
        if 'anon_id' in comment_dict: self.anon_id = comment_dict['anon_id']
        if 'comment' in comment_dict: self.comment = comment_dict['comment']
        if 'comment_id' in comment_dict: self.comment_id = comment_dict['comment_id']
        if 'comment_type' in comment_dict: self.comment_type = comment_dict['comment_type']
        if 'course_num_sect_id' in comment_dict: self.course_num_sect_id = comment_dict['course_num_sect_id']
        if 'instructor_first_name' in comment_dict: self.instructor_first_name = comment_dict['instructor_first_name']
        if 'instructor_last_name' in comment_dict: self.instructor_last_name = comment_dict['instructor_last_name']
        if 'sentiment' in comment_dict: self.sentiment = comment_dict['sentiment']
        if 'topic_model_id' in comment_dict: self.topic_model_id = comment_dict['topic_model_id']
        if 'course' in comment_dict: self.course_modality = comment_dict['course']

    def convertToCommentDict(self):
        return {
                    'anon_id':self.anon_id,
                    'comment':self.comment,
                    'comment_id':self.comment_id,
                    'comment_type':self.comment_type,
                    'course_num_sect_id':self.course_num_sect_id,
                    'instructor_first_name':self.instructor_first_name,
                    'instructor_last_name':self.instructor_last_name,
                    'sentiment':self.sentiment,
                    'topic_model_id':self.topic_model_id,
                    'course_modality':self.course_modality
                }
        
    def getComment(self):
        return self.comment

    def setComment(self, comment):
        self.comment = comment

    def getCommentId(self):
        return self.comment_id

    def setCommentId(self, comment_id):
        self.comment_id = comment_id

    def getCommentType(self):
        return self.comment_type

    def setCommentType(self, comment_type):
        self.comment_type = comment_type

    def getCourse(self):
        return self.course_num_sect_id

    def setCourse(self, course_num_sect_id):
        self.course_num_sect_id = course_num_sect_id

    def getInstructor(self):
        return (self.instructor_first_name, self.instructor_last_name)

    def setInstructor(self, first_name, last_name):
        self.instructor_first_name = first_name
        self.instructor_last_name = last_name

    def getModality(self):
        return self.course_modality

    def setModality(self, modality):
        self.course_modality = modality

    def getSentiment(self):
        return self.sentiment

    def setSentiment(self, sentiment):
        self.sentiment = sentiment

    def getTopicModelId(self):
        return self.topic_model_id

    def setTopicModelId(self, topic_model_id):
        self.topic_model_id = topic_model_id

    def __init__(self, comment_dict = None, comment = '', comment_type = '', comment_id = 0):

        if comment_dict is None:
            self.comment = comment
            self.comment_type = comment_type
            self.comment_id = comment_id
        else:
            self.convertFromCommentDict(comment_dict)

