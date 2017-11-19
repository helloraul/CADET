# Need to append to the path in order to import the right files
import sys
sys.path.append('cadetapi/')
sys.path.append('cadetapi/controllers/database/')

from cadet_insert import *

# set up a list of comments
CommentList = []

# Create Comments to fill in my list
MyComment = {}
MyComment['anon_id'] = 42
MyComment['instructor_first_name'] = 'Joe'
MyComment['instructor_last_name'] = 'Bennett'
MyComment['course_program'] = 'Engineering'
MyComment['course_modality'] = 'in-person'
MyComment['course_num_sect_id'] = '605.423'
MyComment['course_comments'] = 'I like this class overall'
MyComment['instructor_comments'] = 'The instructor did a good job of challenging the students'
MyComment['additional_comments'] = 'The campus is in a really convenient location'

CommentList.append(MyComment)

MyComment = {}
MyComment['anon_id'] = 54
MyComment['instructor_first_name'] = 'Joel'
MyComment['instructor_last_name'] = 'Coffman'
MyComment['course_program'] = 'CyberSecurity'
MyComment['course_modality'] = 'Online'
MyComment['course_num_sect_id'] = '605.401'
MyComment['course_comments'] = 'love this class! i learn so much!'
MyComment['instructor_comments'] = 'he was entertaining and engaged and he always communicated things in a clear way.'
#MyComment['additional_comments'] = ''

CommentList.append(MyComment)

# Create a dataset and insert my list of comments
NewDataset = DbDataset()
dsid = NewDataset.GetId(CommentList)
print('I found (or inserted) all these comment IDs as DataSet:', dsid)

badid = 42
RetDataset = DbDataset()
comSetOne = RetDataset.GetDataset(badid)
if not comSetOne:
	print('Nothing returned for dataset with ID', badid)
else:
	for comment in comSetOne:
		print(comment['course_comments'])
comSetTwo = RetDataset.GetDataset(dsid)
if not comSetTwo:
	print('Nothing returned for dataset with ID', dsid)
else:
	for comment in comSetTwo:
		print(comment['course_comments'])
