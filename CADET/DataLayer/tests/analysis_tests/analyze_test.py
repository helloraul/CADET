import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from cadetapi.controllers.analysis.DatasetAnalysis import DatasetAnalysis as Analyzer
from cadetapi.controllers.database.DbControl import DbResult, DbDataset

if __name__ == '__main__':

    analyzer = Analyzer(1, 3, 3, 30)
    analyzer.runAnalysis()

    print("********Course Comments**********")
    for comment in analyzer.getCourseCommentList():
        print(comment.__dict__)
        print('')

    print("********Instructor Comments**********")
    for comment in analyzer.getInstructorCommentList():
        print(comment.__dict__)
        print('')

    print("********Topic Sentiment**********")
    print(analyzer.getTopicSentimentHistogram())
    print('')

    print("********Instructor Sentiment**********")
    print(analyzer.getInstructorSentimentHistogram())
    print('')

    print("********Topic Model**********")
    print(analyzer.getTopicModel())
    print('')

    topics = { 0: ['comment1', 'comment2', 'comment3'], 1: ['comment1', 'comment2', 'comment3'] }


    print("Attempt output formatting")

    results = analyzer.getResults()
    comments = DbDataset().Query(1)
    dataset_id = DbResult().GetId(comments, 5, 3, 31)
    DbResult().StoreAnalysis(dataset_id, results)
    results = DbResult().Query(dataset_id)
    print('\n\ngetting results...\n\n')

    for thing in results['results']['topics_stats']:
        print(thing)
    for thing in results['results']['instructor_stats']:
        print(thing)
