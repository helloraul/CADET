from cadet_insert import *

# set up a list of comments
CommentList = []

# Create Comments to fill in my list
MyComment = OrigCom.Comment()
MyComment.anon_id = 42
MyComment.setInstructorName('Joe', 'Bennett')
MyComment.setCourse('Engineering', 3, '605.423')
MyComment.course_comments = 'I like this class overall'
MyComment.instructor_comments = 'The instructor did a good job of challenging the students'
MyComment.additional_comments = 'The campus is in a really convenient location'
CommentList.append(MyComment)

MyComment = OrigCom.Comment()
MyComment.anon_id = 54
MyComment.setInstructorName('Joel', 'Coffman')
MyComment.setCourse('CyberSecurity', 2, '605.401')
MyComment.course_comments = 'love this class! i learn so much!'
MyComment.instructor_comments = 'he was entertaining and engaged and he always communicated things in a clear way.'
#MyComment.additional_comments = ''
CommentList.append(MyComment)

# Create a dataset and insert my list of comments
NewDataset = DbDataset()
dsid = NewDataset.GetId(CommentList)
print('I found (or inserted) all these comment IDs as DataSet:', dsid)


RetDataset = DbDataset()
comSetOne = RetDataset.GetDataset(42)
comSetTwo = RetDataset.GetDataset(dsid)
for comment in comSetTwo:
	print(comment.course_comments)
#print('I got something, but not sure how to show you')