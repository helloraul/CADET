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
                    Course.program.label('program'),
                    Course.modality.label('modality'),
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
        self.course_id = self.course.GetId(self.comment['program'],
                                           self.comment['modality'],
                                           self.comment['course_num_sect_id'])
        self.instructor_id = self.instr.GetId(self.comment['instructor_first_name'],
                                              self.comment['instructor_last_name'])
        self.anon_id = self.comment['anon_id']

        # PutComment returns comment ID
        # Add comment to DB if does not exist
        return self.PutComment(comm)

    def PutComment(self, comm):
        session = self.sess

        # If there is an existing comment, check for that
        result = session.query(Comment).filter(db.and_(
            Comment.anon_id       == comm['anon_id'],
            Comment.course_id     == self.course_id,
            Comment.instructor_id == self.instructor_id,
            Comment.c_com         == comm['course_comments'],
            Comment.i_com         == comm['instructor_comments'],
            Comment.a_com         == comm['additional_comments'],
            )).first()

        if result is None:
            # Insert new comment into the comments table
            new_comment = Comment(
                anon_id = comm['anon_id'],
                course_id = self.course_id,
                instructor_id = self.instructor_id,
                c_com = comm['course_comments'],
                i_com = comm['instructor_comments'],
                a_com = comm['additional_comments'],
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
            self.comment['program'] = prog
            self.comment['modality'] = mod
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
        self.comment['program'] = ''
        self.comment['modality'] = ''
        self.comment['course_num_sect_id'] = ''
        self.comment['course_comments'] = ''
        self.comment['instructor_comments'] = ''
        self.comment['additional_comments'] = ''

    def Query(self, pk=None):
        query = self.sess.query(
                    Comment.anon_id.label('anon_id'),
                    Course.program.label('program'),
                    Course.modality.label('modality'),
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
        
        # reset (clear) existing comment_keys
        del self.comment_keys[:]
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

class DbStopword():
    word_list = []
    word_string = ''

    def FullList(self):
        query = self.sess.query(Stopword.stop_word)
        result = query.all()
        if not result:
            # Primary Key not found in database
            return False
        else:
            del self.word_list[:]
            self.word_string = ''
            for word in result:
                # Re-initialize the comment object each time,
                # or else we'll just overwrite by reference
                self.word_list.append(word[0])
            self.word_string = ' '.join(self.word_list)
            return self.word_string

    def InsertWord(self, word):
        for w in word:
            # If there is an existing word, check for that
            result = self.sess.query(Stopword).filter(db.and_(
                Stopword.stop_word == w,
                )).first()

            if result is None:
                # Insert new word into the stop_words table
                new_record = Stopword(
                    stop_word = w,
                    )
                self.sess.add(new_record)
                #self.sess.flush()

        self.sess.commit()
        
        # Return all stopwords
        return self.Query()

    def Query(self, pk=None):
        query = self.sess.query(Stopword)
        if pk is None:
            return query.order_by(Stopword.stop_word).all()
        else:
            return query.filter(Stopword.id==pk).first()

    def __init__(self):
        self.sess = DbSession()

class DbResult():
    pk = 0

    def StoreAnalysis(self, pk, analysis):
        # store analysis based on predetermined ID

        # first check to make sure we don't already have something
        exists = self.Query(pk)
        if exists:
            print('Cannot insert analysis, analysis has already been performed')
            return True #not positive this should be the return value

        # Fetch the dataset id, which we will need later
        result = self.sess.query(ResultSet).filter(
                ResultSet.id == pk,
            ).first()

        if result is None:
            print("result set id " + pk + " does not exist")
            return False

        dsid = result.dataset_id

        # iterate through topics
        for topic in analysis['topics_stats']:
            success = self.__StoreTopic(pk, topic)
            if not success:
                print('Could not store topic')
                return False

        # iterate through instructor analysis
        for instr in analysis['instructor_stats']:
            success = self.__StoreInstr(pk, instr)
            if not success:
                print('could not store instructor analysis')
                return False

        # single commit for the full insert
        self.sess.commit()
        return True

    def __StoreTopic(self, pk, topic):
        new_record = ResultTopic(
                result_id = pk,
            )
        self.sess.add(new_record)
        self.sess.flush()
        topic_pk = new_record.id
        
        # Store the Comment Sentiments
        for topic_sent in topic['comments']: #positive, neutral, negative
            for topic_comment in topic['comments'][topic_sent]:
                success = self.__StoreCourseComment(topic_pk, topic_comment, topic_sent)
                if not success:
                    print('Failed to store topic sentiments')
                    return False

        # Store the Topic Words
        for topic_word in topic['topic_words']:
            new_record = TopicWord(
                topic_id = topic_pk,
                word = topic_word,
            )
            self.sess.add(new_record)
        
        self.sess.flush()
        return True

    def __StoreCourseComment(self, topic_pk, topic_comment, topic_sent):
        # topic_comment is the actual string text of the comment
        # what we need is the pk from the comments table
        # we need to find the right one, based on the dataset that was analyzed
        # it could even be more than one (identical words), in which case
        # we'll store both (all)
        query = self.sess.query(Comment.id).filter(db.and_(
                Comment.c_com == topic_comment,
                ResultTopic.id == topic_pk,
            ))
        query = query.join(CommentDataSet)
        query = query.join(DataSet)
        query = query.join(ResultSet)
        query = query.join(ResultTopic)
        result = query.all()

        if result is None:
            print('could not find comment id for: ' + topic_comment)
            return False

        for comment_pk in result:
            new_record = ResultCourseComment(
                    topic_id = topic_pk,
                    comment_id = comment_pk.id,
                    course_com_sent = topic_sent,
                )
            self.sess.add(new_record)
            
        self.sess.flush()

        return True

    def __StoreInstr(self, result_pk, instr):
        # Store the Comment Sentiments
        for inst_sent in instr['comments']: #positive, neutral, negative
            for inst_comment in instr['comments'][inst_sent]:
                success = self.__StoreInstrComment(
                                    result_pk, 
                                    inst_comment, 
                                    inst_sent, 
                                    instr['course_num_sect_id'], 
                                    instr['instructor_last_name'], 
                                    instr['instructor_first_name'],
                                )
                if not success:
                    print('Failed to store instructor comment')
                    return False

        return True

    def __StoreInstrComment(self, result_pk, inst_comment, inst_sent, 
                            num_sec, i_last, i_first):
        # topic_comment is the actual string text of the comment
        # what we need is the pk from the comments table
        # we need to find the right one, based on the dataset that was analyzed
        # it could even be more than one (identical words), in which case
        # we'll store both, but we'll also deduplicate as we go
        query = self.sess.query(Comment.id).filter(db.and_(
                Comment.i_com == inst_comment,
                ResultSet.id == result_pk,
                Instructor.last_name == i_last,
                Instructor.first_name == i_first,
                Course.num_sec == num_sec,
            ))
        query = query.join(Instructor)
        query = query.join(Course)
        query = query.join(CommentDataSet)
        query = query.join(DataSet)
        query = query.join(ResultSet)
        result = query.all()

        if result is None:
            print('Could not find comment id for inst comment: ' + inst_comment)
            return False

        for comment_pk in result:
            new_record = ResultInstructorComment(
                    result_id = result_pk,
                    comment_id = comment_pk.id,
                    instr_com_sent = inst_sent,
                )
            self.sess.add(new_record)
            
        self.sess.flush()

        return True

    def GetId(self, comments, topics, words, num_it):
        # retrieve result set
        # if result set exists, return it
        # if result doesn't exist, return the primary key
        dataset = DbDataset()
        dsid = dataset.GetId(comments)
        sw = DbStopword()
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

    def Query(self, pk):
        # get criteria to return with the analysis
        query = self.sess.query(ResultSet)
        query = query.filter(ResultSet.id == pk)
        result = query.first()
        if result is None:
            print('Result set id ' + str(pk) + ' does not exist')
            return False

        response = {}
        response['result_id'] = pk
        criteria = {}
        criteria['document_id_number'] = result.dataset_id
        criteria['user_selected_number_topics'] = result.topic_cnt
        criteria['user_selected_number_iterations'] = result.iterations
        criteria['user_selected_words_per_topic'] = result.word_cnt
        response['meta_file_info'] = criteria
        response['results'] = {}
        response['results']['topics_stats'] = []
        response['results']['instructor_stats'] = []

        # get the topics, words, comments, and sentiments
        # if we don't have any topics, that must mean there's no result
        query = self.sess.query(ResultTopic)
        query = query.filter(ResultTopic.result_id == pk)
        result = query.all()
        if not result:
            print('Analysis has not been performed for result set ' + str(pk))
            return False

        for row in result:
            topic = {}
            topic['comments'] = {}
            topic['comments']['positive'] = []
            topic['comments']['neutral'] = []
            topic['comments']['negative'] = []
            topic['words'] = []
            #fetch comments
            query = self.sess.query(
                    Comment.c_com, 
                    ResultCourseComment.course_com_sent,
                )
            query = query.filter(ResultCourseComment.topic_id == row.id)
            query = query.join(ResultCourseComment)
            topic_result = query.all()
            for comment in topic_result:
                topic['comments'][comment.course_com_sent].append(comment.c_com)

            #fetch words
            query = self.sess.query(TopicWord)
            query = query.filter(TopicWord.topic_id == row.id)
            topic_result = query.all()
            for word in topic_result:
                topic['words'].append(word.word)

            response['results']['topics_stats'].append(topic)

        # get the instructor comments and sentiments
        query = self.sess.query(
                        Course.num_sec,
                        Instructor.first_name,
                        Instructor.last_name,
                    )
        query = query.filter(ResultInstructorComment.result_id == pk)
        query = query.join(Comment)
        query = query.join(Instructor)
        query = query.join(ResultInstructorComment)
        print(query)
        result = query.distinct().all()
        if not result:
            # No instructor comments, nothing else to be done
            return response

        for row in result:
            instcom = {}
            instcom['course_num_sect_id'] = row.num_sec
            instcom['instructor_last_name'] = row.last_name
            instcom['instructor_first_name'] = row.first_name
            comlist = {}
            comlist['positive'] = []
            comlist['neutral'] = []
            comlist['negative'] = []

            query = self.sess.query(
                    Comment.i_com,
                    ResultInstructorComment.instr_com_sent,
                )
            query = query.filter(db.and_(
                    ResultInstructorComment.result_id == pk,
                    Course.num_sec == row.num_sec,
                    Instructor.first_name == row.first_name,
                    Instructor.last_name == row.last_name,
                ))
            query = query.join(Course)
            query = query.join(Instructor)
            query = query.join(ResultInstructorComment)
            #print(query)
            instr_result = query.all()
            for comment in instr_result:
                comlist[comment.instr_com_sent].append(comment.i_com)

            instcom['comments'] = comlist
            response['results']['instructor_stats'].append(instcom)
        
        return response

    def GetCommentIDs(self, result_id):
        query = self.sess.query(CommentDataSet.comment_id)
        query = query.filter(ResultSet.id == result_id)
        query = query.join(DataSet)
        query = query.join(ResultSet)
        result = query.all()
        response = []
        for comment in result:
            response.append(comment.comment_id)
        return response

    def __init__(self):
        self.sess = DbSession()
