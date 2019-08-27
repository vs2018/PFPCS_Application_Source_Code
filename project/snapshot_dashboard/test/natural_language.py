# [1] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [2] Requests library - RequestException class to catch exceptions when sending a HTTP request, URL: https://2.python-requests.org/en/master/_modules/requests/exceptions/
# [3] Requests library - get function to send HTTP request, URL: https://2.python-requests.org/en/master/
# [4] Beautiful Soup 4 library - BeautifulSoup to scrape HTML data from websites, URL: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# [5] TextBlob library - NaiveBayesClassifier class to classify text data, URL:https://textblob.readthedocs.io/en/dev/classifiers.html
# [6] IBM Watson Discovery API - DiscoveryV1 to extract news articles, URL: https://cloud.ibm.com/apidocs/discovery?code=python
# [7] PyMongo API - to catch PyMongo exceptions , URL: https://api.mongodb.com/python/current/api/pymongo/errors.html
# [8] Adapted from: https://realpython.com/python-web-scraping-practical-introduction/
# [9] Adapted from: Author: JoeCondron, Date: Jul 23 '15 at 17:17, URL: https://stackoverflow.com/questions/31593201/how-are-iloc-ix-and-loc-different
# [10] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [11] Adapted from: Author: community wiki, Date:May 25 '18 at 11:00, URL: https://stackoverflow.com/questions/311627/how-to-print-a-date-in-a-regular-format
# [12] Adapted from: Author:Andy Hayden, Date:Dec 9 '12 at 9:40, URL:https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it
# [13] Source: Author:Paul H, Date:Mar 5 '14 at 23:41, URL:https://stackoverflow.com/questions/22211737/how-to-sort-a-pandas-dataframe-by-index
# [14] Adapted from: Author: shadi, Date:Sep 30 '17 at 8:46, URL:https://stackoverflow.com/questions/17001389/pandas-resample-documentation
# [15] Adapted from: https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
# [16] Adapted from: Author: Matti John, Date:Jun 8 '13 at 16:20, URL:https://stackoverflow.com/questions/17001389/pandas-resample-documentation
# [17] Source: https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/discovery_v1.py
# [18] Adapted from: Author:Paul H, Date: May 17 '18 at 18:38, URL:https://stackoverflow.com/questions/50397384/groupby-at-index-level-in-pandas
# [19] Adapted from: Author:Songhua Hu, Date:Jan 23 at 7:20, URL:https://stackoverflow.com/questions/22407798/how-to-reset-a-dataframes-indexes-for-all-groups-in-one-step
# [20] Adapted from: Author: Make42, Date:Nov 9 '17 at 13:57, URL:https://stackoverflow.com/questions/46728152/upsample-timeseries-in-pandas-with-interpolation
# [21] Adapted from: Author: mkln, Date: Dec 10 '13 at 10:19, URL: https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
# [22] Source: Author:Akshay, Date:Nov 28 '17 at 0:28, URL:https://stackoverflow.com/questions/47522009/make-directory-in-python
# [23] Adapted from: Author: Eli Courtwright, Date: Sep 18 '08 at 13:11, URL: https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
# [24] Source: Wordcloud library used, URL: https://github.com/amueller/word_cloud
# [25] Source: https://towardsdatascience.com/random-forest-in-python-24d0893d51c0?gi=10839cfeb9a9
# [26] Source: Author: Andy Hayden, Date: Jun 21 '13 at 18:51, URL: https://stackoverflow.com/questions/17241004/how-do-i-convert-a-pandas-series-or-index-to-a-numpy-array

import datetime
import pandas as pd  # [1]
import os
from requests.exceptions import RequestException  # [2]
from contextlib import closing
from requests import get  # [3]
from bs4 import BeautifulSoup  # [4]
from textblob.classifiers import NaiveBayesClassifier  # [5]
from ibm_watson import DiscoveryV1  # [6]
import pymongo  # [7]

from database import DatabaseModel
from natural_language_data import (
    rac_urls,
    training_data,
    training_data_title,
    training_data_body,
)
from prediction_model import PredictionModel
from utility import Utility


