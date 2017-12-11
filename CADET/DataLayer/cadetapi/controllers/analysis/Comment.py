import string

"""
Comment: [container class]

Class that contains information regarding each student comment (and the
comment itself) For each comment activly store: sentiment, topic_model_id,
instructor_name
"""

class Comment():

    # This class only holds attributes in the following lists
    # Make sure that these attributes are converted to strings or integers
    string_values = ['comment', 'comment_type', 'course_modality', 'course_num_sect_id',
            'instructor_first_name', 'instructor_last_name', 'sentiment']
    integer_values = ['anon_id', 'comment_id', 'topic_model_id']

    # Ensure that only the keys defined in this class are stored
    def convertFromCommentDict(self, comment_dict):
        for key, value in comment_dict.items():
            if key in self.string_values:
                self.__dict__[key] = str(value)
            elif key in self.integer_values:
                self.__dict__[key] = int(value)

    # Overwrite attributes, but prevent new attributes from being added
    def __setattr__(self, name, value):
        if name in self.string_values:
            self.__dict__[name] = str(value)
        elif name in self.integer_values:
            self.__dict__[name] = int(value)
        else:
            raise AttributeError("No such attribute: " + name)

    # Return a single attribute, if it is defined
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __init__(self, comment_dict = None, comment = '', comment_type = '', comment_id = 0):

        # A comment should have these attributes defined initially
        self.comment = str(comment)
        self.comment_type = str(comment_type)
        self.comment_id = int(comment_id)

        # Other attributes will be defined in this method / default attributes may be overwritten
        if comment_dict:
            self.convertFromCommentDict(comment_dict)

