# [1] Requests library - RequestException class to catch exceptions when sending a HTTP request, URL: https://2.python-requests.org/en/master/_modules/requests/exceptions/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] NumPy library used for data processing, URL: https://www.numpy.org/
# [4] Tweepy library - to catch tweepy exceptions, URL: https://tweepy.readthedocs.io/en/latest/api.html#tweepy-error-exceptions
# [5] Tweepy library - API class to fetch timeline tweets from Twitter API, URL: https://tweepy.readthedocs.io/en/latest/api.html#tweepy-api-twitter-api-wrapper
# [6] Tweepy library - OAuthHandler class to authenticate Twitter API credentials, URL: http://docs.tweepy.org/en/v3.8.0/auth_tutorial.html
# [7] To catch IBM Watson generated exceptions, URL: https://github.com/IBM/python-sdk-core
# [8] IBM Natural Language Understanding API to calculate sentiment, URL: https://cloud.ibm.com/apidocs/natural-language-understanding?code=python
# [9] Source: https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/natural_language_understanding_v1.py
# [10] Source: https://github.com/vprusso/youtube_tutorials/blob/master/twitter_python/part_5_sentiment_analysis_tweet_data/sentiment_anaylsis_twitter_data.py
# [11] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mean.html
# [12] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe

import requests  # [1]
import pandas as pd  # [2]
import numpy as np  # [3]
import tweepy  # [4]
from tweepy import API  # [5]
from tweepy import OAuthHandler  # [6]
import ibm_cloud_sdk_core  # [7]
from ibm_watson import NaturalLanguageUnderstandingV1  # [8]
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    SentimentOptions,
)  # [8]
from ..infrastructure.database import DatabaseModel
from ..infrastructure.utility import Utility
from ..infrastructure.gui_component import UIComponent


class NLUConnection:
    def __init__(self):
        self.version = "2018-03-16"
        self.key = "keVXTae0f2m98zTXKzDD2Nh4rAUTtQ81ncjFRlu-R3Cn"
        self.url = (
            "https://gateway-lon.watsonplatform.net/natural-language-understanding/api"
        )
        self.connection = self.connect()

    def connect(self):  # [9]
        connection = NaturalLanguageUnderstandingV1(
            version=self.version, url=self.url, iam_apikey=self.key
        )
        return connection


class TwitterConnection:
    def __init__(self): # [10]
        self.key = "X9rPqN7KFmze7srVvE51FqaJf"
        self.secret = "E0SbuDIgETvJQicBqoQTn9GtVe3jyJKdJEcXFfCfCGw1mrmljl"
        self.token = "724869065894928385-uUY1B7BxAga8zUv3Ni3M3DLITTQI1Sf"
        self.token_secret = "Hfgm9x91y9GVdTSBaSLpulWCoKa1C5YM1YvAR8IdFLXQ0"
        self.connection = self.connect()

    def connect(self):  # [10]
        oauth_handler = OAuthHandler(self.key, self.secret)
        oauth_handler.set_access_token(self.token, self.token_secret)
        connection = API(oauth_handler)
        return connection


class Sentiment:
    def __init__(self, handles):
        self.handles = handles

    def generate_sentiment(self, tweet):
        try:
            analysis = (
                NLUConnection()
                .connection.analyze(
                    text=tweet, features=Features(sentiment=SentimentOptions())
                )
                .get_result()
            )  # [9]
            analysis = analysis["sentiment"]["document"]["score"]
        except (
            requests.exceptions.RequestException,  # [1]
            ibm_cloud_sdk_core.api_exception.ApiException,  # [7]
        ) as e:
            analysis = 0
        return analysis

    def get_user_timeline(self, handle, api):
        timeline = api.user_timeline(screen_name=handle, count=5) # [10]
        return timeline

    def generate_timeseries(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=["tweets"])  # [10]
        df["sentiment"] = np.array(
            [self.generate_sentiment(tweet) for tweet in df["tweets"]]
        )  # [10]
        df["mean"] = df["sentiment"].mean() #[11]
        return df

    def update_sentiment(self, df):
        y_ax = df["mean"].iloc[-1] #[12]
        if y_ax == 0.0:
            y_ax = 0.01
        return y_ax

    def process_sentiment(self):  # [10]
        api = TwitterConnection().connection
        traces = []
        for handle in self.handles:
            try:
                tweets = self.get_user_timeline(handle, api)
                df = self.generate_timeseries(tweets)
                y_ax = self.update_sentiment(df)

                trace = UIComponent().render_twitter_trace(handle, y_ax)
                traces.append(trace)
            except tweepy.TweepError as e:
                continue
        return traces
