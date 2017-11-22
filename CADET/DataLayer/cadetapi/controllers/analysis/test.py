from Processor import Processor 
from Comment import Comment as CommentObject

def create_comment_object(text):
    comment = CommentObject()
    comment.comment = text 
    comment.sentiment_classifier = ''
    comment.topic_model_id = 0
    comment.course_comments = 'lame'
    comment.instructor_comments = text 
    comment.additional_comments = ''
    comment.instructor_last_name = 'Who'
    comment.instructor_first_name = 'Cares'
    comment.course_program = ''
    comment.course_modality = 0
    comment.course_num_sect_id = '123.45.6'
    comment.anon_id = 2
    return comment

if __name__ == "__main__":

    
    comments = list()
    comments.append(create_comment_object('Fuck this'))
    comments.append(create_comment_object('Hello!'))
    comments.append(create_comment_object('This sucks'))
    comments.append(create_comment_object('I love you so much'))
    comments.append(create_comment_object('You are awesome'))
    comments.append(create_comment_object('I love to hate this class.'))
    comments.append(create_comment_object('I love you so much that I hate myself.'))
    comments.append(create_comment_object('You are the fucking shit bro. You are literally God incarnate.'))
    comments.append(create_comment_object('You are okay.'))
    comments.append(create_comment_object('Your mom says hi.'))

    processor = Processor()
    processor.init(comments,3,3,40)
    processor.process()

    for comment in processor.instructorCommentList:
        comment.show()
        print('')
    print(processor.topic_sentiment_histogram)
    print(processor.instructor_sentiment_histogram)

