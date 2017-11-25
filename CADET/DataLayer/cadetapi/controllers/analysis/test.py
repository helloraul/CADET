from Processor import Processor 
from Comment import Comment as CommentObject

def create_comment_object(num, text):
    comment = CommentObject()
    comment.comment = text 
    comment.instructor_last_name = 'Who'
    comment.instructor_first_name = 'Cares'
    comment.course_program = ''
    comment.anon_id = 2
    comment.comment_id = num
    comment.comment_type = 'Course'
    return comment

if __name__ == "__main__":

    
    comments = list()
    comments.append(create_comment_object(1,'Fuck this'))
    comments.append(create_comment_object(2, 'Hello!'))
    comments.append(create_comment_object(3,'This sucks'))
    comments.append(create_comment_object(4,'I love you so much'))
    comments.append(create_comment_object(5,'You are awesome'))
    comments.append(create_comment_object(6,'I love to hate this class.'))
    comments.append(create_comment_object(7,'I love you so much that I hate myself.'))
    comments.append(create_comment_object(8,'You are the fucking shit bro. You are literally God incarnate.'))
    comments.append(create_comment_object(9,'You are okay.'))
    comments.append(create_comment_object(10,'Your mom says hi.'))

    processor = Processor()
    processor.init(comments,3,3,40)
    processor.process()

    for comment in processor.instructorCommentList:
        comment.show()
        print('')
    for comment in processor.courseCommentList:
        comment.show()
        print('')
    print(processor.topic_sentiment_histogram)
    print(processor.instructor_sentiment_histogram)

