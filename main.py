import re
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup as bs, BeautifulSoup
from urllib.parse import urlparse
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import praw
import time
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import tensorflow
import nltk
from wordcloud import WordCloud
import yfinance
import functions
import multiprocessing
import time

def getUserPass(wordList_):
    fileObj = open("C:\\Users\\Andre\\Documents\\txt.txt", "r", encoding='utf-8')  # pass info
    words = fileObj.read().splitlines()
    for i in words:
        wordList_.append(i)
    return wordList_
def getPinnedPost(subreddit_):
    for post in subreddit_.hot(limit=100):  # first n posts
        if post.stickied:  # if post pinned
            return post
    return None
def createListOfComments(subreddit_):
    local_list = []
    count = 0
    for submission in subreddit_.hot(limit=5):  # first n posts
        for comment in submission.comments:
            if hasattr(comment, "body"):
                count += 1
                # print(comment.body)
                local_list.append(comment.body)
    writeToFile(local_list, 'file')
    return local_list
def printSentimentList(full_list_):
    for i in range(len(full_list_)):
        blob = TextBlob(full_list_[i])
        if blob.sentiment.polarity > .2 or blob.sentiment.subjectivity > .2:
            print(f"Text {blob} [SENTIMENT: {blob.sentiment}")

            def returnSentimentList(full_list_):
                list_ = []
                for i in range(len(full_list_)):
                    blob = TextBlob(full_list_[i])
                    if blob.sentiment.polarity > .2 or blob.sentiment.subjectivity > .2:
                        list_.append(blob)
                return list_
def generateReddit(wordlist_):
    secretKey = wordlist_[0]  # api secret key
    personaluse = wordlist_[1]  # READ FROM FILE
    wanted_subreddits = []  # AUTO LOAD IN CONSTRUCTOR AS WELL?
    reddit = praw.Reddit(client_id=personaluse,
                         client_secret=secretKey,
                         user_agent="<console:HAPPY:1.0>",
                         username=wordlist_[2],
                         password=wordlist_[3]  # needed pass
                         )
    return reddit
def writeToFile(list, filename):
    textfile = open(f"{filename}.txt", "w", encoding='utf-8')
    #textfile.write('hello')
    for i in list:
        textfile.write(str(i) + ",\n")

    textfile.close()
def readFile(fileName):
    fileObj = open(fileName, "r", encoding='utf-8')
    words = fileObj.read().split("\n\n")  # Split by 2 new lines for paragraphs
    fileObj.close()
    return words
def wordCloud(frequencyCounter):
    wcloud = WordCloud().generate_from_frequencies(frequencyCounter)
    plt.imshow(wcloud, interpolation='bilinear')
    plt.show()
def populateWantedSubreddits(tickers_, subreddits_):
    wanted_subreddits_= []
    templist = []
    for i in range(len(tickers_)):
        for j in subreddits_[f'{tickers_[i]}']:  # get dict key
            tempsubreddit = reddit.subreddit(f"{j}")  # get individual subreddit
            templist.append(tempsubreddit)  # add to temp list
        wanted_subreddits_.append(templist)  # add temp list to fill list
        templist = []

    return wanted_subreddits_


def iterSubsEvaluate(wanted_subreddits_):
    for i in range(len(wanted_subreddits_)):
        print("/r/" + str(wanted_subreddits_[i]))
        createListOfComments(wanted_subreddits_[i])
        paragraphs = readFile("file.txt")
        functions.getRedditReviewValues2(paragraphs)

tickers = ['AMZN', 'TSLA']  # Add Tickers here
wordlist = []

subreddits = {'AMZN':
                ["FulfillmentByAmazon", "AmazonFBAHelp", "AmazonUnder25", "AmazonSeller"],
              'TSLA':
                ["TeslaMotors"]

              }

wordlist = getUserPass(wordlist)
reddit = generateReddit(wordlist)
wanted_subreddits = populateWantedSubreddits(tickers, subreddits)

for list in wanted_subreddits:
    iterSubsEvaluate(list)

#functions.StockSentimentAnalysis(tickers)
