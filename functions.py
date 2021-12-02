import praw
from textblob import TextBlob
from nltk.sentiment import vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from bs4 import BeautifulSoup as bs, BeautifulSoup
from urllib.request import urlopen, Request

def getRedditReviewValues2(list):
    vader = SentimentIntensityAnalyzer()
    total_neg = 0
    best = 0
    worst = 0

    blobAveragePolarity = 0
    blobAverageSubjectivity = 0
    for i in range(len(list)):
        text = (list[i])  # Gets the particular thing I want
        blob = TextBlob(text)  # use blbo to analys string

        blobAveragePolarity += blob.sentiment[0]
        blobAverageSubjectivity += blob.sentiment[1]

        currentValue = vader.polarity_scores(text)['compound']  # " "
        #print(currentValue)
        total_neg += currentValue
        if currentValue > best:
            best = currentValue
        elif currentValue < worst:
            worst = currentValue
    print("Blob Mean Polarity: " + str(blobAveragePolarity / len(list)))
    print("Blob Mean Subjectivity: " + str(blobAverageSubjectivity / len(list)))
    print("Num Reviews: " + str(len(list)))
    print("Mean Review: " + str(total_neg / len(list)))
    print("Best Review: " + str(best))
    print("Worst Review: " + str(str(worst)) + "\n")
def getVaderReviewValues(df):
    vader = SentimentIntensityAnalyzer()
    total_neg = 0
    best = 0
    worst = 0

    blobAveragePolarity = 0
    blobAverageSubjectivity = 0
    for i in range(len(df)):
        text = (df['Text'][i])  # Gets the particular thing I want
        blob = TextBlob(text)  # use blbo to analys string

        blobAveragePolarity += blob.sentiment[0]
        blobAverageSubjectivity += blob.sentiment[1]

        currentValue = vader.polarity_scores(text)['compound']  # " "
        total_neg += currentValue
        if currentValue > best:
            best = currentValue
        elif currentValue < worst:
            worst = currentValue
    print("Blob Mean Polarity: " + str(blobAveragePolarity / len(df)))
    print("Blob Mean Subjectivity: " + str(blobAverageSubjectivity / len(df)))
    print("Num Reviews: " + str(len(df)))
    print("Mean Review: " + str(total_neg / len(df)))
    print("Best Review: " + str(best))
    print("Worst Review: " + str(str(worst)) + "\n")


def fillDictWTickers(listOfTickers):
    finviz_URL = 'https://finviz.com/quote.ashx?t='
    dict = {}
    for ticker in listOfTickers:
        url = finviz_URL + ticker
        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)

        html = BeautifulSoup(response, features="lxml")  # ("lxml")

        news_table = html.find(id='news-table')
        dict[ticker] = news_table
    #    print(html)
    return dict


def createTensorForDataFrame(tickerRows_):
    '''
    Temp list 2:
        List of tickers
            - Ticker has lists of things to saw
                - Each list of things to sy has list containing date and text
    '''
    tempList2 = []
    for ticker in tickerRows_:
        intermediateTempList = []
        for row in ticker:
            # print(row.a.text)
            text = row.a.text
            timestamp = row.td.text
            temp = [timestamp, text]
            intermediateTempList.append(temp)
        tempList2.append((intermediateTempList))
    return tempList2


def fillTickerRows(news_tables_, tickers_):
    tickerData_ = []
    tickerRows_ = []
    for i in tickers_:
        tickerData_.append(news_tables_[i])
    for i in tickerData_:
        tickerRows_.append(i.findAll('tr'))
    return tickerRows_


def populateDataFrameList(TickerTensor_):
    listOfDataFrames_ = []
    for i in range((len(TickerTensor_))):
        listOfDataFrames_.append(pd.DataFrame(TickerTensor_[i], columns=['Date', 'Text']))
    return listOfDataFrames_


def StockSentimentAnalysis(tickers):
    news_tables = fillDictWTickers(tickers)
    tickerRows = fillTickerRows(news_tables, tickers)
    TickerTensor = createTensorForDataFrame(tickerRows)
    listOfDataFrames = populateDataFrameList(TickerTensor)
    for i in range(len(listOfDataFrames)):
        print(f"YAHOO: {tickers[i]}")
        getVaderReviewValues(listOfDataFrames[i])
