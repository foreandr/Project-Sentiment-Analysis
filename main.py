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

mySentiment = functions.SentimentAnalysisClass()
print(mySentiment.tickers)
print(mySentiment.wordlist)
#print(mySentiment.getUserPass(mySentiment.wordlist)) # sometimes wants self, sometimes doesnt..



tickers=['AMZN', 'MSFT', 'AMD']
#functions.StockSentimentAnalysis(tickers)

