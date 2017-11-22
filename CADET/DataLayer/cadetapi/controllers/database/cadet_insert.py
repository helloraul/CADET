#from sqlalchemy import *
#from sqlalchemy.orm import *
 
from cadetapi.models import *
#import Comment as OrigCom
 
class DbInstructor():
    pk = 0
    lname = ''
    fname = ''


    def GetId(self, fname, lname):
        if self.pk != 0 and self.fname==fname and self.lname==lname: 
            # the primary key is already set, just return it
            return self.pk
        else: # need to fetch the record from the database
            self.lname = lname
            self.fname = fname
            return self.__FetchID()

    def __FetchID(self):
        # Reference session to the database
        session = self.sess

        # fetch record if already exists
        result = session.query(Instructor).filter(db.and_(
            Instructor.last_name  == self.lname,
            Instructor.first_name == self.fname,
            )).first()

        if result is None: # record does not yet exist in the database
            # Insert new instructors into the instructors table
            new_instr = Instructor(first_name=self.fname,last_name=self.lname)
            session.add(new_instr)
            session.flush()
            self.pk = new_instr.id
            session.commit()
        else: # retrieved record from database, return primary key
            self.pk = result.id
        return self.pk

    def GetInstructor(self, pk):
        if self.pk == pk:
            return (self.lname, self.fname)
        else:
            self.pk = pk
            return self.__FetchInstructor()

    def __FetchInstructor(self):
        session = self.sess

        instr = session.query(Instructor).filter(
            Instructor.id == self.pk,
            ).first()
        if instr is None: # record does not exist
            # clear everything out and return false
            self.pk = 0
            self.lname=''
            self.fname=''
            return

        self.lname = instr.last_name
        self.fname = instr.first_name
        return (self.lname, self.fname)

    def Query(self, pk=None):
        query = self.sess.query(
                    Instructor.first_name.label('instructor_first_name'),
                    Instructor.last_name.label('instructor_last_name'),
                )
        if pk is None:
            return query.all()
        else:
            return query.filter(Instructor.id==pk).first()

    def __init__(self):
        # Open session to the database
        self.sess = DbSession()



class DbCourse():
    pk = 0
    program = ''
    modality = 0
    num_sec = ''
    
    def GetId(self, program, modality, num_sec):
        if (self.pk != 0 and \
            self.program==program and \
            self.modality==modality and \
            self.num_sec==num_sec):
            return self.pk
        else:
            self.pk = 0
            self.program = program
            self.modality = modality
            self.num_sec = num_sec
            return self.__FetchID()

    def __FetchID(self):
        # Open session to the database
        session = self.sess

        # Check to see if an entry already exists
        course = session.query(Course).filter(db.and_(
            Course.program  == self.program,
            Course.modality == self.modality,
            Course.num_sec  == self.num_sec,
            )).first()

        if course is None:
            # Insert new course into the courses table
            new_course = Course(program = self.program,
                                modality = self.modality,
                                num_sec = self.num_sec)
            session.add(new_course)
            session.flush()
            self.pk = new_course.id
            session.commit()
        else:
            self.pk = course.id
        return self.pk

    def GetCourse(self, pk):    
        if self.pk == pk:
            return (self.program, self.modality, self.num_sec)
        else:
            self.pk = pk
            return self.__FetchCourse()

    def __FetchCourse(self):
        session = self.sess

        course = session.query(Course).filter(Course.id == self.pk).first()
        if course is None: # record does not exist
            # clear everything out and return false
            self.pk = 0
            self.program=''
            self.modality=0
            self.num_sec=''
            return

        self.program = course.program
        self.modality = course.modality
        self.num_sec = course.num_sec
        return (self.program, self.modality, self.num_sec)

    def Query(self, pk=None):
        query = self.sess.query(
                    Course.program.label('course_program'),
                    Course.modality.label('course_modality'),
                    Course.num_sec.label('course_num_sect_id'),
                )
        if pk is None:
            return query.all()
        else:
            return query.filter(Course.id==pk).first()

    def __init__(self):
        # Open session to the database
        self.sess = DbSession()

