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
# [17] Adapted from: https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/discovery_v1.py
# [18] Adapted from: Author:Paul H, Date: May 17 '18 at 18:38, URL:https://stackoverflow.com/questions/50397384/groupby-at-index-level-in-pandas
# [19] Adapted from: Author:Songhua Hu, Date:Jan 23 at 7:20, URL:https://stackoverflow.com/questions/22407798/how-to-reset-a-dataframes-indexes-for-all-groups-in-one-step
# [20] Adapted from: Author: Make42, Date:Nov 9 '17 at 13:57, URL:https://stackoverflow.com/questions/46728152/upsample-timeseries-in-pandas-with-interpolation
# [21] Adapted from: Author: mkln, Date: Dec 10 '13 at 10:19, URL: https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
# [22] Source: Author:Akshay, Date:Nov 28 '17 at 0:28, URL:https://stackoverflow.com/questions/47522009/make-directory-in-python
# [23] Adapted from: Author: Eli Courtwright, Date: Sep 18 '08 at 13:11, URL: https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
# [24] Wordcloud library used, URL: https://github.com/amueller/word_cloud


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
    def __init__(self):
        self.classifier = self.fit()
        # print(self.classifier,"TextClassificationEngine init")

    def fit(self):  # [5]
        cl = NaiveBayesClassifier(training_data_title[0:-10])
        return cl

    def classify(self, data):  # [5]
        # print(data,"prediction_engine input textclassifier")
        re = self.classifier.prob_classify(data)
        overall = re.max()
        pos = round(re.prob("pos"), 2)
        neg = round(re.prob("neg"), 2)
        # print(overall, pos, neg,"prediction_engine output textclassifier")
        return {"overall": overall, "pos": pos, "neg": neg}


class WebScraper:
    # tested
    def __init__(self, url):
        self.url = url
        # print(self.url,"WebScraper init")

    def get_html(self, url):  # [8]
        # print(url,"WebScraper get_html input")
        try:
            with closing(get(url, stream=True)) as response:
                result = BeautifulSoup(response.content, "html.parser")  # [4]
                # print(result,"WebScraper get_html output")
                return result
        except RequestException as e:
            # print(e)
            return None

    def scrape_url(self, links):  # [4] [8]
        # print(links,"scrape_url input")
        try:
            # data = Utility.open("rac")
            data = DatabaseModel().read("rac_data", "rac")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            # print(e)
            data = []
            for link in links:
                html = self.get_html(link)
                title = html.find_all("h1", class_="newsroom-headline fn")
                # print(title)
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
            # Utility.save("rac", data)
            DatabaseModel().save(data, "rac_data", "rac")
        # print(data,"scrape_url output")
        return data

    def scrape_urls(self):  # [4] [8]
        try:
            # links = Utility.open("rac-links")
            links = DatabaseModel().read("rac_data_sources", "rac")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            # print(e)
            html = self.get_html(self.url)
            # print(html,self.url,"html in scrape urls")
            result = html.find_all("a", class_="material")
            links = []
            for r in result:
                links.append(r["href"])
            start = "https://media.rac.co.uk"
            full_link = [start + link for link in links]
            links = rac_urls + full_link
            # Utility.save("rac-links", links)
            DatabaseModel().save(links, "rac_data_sources", "rac")
        result = self.scrape_url(links)
        # print(result,"scarpe_urls output vishal")
        return result

    def scrape_rac_outlook(self):  # [4] [8]
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
        # print(diesel, petrol, super_unleaded, lpg,"scrape_prediction output")
        return {
            "diesel": diesel,
            "petrol": petrol,
            "super_unleaded": super_unleaded,
            "lpg": lpg,
        }


