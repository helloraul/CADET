#Class FileIngester
#file for reading and parsing student comments

from PyQt5.QtCore import QThread
from Comment import Comment
from AnalysisModule import AnalysisModule
import re  # regular expressions
import openpyxl  #for reading in excel files 

"""
FileIngesterUtil: extends QThread so each file can perform analysis on its own thread

Class for reading and parseing txt and xlsx files. txt files are meant to only contain a list of comments
While xlsx files will have all data available about the course and instructors. Whatever data is available will be 
loaded and saved. Each FileIngesterUtil will have and AnalysisModule for doing computations on the data as well
"""

class FileIngesterUtil(QThread):
	'Class for reading and parsing files'
		
	num_topics = 0
	words_per_topic =0
	iterations = 0
	hasInstructorData = False
	
#	readAndParseTXT:
#		txt files are meant to just contain a list of comments about the course
#		So only a single topic model and sentiment histogram will be generated
	def readAndParseTXT(self): #text file
		file = open(self.fileName,'r')
		rawFileData = file.read()
		file.close()
		self.hasInstructorData = False
		self.comments = rawFileData.split("\n")
		self.comments = list(filter(None, self.comments))
		for comment in self.comments:
			comment = ''.join([i if ord(i) < 128 else ' ' for i in comment]) #remove all non-ascii characters
			self.commentList.append(Comment(comment=comment))
			self.text += comment
		print("Finished parsing file.")
		self.analysisModule = AnalysisModule(comments=self.comments, text=self.text, num_topics=self.num_topics, words_per_topic=self.words_per_topic, iterations=self.iterations)
		
		
#	readAndParseXLSX
#		method for reading in excel files. These will contain all info about the course.
#		From this we generate a topic model sentiment_histogram and sentiment histograms about each instructor		
	def readAndParseXLSX(self):  #excel file 
	       
	    work_book = openpyxl.load_workbook(self.fileName)
	    sheet = work_book.active
	    self.hasInstructorData = True 
	    notFirstRow = False # fist row of excel worksheet has only column headers, so we ignore
	    #sheet.columns = list(sheet.columns)
#	    print("sheet['A'] = ", sheet['A'])
            #print("sheet columns as a list = ", list(sheet.columns))