class DbComment():
    pk = 0
    course_id = 0 ;
    instructor_id = 0 ;
    comment = {}

    def GetId(self, comm):
        self.__clear_comment()
        #self.comment = {**self.comment, **comm} # python >= 3.5
        self.comment.update(comm)
        self.course_id = self.course.GetId(self.comment['course_program'],
                                           self.comment['course_modality'],
                                           self.comment['course_num_sect_id'])
        self.instructor_id = self.instr.GetId(self.comment['instructor_first_name'],
                                              self.comment['instructor_last_name'])
        self.anon_id = self.comment['anon_id']

        session = self.sess

        # If there is an existing comment, check for that
        result = session.query(Comment).filter(db.and_(
            Comment.anon_id       == self.comment['anon_id'],
            Comment.course_id     == self.course_id,
            Comment.instructor_id == self.instructor_id,
            Comment.c_com         == self.comment['course_comments'],
            Comment.i_com         == self.comment['instructor_comments'],
            Comment.a_com         == self.comment['additional_comments'],
            )).first()

        if result is None:
            # Insert new comment into the comments table
            new_comment = Comment(
                anon_id = self.comment['anon_id'],
                course_id = self.course_id,
                instructor_id = self.instructor_id,
                c_com = self.comment['course_comments'],
                i_com = self.comment['instructor_comments'],
                a_com = self.comment['additional_comments'],
                )
            session.add(new_comment)
            session.flush()
            self.pk = new_comment.id
            session.commit()
        else:
            # Found existing record
            self.pk = result.id

        return self.pk

    def GetComment(self, pk):
        session = self.sess
        self.pk = pk
        self.comment = {}

        # If there is an existing comment, check for that
        query = session.query(Comment).filter(
            Comment.id == self.pk
            )
        #print(query)
        result = query.first()

        if result is None:
            # Primary Key not found in database
            return False
        else:
            # Found existing record
            (lname, fname) = self.instr.GetInstructor(result.instructor_id)
            (prog, mod, num) = self.course.GetCourse(result.course_id)
            self.comment = {}
            self.comment['anon_id'] = result.anon_id
            self.comment['instructor_first_name'] = fname
            self.comment['instructor_last_name'] = lname
            self.comment['course_program'] = prog
            self.comment['course_modality'] = mod
            self.comment['course_num_sect_id'] = num
            self.comment['course_comments'] = result.c_com
            self.comment['instructor_comments'] = result.i_com
            self.comment['additional_comments'] = result.a_com
            return self.comment

    def __clear_comment(self):
        pk = 0
        course_id = 0 ;
        instructor_id = 0 ;
        self.comment['anon_id'] = 0
        self.comment['instructor_first_name'] = ''
        self.comment['instructor_last_name'] = ''
        self.comment['course_program'] = ''
        self.comment['course_modality'] = ''
        self.comment['course_num_sect_id'] = ''
        self.comment['course_comments'] = ''
        self.comment['instructor_comments'] = ''
        self.comment['additional_comments'] = ''

    def Query(self, pk=None):
        query = self.sess.query(
                    Comment.anon_id.label('anon_id'),
                    Course.program.label('course_program'),
                    Course.modality.label('course_modality'),
                    Course.num_sec.label('course_num_sect_id'),
                    Instructor.first_name.label('instructor_first_name'),
                    Instructor.last_name.label('instructor_last_name'),
                    Comment.c_com.label('course_comments'),
                    Comment.i_com.label('instructor_comments'),
                    Comment.a_com.label('additional_comments'),
                ).join(Course).join(Instructor)
        if pk is None:
            return query.all()
        else:
            return query.filter(Comment.id==pk).first()

    def __init__(self):
        # Open session to the database
        self.sess = DbSession()
        self.course = DbCourse()
        self.instr = DbInstructor()
        self.__clear_comment()
        