class NaturalLanguage:
    def __init__(self, query_input):
        self.query_input = query_input

    # tested
    def process_predictions(self, forecast):
        forecast.to_excel("Text_badget_input_test.xlsx")
        # print(forecast,"Text badge_input")
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

        # print(colour,movement,"Text badget_input output")
        return {"colour": colour, "movement": movement}

    # tested
    def process_classifications(self, scores):
        # print(scores,"update_classifications input")
        classifications = []
        dates = []
        for score in scores:
            # print(score[0],"score")
            try:
                date = datetime.datetime.strptime(score[0], "%b %d, %Y").strftime(
                    "%Y-%m-%d"
                )  # [11]
                # print(date,"date")
            except ValueError:
                date = score[0].split("T")[0]
            dates.append(date)
            if score[2] == "pos":
                classification = 1
            else:
                classification = -1
            classifications.append(classification)
        # print(classifications,dates,"update_classifications output")
        return {"classifications": classifications, "dates": dates}

    # tested
    def prepare_timeseries(self, classifications, dates):
        # print(classifications,dates,"Text load input")
        dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]  # [11]
        oldest = min(dates)
        today = Utility.get_today_date()
        # print(dates)
        idx = pd.date_range(str(oldest), periods=len(classifications), freq="M")  # [12]
        cols = ["Classification"]  # [12]
        df = pd.DataFrame(classifications, dates, cols)  # [12]
        df.sort_index(inplace=True)  # [13]
        # print(df,"Text load output")
        return df


class RACNewsletter(NaturalLanguage):
    def __init__(self, query_input):
        # #print(query_input,"instance of news class vishal")
        super().__init__(query_input)

    # def transform(self,scores):
    #     #print(scores,"news transform input")
    #     classifications,dates = super().update_classifications(scores)
    #     df = super().load(classifications,dates)
    #     df = df.resample(rule='1MS').last().interpolate()
    #     #print(df,"news transform output")
    #     return df

    # tested
    def get_classification(self, data):
        # #print(data,"news classify input")
        scores = []
        # training_data_title = []
        # training_data_body = []
        for result in data[-10:]:
            classification = Classifier().classify(result["title"])
            # training_data_title.append(
            #     (
            #         "Classifier trained on title",
            #         result["title"],
            #         classification["overall"],
            #     )
            # )
            # training_data_body.append(
            #     (
            #         "Classifier trained on content",
            #         result["title"],
            #         classification_content["overall"],
            #     )
            # )
            # print(
            #     (
            #         "Classifier trained on title",
            #         result["title"],
            #         classification["overall"],
            #     )
            # )
            # print(
            #     (
            #         "Classifier trained on content",
            #         result["title"],
            #         classification_content["overall"],
            #     )
            # )
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
        # print(training_data_title)
        # print(training_data_body)
        classifications = super().process_classifications(scores)
        df = super().prepare_timeseries(
            classifications["classifications"], classifications["dates"]
        )
        df = df.resample(rule="1MS").last().interpolate()  # [14] [15] [16]
        # #print(df,"news classify ouput")
        return df

    # def predict(self,data):
    #     #print(data,"News predict input")
    #     diesel, petrol, super_unleaded, lpg = WebScraper('https://www.rac.co.uk/drive/advice/fuel-watch/').scrape_predictions()
    #     df = self.classify(data)
    #     model = NeuralNetworkEngine(5, df, 1, "Classification", "M")
    #     forecast = model.prediction_engine()
    #     colour,movement = super().badge_input(forecast)
    #     #print([movement, colour, petrol, diesel, super_unleaded, lpg],"News predict output")
    #     return [movement, colour, petrol, diesel, super_unleaded, lpg]

    # tested
    def generate_prediction(self):
        web_scraper = WebScraper(self.query_input)
        data = web_scraper.scrape_urls()
        # #print(data,"News predict input")
        outlook = WebScraper(
            "https://www.rac.co.uk/drive/advice/fuel-watch/"
        ).scrape_rac_outlook()
        df = self.get_classification(data)

        model = PredictionModel(df, 1, "Classification", "unleaded", "M", "N/A", "N/A")
        forecast = model.predict()

        # model = NeuralNetworkEngine(5, df, 1, "Classification", "M")
        # forecast = model.prediction_engine()
        prediction = super().process_predictions(forecast)
        # #print([movement, colour, petrol, diesel, super_unleaded, lpg],"News predict output")
        return {
            "movement": prediction["movement"],
            "colour": prediction["colour"],
            "petrol": outlook["petrol"],
            "diesel": outlook["diesel"],
            "super_unleaded": outlook["super_unleaded"],
            "lpg": outlook["lpg"],
        }
        # return result


