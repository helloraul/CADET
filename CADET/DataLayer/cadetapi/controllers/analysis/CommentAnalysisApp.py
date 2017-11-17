"""
CommentAnalysisApp: use QT python for GUI components
PROGRAM STARTS HERE
The main GUI window is set up when the ApplicationWindow is initialized

"""

from __future__ import unicode_literals

from FileIngesterUtil import FileIngesterUtil
from GraphCanvas import BarGraphCanvas, TimeBarGraphCanvas
from SaveFile import PopupSave
from TopicModelOptionsWindow import TopicModelOptions
from FileImportMenu import FileImportMenu
from Comment import Comment
#import multiprocessing

import sys

import time
import threading
import copy

from PyQt5 import QtCore, QtGui, QtWidgets


class ApplicationWindow(QtWidgets.QMainWindow):

    main_layout = None
    progressBar = None
    topicModelOptionsWidget = None # menu for entering topic model params.
    main_tab_pane = None
    courseTabs = []  #tabs displaying data about the overall course
    instructorTabs = [] #tabs displaying data about the instructors
    fileUtilArray = []

	
	
    def __init__(self):  #initialize the main GUI window here
	    QtWidgets.QMainWindow.__init__(self)
	    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	    self.setWindowTitle("application main window")
	    self.setGeometry(QtCore.QRect(100, 100, 600, 400))
	    self.file_menu = QtWidgets.QMenu('&File', self)
		
	    #drop down menu opotions
	    self.file_menu.addAction('&Open', self.displayFileMenu, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
	    self.file_menu.addAction('&Save', self.createSave, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
	    self.file_menu.addAction('&Quit', self.fileQuit,QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
	    
	    self.menuBar().addMenu(self.file_menu)

	    self.help_menu = QtWidgets.QMenu('&Help', self)
	    self.menuBar().addSeparator()
	    self.menuBar().addMenu(self.help_menu)

	    self.help_menu.addAction('&About', self.about)

	    self.main_widget = QtWidgets.QWidget(self)

	    self.main_widget.setFocus()
	    self.setCentralWidget(self.main_widget)
		
	    self.main_tab_pane = QtWidgets.QTabWidget()
		
	    self.courseTabLayout = QtWidgets.QGridLayout()
	    self.instructorTabLayout = QtWidgets.QGridLayout()
	    
	    self.courseTabPane = QtWidgets.QTabWidget()#Init. tab layouts
	    self.courseTabPane.setMovable(True)
	    self.instructorTabPane = QtWidgets.QTabWidget()
	    self.instructorTabPane.setMovable(True)
		
	    self.courseTab = QtWidgets.QWidget()
	    self.courseTab.setLayout(self.courseTabLayout)
		
	    self.instructorTab = QtWidgets.QWidget()
	    self.instructorTab.setLayout(self.instructorTabLayout)
	   
	    self.main_tab_pane.addTab(self.courseTab, "Overview")
	    self.main_tab_pane.addTab(self.instructorTab, "Instructor")
		
	    self.main_layout = QtWidgets.QGridLayout(self.main_widget)
	
	
	
	#open the save file dialog
    def createSave(self):
	    if len(self.fileUtilArray) >= 1:  #must have file loaded in order to save
		    #print ("Opening a new popup window...")
		    
		    self.w = PopupSave(fileUtilArray=self.fileUtilArray, courseSentimentArray=self.courseSentimentArray,instructorSentimentArray=self.instructorSentimentArray)
		    self.w.setGeometry(QtCore.QRect(100, 100, 350, 100))
		    self.w.show() # display save popup window
	    else:
		    print("No data to save: please load file first.")
	

	
	#open a dialog for creating the topic model 
    def openTopicModelOptions(self):    
	    self.topicModelOptionsWidget = TopicModelOptions()  
	    self.topicModelOptionsWidget.setGeometry(QtCore.QRect( 100, 100, 280, 300 ) )
	    self.topicModelOptionsWidget.exec_()
	
	
    fileUtilArray = []	# array containing FileIngesterUtil objs for each file loded
    fileIndexer = -1    #used for indexing files and assigning fileId numbers to each FileIngesterUtil
	
#	displayFileMenu()
#		have the fielMenuWidget open and get user input files
    def displayFileMenu(self):
	    self.openFileMenuWidget = FileImportMenu()
	    self.openFileMenuWidget.exec_() # display the fileMenu dialog
	    fileNames = self.openFileMenuWidget.getFileNames() # get user input (list of file names)
	    self.openFileMenuWidget.clearAll() # wipe clean for later use
	    #print("FileNames = ", fileNames)
		
	    if fileNames is not None and len(fileNames) > 0:
		    self.clearAll()
    
	    hasNonJSON = False # if there are only JSON file we don't need to display a progressBar
	    for file in fileNames:
		    if file.endswith('.txt') or file.endswith('.xlsx'):
			    self.openTopicModelOptions() #get topic model params from the user
			    hasNonJSON = True
			    break # we break b/c we only need input from the user once.

	    for file in fileNames: # call open file on each fileName to begin ingest and analysis
		    self.openFile(file)

	    largestFile = 0 #the largestFile is used to calibrate the progress bar timer (the larger the file, the more time on the progress bar)
	    for fileUtil in self.fileUtilArray:
		    if largestFile < len(fileUtil.getCommentList()):
			    largestFile = len(fileUtil.getCommentList())
		
	    self.courseSentimentArray = [None]*len(self.fileUtilArray)
	    self.instructorSentimentArray = [None]*len(self.fileUtilArray)
		
	    if hasNonJSON:# only need progress bar if there are non JSON files to load
		    self.progressBar = QtWidgets.QProgressBar()
		    self.progressBar.setFixedSize(300,20)
		    self.progressBar.setGeometry(100, 100, 100, 10)
		    self.main_layout.addWidget(self.progressBar)
		    self.progressBar.show()
		    self.updateProgressBar(largestFile)
		    #t = threading.Thread( target=self.updateProgressBar, args=(largestFile,) )
		    #t.start()  #thread to update progress bar
	    else:
		    self.main_layout.addWidget(self.main_tab_pane)

	
	
	
	
	
	
    def openFile(self, fileName): 
		
	    if fileName.endswith('.txt') or fileName.endswith('.xlsx'): # load from .txt or excel file 	
		    self.courseTabs.append(QtWidgets.QWidget())		
		    num_topics = self.topicModelOptionsWidget.getNumTopics()
		    num_words = self.topicModelOptionsWidget.getNumWords() 
		    num_iterations = self.topicModelOptionsWidget.getNumIterations()
		    self.fileIndexer +=1 
			
		    fileUtil = FileIngesterUtil(fileName, num_topics=num_topics, words_per_topic=num_words, iterations=num_iterations)
		    fileUtil.setFileID(self.fileIndexer)
		    self.fileUtilArray.append( fileUtil )
		    fileUtil.finished.connect( self.finishedAnalysis )
		    fileUtil.start()   #call run() method in FileIngesterUtil (overrided from QThread)
			

		
		#b/c json files could contain many semesters worth of data with no needed analysis, we open and initialize here.
	    elif fileName.endswith('.json'): #load from save json file
		    import json
		    from collections import OrderedDict
	
		    file = open(fileName,'r')
		    file_count = int(file.readline()) #get number of semesters (number of files saved)
		    commentList_raw = []
		    courseCommentList = []
		 
		    for i in range(0, file_count):
			    self.fileIndexer += 1
			    
			    self.courseTabs.append(QtWidgets.QWidget())
			    fileUtil = FileIngesterUtil(fileName) # add file to list
			    title = file.readline()[6:].rstrip()  # get name of file ex: 'Fall2015'
				
			    self.courseSentimentArray.append(None) # initialize index,- will store data about each file
			    self.instructorSentimentArray.append(None)
				
			    course_sentiment_histogram = json.loads(file.readline()[7:].rstrip(), object_pairs_hook=OrderedDict) #init course_sentiment_histogram dict
			    topic_model = json.loads(file.readline()[7:].rstrip(), object_pairs_hook=OrderedDict) # init topic_model dict
			    commentList_raw = json.loads(file.readline()[7:].rstrip())  # get comments as list of dictionaries
			    
			    for comment in commentList_raw: # init the Comment objs and store in a list
				    commentObj = Comment(commentDict=comment)
				    courseCommentList.append(commentObj)
				
			    instructor_rawText = file.readline()[12:]  #get instructor comments as list of dictionaries
			    
			    if instructor_rawText != "": # see if instructor data was available
				    instructorCommentList_raw = json.loads(instructor_rawText)
				    instructorCommentList = []				
				    for comment in instructorCommentList_raw:  #init instructor Comments objs and store in a list
					    commentObj = Comment(commentDict=comment) 
					    instructorCommentList.append(commentObj)
			    
				    instructorSentimentHistogram = json.loads(file.readline()[12:]) #init instructorSentimentHistogram as dict
				    fileUtil.setInstructorComments(instructorCommentList)  #store in fileUtil
				    fileUtil.setInstructorSentimentHistogram(instructorSentimentHistogram)
				#Begin to init FileIngesterUtil attributes
			    fileUtil.setFileTitle(title[:-1])
			    fileUtil.setCourseSentimentHistogram(course_sentiment_histogram)
			    fileUtil.setTopicModel(topic_model)
			    fileUtil.setCourseComments(courseCommentList)
			    
			    fileUtil.setFileID(self.fileIndexer)
			    #print("file indexer =", self.fileIndexer)
			    self.fileUtilArray.append(fileUtil)
			    fileUtil.setDisplayed(True)
			    self.addWidgets(fileUtil, fileNum=self.fileIndexer)
				
			    self.courseTabLayout.addWidget(self.courseTabPane)
			    self.instructorTabLayout.addWidget(self.instructorTabPane)
		        
			    self.main_layout.addWidget(self.main_tab_pane)
			    self.numFilesLoaded += 1
			    file.readline()
				     
		
	    elif len(fileName) == 0: #no file was selected
		    return 
		
	    else: #file was of wrong type 
		    print("Error: File must be type: .txt, .xlsx or from saves .json")


	
    courseSentimentArray = list()
    instructorSentimentArray = list()
    instructorNameList = ["All"] # list of instructor names (used to set the dropdown combobox)
	
	# Adds the graph and topic model to the screen 
    def addWidgets(self, fileUtil, fileNum):
	    print("fileIdIndex = ", fileNum, "number of courseTabs = ", len(self.courseTabs) )
		
		#Copy dictionaries by value and store in lists (Will be needed for writing to save file)
	    self.courseSentimentArray[fileUtil.getFileID()] = copy.deepcopy(fileUtil.getTopicHistogram())
	    self.instructorSentimentArray[fileUtil.getFileID()] = copy.deepcopy(fileUtil.getInstructorSentimentHistogram())
		
	    topicModelLabel = QtWidgets.QLabel(self)
	    topic_model = fileUtil.getTopicModel() #dict {topic_ID, list(words in that topic) }
	    labelText =""
		
	    for key in topic_model.keys():  #Format topic model in one string and put in a label
		    labelText += "\n"
		    labelText+="Topic id = "+str(key)+"\n"
		    for i in range (0, len(topic_model.get(key))):
			    labelText+=topic_model.get(key)[i]+"\n"
	    topicModelLabel.setText(labelText)  #add text to label
	     
	    courseHistogramGraph = BarGraphCanvas(self.main_widget, width=5, height=4, dpi=100, fileUtil=fileUtil) #get Graph widget
		
	    if fileUtil.hasInstructorData:   #if there is data about the instructors available
		    instructorHistogramGraph = BarGraphCanvas(self.main_widget, width=5, height=4, dpi=100, fileUtil=fileUtil, setInstructorGraph=True)
		    instructorLayout = QtWidgets.QGridLayout()
		    instructorTab = QtWidgets.QWidget()
		    self.instructorTabs.append(instructorTab)
		    instructorTab.setLayout(instructorLayout)
		    self.comboBox = QtWidgets.QComboBox(self)
			
			#get total list of instructor names from all semesters loaded 
		    self.instructorNameList += list(fileUtil.getInstructorSentimentHistogram().keys())
	
		    if self.numFilesLoaded == self.fileIndexer: 
				#sort list of instructors and remove repeats
			    self.instructorNameList = sorted( list(set(self.instructorNameList)), key=str.lower)
			    self.comboBox.addItems(self.instructorNameList)
				
		    self.comboBox.currentIndexChanged.connect(self.comboSelectionChange)
		    self.comboBox.setFixedSize(200, 20)
		    self.instructorTabPane.addTab(instructorTab, fileUtil.getFileTitle() )
			
		    self.instructorTabLayout.addWidget(self.comboBox, 0, 0) #comboBox goes above courseTabs 
		    instructorLayout.addWidget(instructorHistogramGraph, 1, 1)
			
			
	    tabLayout = QtWidgets.QGridLayout()
	    self.courseTabs[fileNum].setLayout(tabLayout)

	    self.courseTabPane.addTab(self.courseTabs[fileNum], fileUtil.getFileTitle() )
	    tabLayout.addWidget(courseHistogramGraph, 0, 0)
	    tabLayout.addWidget(topicModelLabel, 0, 1)

		
    numFilesLoaded = 0
	
    #Method is called when the FileIngesterUtil thread terminates. Calls addWidgets() to display graphs
    def finishedAnalysis(self, file=0):
	    print("Number of courseTabs = ",len(self.courseTabs) )
	    print("In finishedAnalysis", file)
	    print("size of array = ", len(self.fileUtilArray), "  at index = ", self.numFilesLoaded)
		
	    for fileUtil in self.fileUtilArray:
		    if fileUtil.hasFinishedLoad and fileUtil.isDisplayed != True:
			    #print("Indexing at ",self.numFilesLoaded, " FInishAnalysis topicHistogram =", fileUtil.getTopicHistogram() )
			    self.addWidgets(fileUtil=fileUtil, fileNum=self.numFilesLoaded)
			    fileUtil.setDisplayed(True)
	    
	    if self.numFilesLoaded == self.fileIndexer: # once all files loaded, close the progress bar
		    print("self.numFilesLoaded = ", self.numFilesLoaded, "self.fileIndexer = ", self.fileIndexer)
		    self.progressBar.close()
		    self.progress_count = 100

	    
	    self.courseTabLayout.addWidget(self.courseTabPane)
	    self.instructorTabLayout.addWidget(self.instructorTabPane)
		
	    self.main_layout.addWidget(self.main_tab_pane)
	    self.numFilesLoaded += 1
	
	
#	comboBoxChange()	
#		detects changes in the doropdown list of instructor names. And will 
#		display another tab with a graph of that instructor
    def comboSelectionChange(self, i):
	    selected_name = self.instructorNameList[i]  #get the instructor name from selected index
	    print("selected-name = ", self.instructorNameList[i])
		
	    instructor_grid_layout = QtWidgets.QGridLayout()
	    singleInstructorTab = QtWidgets.QWidget()
	    self.instructorTabs.append(singleInstructorTab)
	    singleInstructorTab.setLayout(instructor_grid_layout)
		
	    if selected_name != "All": #add new tab with graph
		    instructor_line_graph = TimeBarGraphCanvas(fileUtilArray=self.fileUtilArray, instructorName=selected_name)
			
		    instructor_grid_layout.addWidget(instructor_line_graph)
		    self.instructorTabPane.addTab(singleInstructorTab , selected_name)	
		   
		
#	updateProgressBar
#		SHows progress bar updating while files load
#		Note: prgress bar updates with a timer
    def updateProgressBar(self, largestFile):
	    self.progress_count = 0
	    print("In update progressBar")
	    speed = largestFile / 250
		
	    while self.progress_count < 100:
		    time.sleep(speed)
		    QtWidgets.qApp.processEvents()
		    self.progressBar.setValue(self.progress_count)
		    self.progress_count += 1
			

	    #print("Done progress bar")

		
    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

	#Show message box with help text when user selects the help menu option 
    def about(self):
	    message = 'On Start: Go to File->Open and select either a previously saved json file or load a new student-comment txt/xlsx file'
	    QtWidgets.QMessageBox.about(self, "About", message)

#	clearAll
#each time a new file is loaded, window is cleared out and all variables set to 0 or null
    def clearAll(self):
	    self.fileId = 0
	    self.fileIndexer = -1
	    self.fileUtilArray.clear()
	    self.numFilesLoaded = 0
	    self.instructorSentimentArray.clear()
	    self.courseSentimentArray.clear()
		
	    for i in range(0,self.courseTabPane.count()):
		    self.courseTabPane.removeTab(i)
			
	    for i in range(0, self.instructorTabPane.count()):
		    print("removeing tab...")
		    self.instructorTabPane.removeTab(i) 
				    
	    for i in reversed(range(self.instructorTabLayout.count())): 
		    self.instructorTabLayout.itemAt(i).widget().setParent(None)

	    for i in reversed(range(self.courseTabLayout.count())): 
		    self.courseTabLayout.itemAt(i).widget().setParent(None)
		   
	    for i in range(0, len(self.courseTabs) ):
		    self.courseTabs[i].setParent(None)  
	    for i in range(0, len(self.instructorTabs)):
		    self.instructorTabs[i].setParent(None)
		
	    self.instructorTabs.clear()		
	    self.courseTabs.clear()
	    self.courseTabs = None
	    self.courseTabs = []
	    self.instructorTabPane.setParent(None)
	    self.courseTabPane.setParent(None)
	    self.instructorTabLayout.removeWidget(self.instructorTabPane)
		
	    self.courseTabLayout.removeWidget(self.courseTabPane)

if __name__ == '__main__':
  

        
        qApp = QtWidgets.QApplication(sys.argv)
        
        aw = ApplicationWindow()
        aw.setWindowTitle("%s" % "Student Survey Analysis App")
        aw.show()
        aw.raise_()
        aw.activateWindow()
        sys.exit(qApp.exec_())

