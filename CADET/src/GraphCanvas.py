
from numpy import arange
from CommentDialog import CommentDialog
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#from matplotlib.backends import qt_compat
import sys
from FileIngesterUtil import FileIngesterUtil

#from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor

	
"""
BarGraphCanvas (class for creating graphs)

If setInstructorGraph is set to true, then we get the instructor sentiment histograms from the given 
FileIngesterUtil obj, instead of the topic_sentiment_histogram.

"""	
#File for creating python matlab plots as QT FigureCanvases	
#displaying graph as a QtWidget obj

class BarGraphCanvas(FigureCanvas): 

    p1 = None
    p2 = None
    p3 = None
    fileUtil = None
    topic_sentiment_histogram = {}
    commentList = list()
    setInstructorGraph = False
	
    def __init__(self, parent=None, width=10, height=4, dpi=100, fileUtil=None, setInstructorGraph=False):
	
	    self.fileUtil = fileUtil
	    xLabel = ''
	    range = 100
	    title = ""
	    self.setInstructorGraph = setInstructorGraph
	
	    self.topic_sentiment_histogram.clear()
		
	    if setInstructorGraph==True: # get instructor data
		    self.topic_sentiment_histogram = self.fileUtil.getInstructorSentimentHistogram()
		    self.commentList = self.fileUtil.getInstructorComments()
		    xLabel = "Instructor"
		    range = 40
		    title = "Instructor Sentiment Distribution"

		
	    else:  # get topic model data 	  
		    self.topic_sentiment_histogram = self.fileUtil.getTopicHistogram()
		    self.commentList = self.fileUtil.getCommentList()
		    xLabel = "Topic ID Number" 
		    title = "Topic Sentiment Distribution"
		    
			
	    #print("GraphCanvas ->Topic histogram =", self.topic_sentiment_histogram)	
	    fig2 = plt.figure()
	    
	    N = len(self.topic_sentiment_histogram)
	    ind = arange(N)
	    width = 0.2
	    x = []
	    y = []
	    z = []
	    w = []
	    #print("GraphCanvas sentiment_histogram = ", self.topic_sentiment_histogram) 
	    for key in self.topic_sentiment_histogram:  
		    x.append(key)
		    y.append(self.topic_sentiment_histogram.get(key)[0] )
		    z.append( self.topic_sentiment_histogram.get(key)[1] )
		    w.append( self.topic_sentiment_histogram.get(key)[2] )
	    
	    self.p1 = plt.bar(ind-width, y, width=width, color='b', align='center')
	    self.p2 = plt.bar(ind, z, width=width, color='r', align='center')
	    self.p3 = plt.bar(ind+width, w, width=width, color='g', align='center')
		
	    plt.autoscale(tight=True)
	    plt.title(title)
		
	    if setInstructorGraph==True:
		    plt.xticks(ind, self.topic_sentiment_histogram.keys(), rotation=80)
	    else:
		    plt.xticks(ind, self.topic_sentiment_histogram.keys())
			
	    plt.ylabel('Number of Comments')
	    plt.xlabel(xLabel)
	    
	    plt.yticks(arange(0, range, 10))

	    plt.legend( (self.p1[0], self.p2[0], self.p3[0]), ('Positive', 'Negaitve', 'Neutral') )
	    
	    self.axes = fig2.add_subplot(111)
	    # We want the axes cleared every time plot() is called
	    self.axes.hold(False)
	
	    self.compute_initial_figure()
	    fig2.tight_layout()
	    
	    FigureCanvas.__init__(self, fig2)
	    self.setParent(parent)
		
	    if self.commentList: #only allow if there are comments available 
		    cid = fig2.canvas.mpl_connect('button_press_event', self.onclick)
			
	    FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
	    FigureCanvas.updateGeometry(self)
	    
		
    def compute_initial_figure(self):
	    pass
	
	#when a bar has been clicked, we determin which x-index it is  (pos, neg, or neutral)
	# Then determin which bar index was clicked
	#send information to the "about" method for displaying
    def onclick(self, event):    
	    for i in range(0, len(self.p1)):			
		    if self.p1[i].contains(event)[0]:
			    self.about("positive", i)
			    return
				
	    for i in range(0, len(self.p2)):
		    if self.p2[i].contains(event)[0]:
			    self.about("negative", i)
			    return 
				
	    for i in range(0, len(self.p3)):
		    if self.p3[i].contains(event)[0]:
			    self.about("neutral", i)
			    return