class DiscoveryConnection:
    def __init__(self):  # [17]
        self.version = "2018-08-01"
        self.url = "https://gateway-lon.watsonplatform.net/discovery/api"
        self.key = "AlAAjM1RG99-dBY9I1XIU-V3w4p62cKyzllNjRX4W6pQ"
        self.connection = self.connect()
        self.news_collection = self.generate_news_collection()

    # tested
    def connect(self):  # [17]
        discovery = DiscoveryV1(version=self.version, url=self.url, iam_apikey=self.key)
        # #print(discovery,"connect discovery")
        return discovery

    def generate_news_collection(self):  # [17]
        environments = self.connection.list_environments().get_result()
        news_environment_id = "system"
        collections = self.connection.list_collections(news_environment_id).get_result()
        news_collections = [x for x in collections["collections"]]
        configurations = self.connection.list_configurations(
            environment_id=news_environment_id
        ).get_result()
        # #print(news_collections,"news_collection vishal")
        return news_collections


class NewsArticle(NaturalLanguage):
    def __init__(self, query_input):
        super().__init__(query_input)
        self.discovery = DiscoveryConnection()

    # tested

    def extract_body(self, data):
        # #print(data,"parse_data vishal")
        sentences = []
        for relation in data["enriched_text"]["relations"]:
            sentences.append(relation["sentence"])
        sentences = list(set(sentences))
        try:
            country = data["country"]
        except KeyError as e:
            # print(e)
            country = "N/A"
        # #print(sentences,country,"parse_data output")
        return {"sentences": sentences, "country": country}

    # tested
    def parse_api_data(self, data):
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
        # #print(results,"extract output")
        return results

    # tested

    def generate_timeseries(self, scores):
        # #print(scores,"transform input")
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
        # #print(df1,"transform output")
        return df1

    # tested
    def generate_wordcloud(self, wordcloud):
        Utility.save_file("wordcloud", wordcloud)
        try:
            os.makedirs("assets")  # [22]
        except FileExistsError as e:
            pass
        file = f"wordcloud-{Utility.get_today_date()}.json"
        print(file, "wordcloud file vishal")
        os.system(
            f"wordcloud_cli --text {file} --imagefile assets/wordcloud.png"
        )  # [23] [24]
        return None

    # tested
    def filter_key_words(self, text):
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
        # #print(df,"classify output vishal")
        return df

    def call_api(self):
        try:
            data = DatabaseModel().read("discovery_data", "discovery")
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [7]
            # #print(e,"discovery query exception")
            data = self.discovery.connection.query(
                "system",
                self.discovery.news_collection[-1]["collection_id"],
                natural_language_query=self.query_input,
                passages=True,
                count=50,
                highlight=True,
                deduplicate=True,
            ).get_result()  # [17]
            # Utility.save("discovery", data)
            data = self.parse_api_data(data)
            DatabaseModel().save(data, "discovery_data", "discovery")
        # #print(data,"call api discovery vishal")
        print(data, "result of discovery call api vishal")
        return data

    # tested
    def generate_prediction(self):
        data = self.call_api()
        data = list(data)
        df = self.get_classification(data)
        model = PredictionModel(df, 1, "Classification", "unleaded", "D", "N/A", "N/A")
        forecast = model.predict()
        prediction = super().process_predictions(forecast)
        oldest = str(df.index[0]).split(" ")[0]  # [9]
        latest = str(df.index[-1]).split(" ")[0]  # [9]
        # #print(movement, colour, oldest, latest,"query result")
        return {
            "movement": prediction["movement"],
            "colour": prediction["colour"],
            "oldest": oldest,
            "latest": latest,
        }