class DbDataset():
    pk = 0
    comments = []
    comment_keys = []


    def GetId(self, dataset):
        # Identify if data already exists
        # Insert if data does not already exist
        # Return primary key identifier
        
        #iterate through each comment, collecting IDs as we go
        for SingleComment in dataset:
            newId = self.comment.GetId(SingleComment)
            self.comment_keys.append(newId)
        
        # then see if there is already a dataset of these particular IDs
        # I want to check if an existing dataset contains exactly these IDs

        # so first we see if any of these exist in any dataset

        #set up sub-query
        sc = self.sess.query(CommentDataSet.dataset_id)
        sc = sc.filter(~CommentDataSet.comment_id.in_(self.comment_keys))

        query = self.sess.query(CommentDataSet.dataset_id)
        query = query.filter(db.and_(CommentDataSet.comment_id.in_(
            self.comment_keys)),
            ~CommentDataSet.dataset_id.in_(sc))
        query = query.group_by(CommentDataSet.dataset_id)
        numKeys = len(self.comment_keys)
        query = query.having(db.func.count(CommentDataSet.id) == numKeys)
        result = query.first()
        if not result:
            # if not, create a new dataset based on these comments
            newDataset = DataSet()
            self.sess.add(newDataset)
            self.sess.flush()
            self.pk = newDataset.id
            for SingleId in self.comment_keys:
                newDataset = CommentDataSet(
                        comment_id = SingleId,
                        dataset_id = self.pk)
                self.sess.add(newDataset)
            
            self.sess.flush()
            self.sess.commit()
        else:
            self.pk = result.dataset_id
        
        


        return self.pk

    def GetDataset(self, pk):
        # Fetch existing dataset based on primary key
        session = self.sess
        self.pk = pk

        # If there is an existing comment, check for that
        result = session.query(CommentDataSet.comment_id).filter(
            CommentDataSet.dataset_id == self.pk
            ).all()

        if not result:
            # Primary Key not found in database
            return False
        else:
            del self.comments[:]
            for comment_id in result:
                # Re-initialize the comment object each time,
                # or else we'll just overwrite by reference
                newComment = DbComment()
                self.comments.append(newComment.GetComment(comment_id[0]))
            
            return self.comments

    def __init__(self):
        self.sess = DbSession()
        self.comment = DbComment()

class DbStopWord():
    word_list = []
    word_string = ''

    def FullList(self):
        query = self.sess.query(StopWord.stop_word)
        result = query.all()
        if not result:
            # Primary Key not found in database
            return False
        else:
            del self.stop_list[:]
            self.word_string = ''
            for word in result:
                # Re-initialize the comment object each time,
                # or else we'll just overwrite by reference
                self.word_list.append(word[0])
            self.word_string = ' '.join(word_list)
            return self.word_string

    def __init__(self):
        self.sess = DbSession()

class DbResult():
    pk = 0

    def StoreAnalysis(self, pk, analysis):
        # store analysis based on predetermined ID

        # first check to make sure we don't already have something
        existing = self.GetAnalysis(pk)
        if existing:
            return false #not positive this should be the return value





    def GetId(self, comments, topics, words, num_it):
        # retrieve result set
        # if result set exists, return it
        # if result doesn't exist, return the primary key
        dataset = DbDataset()
        dsid = dataset.GetId(comments)
        sw = DbStopWord()
        swl = sw.FullList()
        
        # If there is an existing dataset, check for that
        result = self.sess.query(ResultSet).filter(db.and_(
            ResultSet.dataset_id == dsid,
            ResultSet.topic_cnt  == topics,
            ResultSet.word_cnt   == words,
            ResultSet.iterations == num_it,
            ResultSet.stop_words == swl,
            )).first()

        if result is None: # record does not yet exist in the database
            # Insert new record
            record = ResultSet(
                dataset_id=dsid,
                topic_cnt = topics,
                word_cnt = words,
                iterations = num_it,
                stop_words = swl,
                )
            self.sess.add(record)
            self.sess.flush()
            self.pk = record.id
            self.sess.commit()
        else: # retrieved record from database, return primary key
            self.pk = result.id
        return self.pk

    def GetAnalysis(self, pk):
        return self.pk

    def __init__(self):
        self.sess = DbSession()
