# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:39:26 2016

@author: mcnambm1
##Sentiment module using twinward sentiment analysis api

##  example: >>import SentimentModule_twinward_api as S
             >>print(S.sentiment("..Write your comment here.."))
"""
import requests
        
def sentiment(comment):

    response = requests.post("https://twinword-sentiment-analysis.p.mashape.com/analyze/", 
      
      headers={
        "X-Mashape-Key": "xuR4UeC5hcmshngemuvKzCgw5hyqp1IHrDDjsnSAsHtKcBFTx7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      },
      params={
        "text": comment
      },
      timeout=5
    )

    willDecode = True
    headers={"X-Mashape-Key": "xuR4UeC5hcmshngemuvKzCgw5hyqp1IHrDDjsnSAsHtKcBFTx7","Content-Type": "application/x-www-form-urlencoded","Accept": "application/json"}
    while willDecode:
	    try: 
		    j = response.json()
		    willDecode = False
	    except ValueError:
		    response = requests.post("https://twinword-sentiment-analysis.p.mashape.com/analyze/", headers=headers, params={"text": comment})
		    pass
			
    classification = j["type"]
	
    if float(j["score"]) < 0.0:
	    classification = "negative"
    elif float(j["score"]) <= .212:
	    classification = "neutral"
    else:
	    classification = "positive"
		
    if float(j["score"]) < 0.212 and float(j["ratio"]) < 0.5:
         classification = "negative"

    return classification