#	    print("sheet.columns = ", sheet.columns)
	    for courseComment, instructorComment, lname, fname in zip(sheet['G'], sheet['H'], sheet['F'], sheet['E']):
	    #for courseComment, instructorComment, lname, fname in zip(sheet.columns[6], sheet.columns[7], sheet.columns[5], sheet.columns[4]):
		    if courseComment.value is not None and notFirstRow:
		        self.commentList.append(Comment(comment=courseComment.value))
		        self.comments.append(courseComment.value)
		        self.text += str(courseComment.value)
		        self.text+= " "
		    
		    if instructorComment.value is not None and notFirstRow:
			    name = lname.value+" ."+fname.value[:1]
			    if name in self.instructor_comments:
				    self.instructor_comments.get(name).append(instructorComment.value)
			    else:
				    self.instructor_comments[name] = []
				    self.instructor_comments.get(name).append(instructorComment.value)
					
		    notFirstRow = True
			
		
	    self.comments = list(filter(None, self.comments))
	    
	    print("Number of instructor comments", len(self.instructor_comments))
	    print("Finish parsing file.")
	    self.analysisModule = AnalysisModule(comments=self.comments, text=self.text, instructor_comments=self.instructor_comments, num_topics=self.num_topics, words_per_topic=self.words_per_topic, iterations=self.iterations)


	def getInstructorComments(self):
		return self.instructorCommentList
	
	def getInstructorSentimentHistogram(self):
		return self.instructor_sentiment_histogram
		
	def getTopicModel(self):
		return self.topic_model
		
	def getTopicHistogram(self):
		return self.topic_sentiment_histogram
	
	def getNumberofComments(self):
	    return len(self.comments)
	
	def getCommentList(self):
		return self.commentList
			
	def setFileID(self, fileId):
		self.fileId = fileId

	def getFileID(self):
		return self.fileId
	
	def getFileName(self):
		return self.fileName
	
	isDisplayed= False
	def setDisplayed(self, isDisplayed):
		self.isDisplayed = isDisplayed
	
	def isDisplayed(self):
		return self.isDisplayed;
	
	def hasInstructorData(self):
		return self.hasInstructorData
		
	def setCourseSentimentHistogram(self, courseSentimentHistogram):
	    self.topic_sentiment_histogram = courseSentimentHistogram
		
	def setTopicModel(self, topicModel):
		self.topic_model = topicModel
		
	def setCourseComments(self, courseComments):
	    self.commentList = courseComments
		
	def setInstructorComments(self, instructorComments):
	    self.hasInstructorData = True
	    self.instructorCommentList = instructorComments
		
	def setInstructorSentimentHistogram(self, instructorSentiment):
	    self.hasInstructorData = True
	    self.instructor_sentiment_histogram = instructorSentiment
	
	def setFileTitle(self, title):
	    self.fileTitle = title
		
	def getFileTitle(self):
	    return self.fileTitle + str(self.fileId)

	def hasFinishedLoad(self):
	    return self.hasFinishedLoad
		
	def run(self): #FileIngesterUtil extend QThread & run on separate threads 
	
		self.analysisModule.runAnalysis() # This will take time !!!!
		                                  # Once complete, we can get data 
										  
		self.topic_model = self.analysisModule.getTopicModel()
		self.topic_sentiment_histogram = self.analysisModule.getTopicHistogram()
		self.commentList = self.analysisModule.getCommentList()
		self.instructor_sentiment_histogram = self.analysisModule.getInstructorSentimentHistogram()
		self.instructorCommentList = self.analysisModule.getInstructorComments()
		self.hasFinishedLoad = True
		
		
	def __del__(self):
		self.wait()	
		
	def __init__(self, fileName, num_topics=5, words_per_topic=6, iterations=30):		
		QThread.__init__(self)
		self.text = ''
		self.hasInstructorData = False
		self.commentList = list()
		self.topic_sentiment_histogram={} #dictionary with < topic_id, [num_pos, num_neg, num_neutral] > mapping
		self.topic_model = {}
		self.analysisModule = {}
		self.fileId = -1
	
		self.comments = []
		self.instructor_comments ={}
		self.instructor_sentiment_histogram = {}
		self.instructorCommentList = list()
		
		self.fileTitle = ""
		
		#self.comments.clear()
		#self.topic_model.clear()
		#self.topic_sentiment_histogram.clear()
		#self.commentList.clear()
		#self.instructor_sentiment_histogram.clear()
		#self.instructorCommentList.clear()
		#self.instructor_comments.clear()
		
		self.fileName = fileName
		self.num_topics = num_topics
		self.words_per_topic = words_per_topic
		self.iterations = iterations
		self.hasFinishedLoad = False
		fileTitle = ""
		
		#Get title from the fileName
		if "fall" in fileName.lower():
		    fileTitle+="Fall"
		
		elif "spring" in fileName.lower():
			fileTitle+="Spring"
		
		elif "winter" in fileName.lower():
			fileTitle+="Winter"
		
		elif "summer" in fileName.lower():
			fileTitle+="Summer"
		
		#get the year from the fileName
		if fileName.endswith("txt") or fileName.endswith("xlsx"):
			year = "_"+re.search(r'[12]\d{3}', fileName).group()
			fileTitle += str(year)
			self.setFileTitle(fileTitle)

		
		if fileName.endswith(".txt"):
		    self.readAndParseTXT()

		elif fileName.endswith(".xlsx"):
		    self.readAndParseXLSX()

		
		print("Number of comments = ", len(self.comments), "   File title = ", self.fileTitle)