#	display a custom dialog box, that will display the comments
    def about(self, classifier, topic_id):
	    
	    message = ""
	    x_axis_tick = list(self.topic_sentiment_histogram.keys())[topic_id]
	    for i in range(0, len(self.commentList)):
		    
		    if self.setInstructorGraph:
			    if str(self.commentList[i].getInstructorName()) == str(x_axis_tick) and self.commentList[i].getSentimentClass() == classifier:
				    message += "--"
				    message += self.commentList[i].getComment()
				    message += "\n\n"
		    else:
			    if str(self.commentList[i].getTopicModleId()) == str(x_axis_tick) and self.commentList[i].getSentimentClass() == classifier:
				    message += "--"
				    message += self.commentList[i].getComment()
				    message += "\n\n"
	    dialog = CommentDialog(comment=message)
	    dialog.exec()


	
"""
TimeBarGraphCanvas: Class for showing graphs from mulitple FileIngesterUtil objs (data over multiple semesters)

-Graphs the sentiment histogram of a given instructor for as many FileUtilIngester objs available
"""
class TimeBarGraphCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=4, dpi=100, fileUtilArray=None, instructorName="", setInstructorGraph=False):
	   
	    fig = plt.figure()
	    plt.ylabel('Number of Comments')
	    range = 40

	    self.fileTitles = []
	    self.fileUtilArray = fileUtilArray
	    self.instructorName = instructorName

	    y = []
	    z = []
	    w = []
	    file_count = 0
	    for fileUtil in fileUtilArray: # for each semester
		    if fileUtil.hasInstructorData:  # if there is data available 
			    if fileUtil.getInstructorSentimentHistogram().get(instructorName) is not None: #if the instructor worked that semester
				    # each index of the array is a semester, three arrays for three types of sentiment classification
				    y.append(fileUtil.getInstructorSentimentHistogram().get(instructorName)[0] ) #add to total sentiment bar
				    z.append(fileUtil.getInstructorSentimentHistogram().get(instructorName)[1] )
				    w.append(fileUtil.getInstructorSentimentHistogram().get(instructorName)[2] )
				    self.fileTitles.append(fileUtil.getFileTitle())
				    file_count += 1
			
	    ind = arange(file_count)	
	    width = 0.3
		#initialize three bars 
	    self.p1 = plt.bar(ind-width, y, width=width, color='b', align='center') 
	    self.p2 = plt.bar(ind, z, width=width, color='r', align='center')
	    self.p3 = plt.bar(ind+width, w, width=width, color='g', align='center')
		
	    plt.legend( (self.p1[0], self.p2[0], self.p3[0]), ('Positive', 'Negaitve', 'Neutral') )
	    plt.xticks(ind, self.fileTitles)	
	    plt.title(instructorName)
	    plt.yticks(arange(0, range, 10))
	    self.axes = fig.add_subplot(111)
	    self.axes.hold(False)

	    
		
	    FigureCanvas.__init__(self, fig)
	    self.setParent(parent)
		
	    FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
	    FigureCanvas.updateGeometry(self)
	    cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
	
	#when a bar has been clicked, we determin which x-index it is  (pos, neg, or neutral)
	# Then determin which bar index was clicked
	#send information to the "about" method for displaying
    def onclick(self, event):    
	    
	    for i in range(0, len(self.p1)):			
		    if self.p1[i].contains(event)[0]:
			    self.about("positive", i)
			    return
				
	    for i in range(0, len(self.p2)):
		    if self.p2[i].contains(event)[0]:
			    self.about("negative", i)
			    return 
				
	    for i in range(0, len(self.p3)):
		    if self.p3[i].contains(event)[0]:
			    self.about("neutral", i)
			    return
	
#	display a custom dialog box, that will display the comments
    def about(self, classifier, x_axis_index):
	    
	    message = "" # get all comments as a string and send to the CommenDialog
	    x_axis_tick = self.fileTitles[x_axis_index]
	    for fileUtil in self.fileUtilArray:
		    if fileUtil.hasInstructorData:
			    instructorList = fileUtil.getInstructorComments()
			    for i in range(0, len(instructorList)):
				    if fileUtil.getFileTitle() == str(x_axis_tick) and instructorList[i].getInstructorName() == self.instructorName and instructorList[i].getSentimentClass() == classifier:
					    message += "--"
					    message += instructorList[i].getComment()
					    message += "\n\n"
	    dialog = CommentDialog(comment=message)
	    dialog.exec()
	   
