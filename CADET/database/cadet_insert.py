from sqlalchemy import *
from sqlalchemy.orm import *
 
from cadet_db import *
import Comment as OrigCom
 
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
        instr = session.query(Instructor).filter(and_(
            Instructor.last_name  == self.lname,
            Instructor.first_name == self.fname,
            )).first()

        if instr is None: # record does not yet exist in the database
            # Insert new instructors into the instructors table
            new_instr = Instructor(first_name=self.fname,last_name=self.lname)
            session.add(new_instr)
            session.flush()
            self.pk = new_instr.id
            session.commit()
        else: # retrieved record from database, return primary key
            self.pk = instr.id
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

    def __init__(self):
        # Open session to the database
        self.sess = dbsession()



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
        course = session.query(Course).filter(and_(
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

    def __init__(self):
        # Open session to the database
        self.sess = dbsession()

class DbComment():
    pk = 0
    anon_id = 0 ;
    #comment = '' ;
    course_id = 0 ;
    instructor_id = 0 ;
    comment_type = 0 ;

    def GetId(self, comm):
        self.comment = comm
        self.course_id = self.course.GetId(comm.course_program,
                                           comm.course_modality,
                                           comm.course_num_sect_id)
        self.instructor_id = self.instr.GetId(comm.instructor_first_name,
                                              comm.instructor_last_name)
        self.anon_id = comm.anon_id

        session = self.sess

        # If there is an existing comment, check for that
        result = session.query(Comment).filter(and_(
            Comment.anon_id       == self.anon_id,
            Comment.course_id     == self.course_id,
            Comment.instructor_id == self.instructor_id,
            Comment.c_com         == comm.course_comments,
            Comment.i_com         == comm.instructor_comments,
            Comment.a_com         == comm.additional_comments,
            )).first()

        if result is None:
            # Insert new comment into the comments table
            new_comment = Comment(
                anon_id = self.anon_id,
                course_id = self.course_id,
                instructor_id = self.instructor_id,
                c_com = comm.course_comments,
                i_com = comm.instructor_comments,
                a_com = comm.additional_comments,
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
            self.comment.anon_id = result.anon_id
            self.comment.setInstructorName(fname, lname)
            self.comment.setCourse(prog, mod, num)
            self.comment.course_comments = result.c_com
            self.comment.instructor_comments = result.i_com
            self.comment.additional_comments = result.a_com

            return self.comment

    def __init__(self):
        # Open session to the database
        self.sess = dbsession()
        self.course = DbCourse()
        self.instr = DbInstructor()
        self.comment = OrigCom.Comment() ;
        

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
        sc = self.sess.query(Comment_Dataset.dataset_id)
        sc = sc.filter(~Comment_Dataset.comment_id.in_(self.comment_keys))

        query = self.sess.query(Comment_Dataset.dataset_id)
        query = query.filter(and_(Comment_Dataset.comment_id.in_(
            self.comment_keys)),
            ~Comment_Dataset.dataset_id.in_(sc))
        query = query.group_by(Comment_Dataset.dataset_id)
        numKeys = len(self.comment_keys)
        query = query.having(func.count(Comment_Dataset.id) == numKeys)
        result = query.first()
        if not result:
            # if not, create a new dataset based on these comments
            newDataset = Dataset()
            self.sess.add(newDataset)
            self.sess.flush()
            self.pk = newDataset.id
            for SingleId in self.comment_keys:
                newDataset = Comment_Dataset(
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
        result = session.query(Comment_Dataset.comment_id).filter(
            Comment_Dataset.dataset_id == self.pk
            ).all()

        if not result:
            # Primary Key not found in database
            print('nothing returned for dataset id', self.pk)
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
        self.sess = dbsession()
        self.comment = DbComment()