class Classifier:
    """Class to classify natural language text"""
    def __init__(self):
        """Construct a classifier object"""
        self.classifier = self.fit()

    def fit(self):  # [5]
        """Instantiate a Naive Bayes Classifier using TextBlob"""
        cl = NaiveBayesClassifier(training_data_title[0:-10])
        return cl

    def classify(self, data):  # [5]
        """Classify text as positive or negative, including the probability the text is positive or negative"""
        re = self.classifier.prob_classify(data)
        overall = re.max()
        pos = round(re.prob("pos"), 2)
        neg = round(re.prob("neg"), 2)
        return {"overall": overall, "pos": pos, "neg": neg}


class WebScraper:
    """Class is responsible for scraping HTML data from web pages"""
    def __init__(self, url):
        """Construct a scraper object with the url of the web page to scrape"""
        self.url = url

    def get_html(self, url): # [8]
        """Instantiate BeautifulSoup to scrape html from a url"""
        try:
            with closing(get(url, stream=True)) as response:
                result = BeautifulSoup(response.content, "html.parser")  # [4]
                return result
        except RequestException as e:
            return None

    def scrape_url(self, links):  # [4] [8]
        """Extract specific html data from web scraped html"""
        try:
            data = DatabaseModel().read("rac_data", "rac")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            data = []
            for link in links:
                html = self.get_html(link)
                title = html.find_all("h1", class_="newsroom-headline fn")
                date = html.find_all("span", class_="material-date")
                content = html.find_all("div", class_="newsroom-article")
                content2 = content[0].find_all("div", class_="markdown clearfix")
                content3 = content2[0].find_all("p")
                sentences = []
                for p in content3:
                    page = p.getText()
                    sentences.append(page)
                sentences = " ".join(sentences)
                data.append(
                    {
                        "title": title[0].text.strip(),
                        "date": date[0].getText(),
                        "content": sentences,
                    }
                )
            DatabaseModel().save(data, "rac_data", "rac")
        return data

    def scrape_urls(self):  # [4] [8]
        """Get relevant RAC website newsletter urls to scrape html data"""
        try:
            links = DatabaseModel().read("rac_data_sources", "rac")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            html = self.get_html(self.url)
            result = html.find_all("a", class_="material")
            links = []
            for r in result:
                links.append(r["href"])
            start = "https://media.rac.co.uk"
            full_link = [start + link for link in links]
            links = rac_urls + full_link
            DatabaseModel().save(links, "rac_data_sources", "rac")
        result = self.scrape_url(links)
        return result

    def scrape_rac_outlook(self):  # [4] [8]
        """Scrape RAC predictions from RAC website"""
        html = self.get_html("https://www.rac.co.uk/drive/advice/fuel-watch/")
        diesel = (
            html.find_all("div", class_="fuel-type-container first odd")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        petrol = (
            html.find_all("div", class_="fuel-type-container even")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        super_unleaded = (
            html.find_all("div", class_="fuel-type-container odd")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        lpg = (
            html.find_all("div", class_="fuel-type-container last even")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        return {
            "diesel": diesel,
            "petrol": petrol,
            "super_unleaded": super_unleaded,
            "lpg": lpg,
        }


class NaturalLanguage:
    """Class to create a time series DataFrame for processed natural langauge text data"""
    def __init__(self, query_input):
        """Construct an object with text data to be processed"""
        self.query_input = query_input

    def process_predictions(self, forecast):
        """Generate the fuel price movement prediction output"""
        try:
            value = forecast.iloc[1][0]  # [9]
        except IndexError as e:
            value = forecast["Prediction"].iloc[0]  # [10]
        if value > 0:
            colour = "#008000"
            movement = "Very likely to come down"
        elif value < 0:
            colour = "#FF0000"
            movement = "Very likely to go up"
        else:
            colour = "#D3D3D3"
            movement = "No change forecast"

        return {"colour": colour, "movement": movement}

    # tested
    def process_classifications(self, scores):
        """Convert classified text data from positive/negative to a numerical score of 1/-1 to make a prediction"""
        classifications = []
        dates = []
        for score in scores:
            try:
                date = datetime.datetime.strptime(score[0], "%b %d, %Y").strftime(
                    "%Y-%m-%d"
                )  # [11]
            except ValueError:
                date = score[0].split("T")[0]
            dates.append(date)
            if score[2] == "pos":
                classification = 1
            else:
                classification = -1
            classifications.append(classification)
        return {"classifications": classifications, "dates": dates}

    def prepare_timeseries(self, classifications, dates):
        """Construct a time series DataFrame to make a prediction"""
        dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]  # [11] [25]
        oldest = min(dates)
        today = Utility.get_today_date()
        idx = pd.date_range(str(oldest), periods=len(classifications), freq="M")  # [12]
        cols = ["Classification"]  # [12]
        df = pd.DataFrame(classifications, dates, cols)  # [12]
        df.sort_index(inplace=True)  # [13]
        return df


class RACNewsletter(NaturalLanguage):
    """Inherits from NaturalLanguage to process html data in RAC Newsletters, and generate predictions"""
    def __init__(self, query_input):
        """Construct a RAC Newsletter object"""
        super().__init__(query_input)

    def get_classification(self, data):
        """Classify RAC Newsletters and generate a time series with classification scores"""
        scores = []

        for result in data[-10:]:
            classification = Classifier().classify(result["title"])

            if classification["pos"] != classification["neg"]:
                scores.append(
                    (
                        result["date"],
                        result["title"],
                        classification["overall"],
                        classification["pos"],
                        classification["neg"],
                    )
                )
        classifications = super().process_classifications(scores)
        df = super().prepare_timeseries(
            classifications["classifications"], classifications["dates"]
        )
        df = df.resample(rule="1MS").last().interpolate()  # [14] [15] [16]
        return df

    def generate_prediction(self):
        """Generate next months fuel price movement prediction based on RAC Newsletters"""
        web_scraper = WebScraper(self.query_input)
        data = web_scraper.scrape_urls()
        outlook = WebScraper(
            "https://www.rac.co.uk/drive/advice/fuel-watch/"
        ).scrape_rac_outlook()
        df = self.get_classification(data)

        model = PredictionModel(df, 1, "Classification", "unleaded", "M", "N/A", "N/A")
        forecast = model.predict()

        prediction = super().process_predictions(forecast)
        return {
            "movement": prediction["movement"],
            "colour": prediction["colour"],
            "petrol": outlook["petrol"],
            "diesel": outlook["diesel"],
            "super_unleaded": outlook["super_unleaded"],
            "lpg": outlook["lpg"],
        }


class DiscoveryConnection:
    """Class to connect to the IBM Watson Discovery APi"""
    def __init__(self):  # [17]
        """Constructor to create an object with a connection to the Discovery news collection dataset"""
        self.version = "2018-08-01"
        self.url = "https://gateway-lon.watsonplatform.net/discovery/api"
        self.key = "AlAAjM1RG99-dBY9I1XIU-V3w4p62cKyzllNjRX4W6pQ"
        self.connection = self.connect()
        self.news_collection = self.generate_news_collection()

    def connect(self):  # [17]
        """IBM Watson Discovery API connection instance"""
        discovery = DiscoveryV1(version=self.version, url=self.url, iam_apikey=self.key)
        return discovery

    def generate_news_collection(self):  # [17]
        """Connection to the news collection dataset"""
        environments = self.connection.list_environments().get_result()
        news_environment_id = "system"
        collections = self.connection.list_collections(news_environment_id).get_result()
        news_collections = [x for x in collections["collections"]]
        return news_collections


class NewsArticle(NaturalLanguage):
    """Inherits from the parent NaturalLanguage class to process online news articles and predict the next days fuel price movement prediction"""
    def __init__(self, query_input):
        """Constructs a news article object"""
        super().__init__(query_input)
        self.discovery = DiscoveryConnection()

    def extract_body(self, data):
        """Extracts the news article body"""
        sentences = []
        for relation in data["enriched_text"]["relations"]:
            sentences.append(relation["sentence"])
        sentences = list(set(sentences))
        try:
            country = data["country"]
        except KeyError as e:
            country = "N/A"
        return {"sentences": sentences, "country": country}

    def parse_api_data(self, data):
        """Constructs a news article dictionary with relevant details"""
        results = []
        for result in data["results"]:
            body = self.extract_body(result)
            if body["country"] == "GB":
                results.append(
                    {
                        "publication_date": result["publication_date"],
                        "country": body["country"],
                        "text": result["text"],
                        "title": result["title"],
                        "url": result["url"],
                        "relations": body["sentences"],
                    }
                )
        return results


    def generate_timeseries(self, scores):
        """Generates a time series DataFrame with classifications of news articles found in a API query"""
        classifications = super().process_classifications(scores)
        df = super().prepare_timeseries(
            classifications["classifications"], classifications["dates"]
        )
        df1 = (
            df.groupby(df.index)
            .apply(lambda df1: df1.resample("D").mean().interpolate())
            .reset_index(level=0, drop=True)
        )  # [18] [19] [20] [21]
        df1 = df1.resample(rule="1D").interpolate()  # [15] [16]
        return df1

    # tested
    def generate_wordcloud(self, wordcloud):
        """Generates a word cloud of the news articles fetched"""
        Utility.save_file("wordcloud", wordcloud)
        try:
            os.makedirs("assets")  # [22]
        except FileExistsError as e:
            pass
        file = f"wordcloud-{Utility.get_today_date()}.json"
        os.system(
            f"wordcloud_cli --text {file} --imagefile assets/wordcloud.png"
        )  # [23] [24]
        return None

    # tested
    def filter_key_words(self, text):
        """Filters the relevant news articles that are on the topic of UK fuel prices"""
        relevant_words = ["uk", "price", "fuel"]
        relevant_words_caps = ["UK", "Price", "Fuel"]
        relevant_words_bool = all(word in text for word in relevant_words)
        relevant_words_caps_bool = all(word in text for word in relevant_words_caps)
        return {
            "relevant_words_bool": relevant_words_bool,
            "relevant_words_caps_bool": relevant_words_caps_bool,
        }

    # tested
    def get_classification(self, data):
        """Generate a positive or negative classification for each news article"""
        wordcloud = []
        scores = []
        date = Utility.get_today_date()
        for result in data:
            title, text, date = (
                [result["title"]],
                [result["text"]],
                result["publication_date"],
            )
            relations = list(set(result["relations"]))
            joined_text = ". ".join(title + text + relations)
            classification = Classifier().classify(joined_text)
            filtered_text = self.filter_key_words(joined_text)
            if (
                filtered_text["relevant_words_bool"]
                or filtered_text["relevant_words_caps_bool"]
            ):
                scores.append(
                    (
                        date,
                        text[0],
                        classification["overall"],
                        classification["pos"],
                        classification["neg"],
                    )
                )
                wordcloud.append(joined_text)
        df = self.generate_timeseries(scores)
        self.generate_wordcloud(wordcloud)
        return df

    def call_api(self):
        """Call the IBM Watson Discovery API to fetch news articles with the query: fuel price uk"""
        try:
            data = DatabaseModel().read("discovery_data", "discovery")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            data = self.discovery.connection.query(
                "system",
                self.discovery.news_collection[-1]["collection_id"],
                natural_language_query=self.query_input,
                passages=True,
                count=50,
                highlight=True,
                deduplicate=True,
            ).get_result()  # [17]
            data = self.parse_api_data(data)
            DatabaseModel().save(data, "discovery_data", "discovery")
        return data

    # tested
    def generate_prediction(self):
        """Generate the next days fuel price movement predictions using news articles on fuel prices in the uk"""
        data = self.call_api()
        data = list(data)
        df = self.get_classification(data)
        model = PredictionModel(df, 1, "Classification", "unleaded", "D", "N/A", "N/A")
        forecast = model.predict()
        prediction = super().process_predictions(forecast)
        oldest = str(df.index[0]).split(" ")[0] #[26]
        latest = str(df.index[-1]).split(" ")[0] #[26]
        return {
            "movement": prediction["movement"],
            "colour": prediction["colour"],
            "oldest": oldest,
            "latest": latest,
        }
