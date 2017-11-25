import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from cadetapi.controllers.analysis.DatasetAnalysis import DatasetAnalysis as Analyzer

if __name__ == '__main__':

    dataset_ids = [1,2,3]
    analyzer = Analyzer(dataset_ids, 3, 3, 5)
    analyzer.runAnalysis()
    
    print("********Course Comments**********")
    for comment in analyzer.getCourseCommentList():
        comment.show()
        print('')

    print("********Instructor Comments**********")
    for comment in analyzer.getInstructorCommentList():
        comment.show()
        print('')

    print("********Topic Sentiment**********")
    print(analyzer.getTopicSentimentHistogram())
    print('')

    print("********Instructor Sentiment**********")
    print(analyzer.getInstructorSentimentHistogram())
    print('')

    print("********Topic Model**********")
    print(analyzer.getTopicModel())

