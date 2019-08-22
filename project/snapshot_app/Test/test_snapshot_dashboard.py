# [1] Pytest library is used to write the unit and integration tests using @pytest.fixture and the in built python assert statement, URL: https://docs.pytest.org/en/latest/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] Plotly library - Graph Object to create interactive graphs, URL: https://plot.ly/python/reference/
# [4] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
# [5] Adapted from: https://plot.ly/python/bar-charts/
# [6] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [7] Source: Author:rslite, Date:Sep 17 '08 at 12:57: URL:https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions/82852#82852
# [8] Adapted from: https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/discovery_v1.py


import pytest  # [1]

from utility import Utility
import pandas as pd  # [2]
from sentiment import *
from natural_language import *
from natural_language_data import *
from average_price import *

from index_fixtures import *
from database import DatabaseModel
from gui_component import UIComponent
import plotly.graph_objs as go  # [3]


class TestClassifier(object):
    def test_fit(self):
        model = Classifier()
        print(model)
        assert str(model.classifier) == "<NaiveBayesClassifier trained on 38 instances>"

    def test_classify(self):
        data = Classifier().classify(text_classification_data)
        print(data)
        assert data["overall"] == "pos"


class TestAveragePrice(object):
    @pytest.fixture
    def model(self):
        return AveragePrice("unleaded", 1)

    def test_update_horizon(self, model):
        horizon = model.horizon
        print(horizon)
        assert horizon == 1

    def test_prepare_timeseries(self, model):
        df = model.prepare_timeseries()
        print(df)
        assert len(df) == 79

    def test_get_prediction(self, model):
        df = model.get_prediction()
        print(df)
        assert df["Prediction"].iloc[0] > 100  # [6]


class TestWebScraper(object):
    @pytest.fixture
    def web_scraper(self):
        return WebScraper("https://www.rac.co.uk/drive/advice/fuel-watch/")

    def test_init(self, web_scraper):
        url = web_scraper.url
        print(url)
        assert url == "https://www.rac.co.uk/drive/advice/fuel-watch/"

    def test_get_html(self, web_scraper):
        html = web_scraper.get_html(web_scraper.url)
        html = str(html)
        print(html)
        assert "</html>" in html

    def test_scrape_url(self, web_scraper):
        data = web_scraper.scrape_url(scrape_url_input)
        print(data)
        assert (
            data[0]["title"]
            == "March sees welcome relief at the pumps as fuel drops by 2.5p a litre"
        )

    def test_scrape_urls(self, web_scraper):
        data = web_scraper.scrape_urls()
        print(data)
        assert "The price of fuel fell" in data[0]["content"]

    def test_scrape_rac_outlook(self, web_scraper):
        data = web_scraper.scrape_rac_outlook()
        print(data)
        assert data["diesel"] is not None


class TestNaturalLanguage(object):
    @pytest.fixture
    def text(self):
        return NaturalLanguage(
            "https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases"
        )

    def test_process_predictions(self, text):
        df = pd.read_excel("Text_badget_input_test.xlsx")  # [4]
        data = text.process_predictions(df)
        print(data)
        assert (data["colour"], data["movement"]) == (
            "#008000",
            "Very likely to come down",
        )

    def test_process_classifications(self, text):
        data = text.process_classifications(transform_input)
        print(data)
        assert (data["classifications"], data["dates"]) == (
            [-1, -1],
            ["2019-06-23", "2019-06-25"],
        )

    def test_prepare_timeseries(self, text):
        df = text.prepare_timeseries([-1, -1], ["2019-06-23", "2019-06-25"])
        print(df)
        assert str(df.index[1]) == "2019-06-25 00:00:00"


class TestRACNewsletter(object):
    @pytest.fixture
    def news(self):
        return RACNewsletter("https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases")

    @pytest.fixture
    def data(self, news):
        web_scraper = WebScraper(news.query_input)
        return web_scraper.scrape_urls()

    def test_init(self, news):
        print(news.query_input)
        assert (
            news.query_input
            == "https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases"
        )

    def test_generate_prediction(self, news):
        result = news.generate_prediction()
        print(result)
        assert result["movement"] == "Very likely to come down"

    def test_classify(self, news, data):
        df = news.get_classification(data)
        print(df)
        assert df["Classification"].iloc[0] == 1.0  # [6]


class TestSentiment(object):
    @pytest.fixture
    def api(self):
        return TwitterConnection().connection

    #
    @pytest.fixture
    def sentiment(self):
        return Sentiment(["BP_Press", "Shell"])

    def test_init(self, sentiment):
        handles = sentiment.handles
        print(handles)
        assert handles == ["BP_Press", "Shell"]

    def test_get_user_timeline(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        print(timeline)
        assert len(timeline) == 5

    def test_generate_timeseries(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        df = sentiment.generate_timeseries(timeline)
        print(df)
        assert isinstance(df, pd.DataFrame) and len(df["sentiment"]) == 5

    def test_update_sentiment(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        df = sentiment.generate_timeseries(timeline)
        y_ax = sentiment.update_sentiment(df)
        print(y_ax)
        assert y_ax > 0

    def test_render_twitter_trace(self):
        render = UIComponent().render_twitter_trace("Shell", 0.1)
        print(render)
        assert render == go.Bar(x=["Shell"], y=[0.1], name="Shell")  # [5]

    def test_bar_chart(self):
        data = [
            go.Bar(x=["BP_Press"], y=[0.2660348], name="BP_Press"),
            go.Bar(x=["Shell"], y=[0.1312202], name="Shell"),
        ]  # [5]
        bar_chart = UIComponent.bar_chart(data)
        print(bar_chart)
        assert len(bar_chart["data"]) == 2

    def test_generate_sentiment(self, sentiment):
        text = "Customers can save 10p per litre on fuel when they spend £60 or more on groceries at a Sainsbury's supermarket"
        sentiment = sentiment.generate_sentiment(text)
        print(sentiment)
        assert abs(sentiment) > 0

    def test_process_sentiment(self, sentiment):
        result = sentiment.process_sentiment()
        print(result)
        assert len(result) == 2


class TestDiscoveryConnection(object):
    @pytest.fixture
    def api(self):
        return DiscoveryConnection()

    def test_connect(self, api):
        connection = str(api.connection).split(" ")[0]
        print(connection)
        assert connection == "<ibm_watson.discovery_v1.DiscoveryV1"

    def test_news_collection(self, api):
        print(api.news_collection)
        assert len(api.news_collection) == 5


class TestNewsArticle(object):
    @pytest.fixture
    def discovery(self):
        return NewsArticle("fuel price uk")

    def test_call_api(self, discovery):
        data = discovery.call_api()
        print(data)
        assert isinstance(data[0], dict)

    def test_get_classification(self, discovery):
        data = discovery.call_api()
        df = discovery.get_classification(data)
        print(df)
        assert isinstance(df["Classification"].iloc[0], (int, float))  # [6]

    def test_filter_key_words(self, discovery):
        data = discovery.filter_key_words("fuel price uk")
        print(data)
        assert data["relevant_words_bool"] == True

    def test_generate_wordcloud(self):  # [7]
        from pathlib import Path

        image = Path("assets/wordcloud.png")
        if image.is_file():
            result = True
        print(result)
        assert result == True

    def test_generate_prediction(self, discovery):
        result = discovery.generate_prediction()
        print(result)
        assert result["movement"] == "Very likely to go up"

    def test_generate_timeseries(self, discovery):
        df = discovery.generate_timeseries(transform_input)
        print(df)
        assert len(df.index) > 0

    def test_parse_api_data(self, discovery):  # [8]
        data = discovery.discovery.connection.query(
            "system",
            discovery.discovery.news_collection[-1]["collection_id"],
            natural_language_query=discovery.query_input,
            passages=True,
            count=50,
            highlight=True,
            deduplicate=True,
        ).get_result()
        results = discovery.parse_api_data(data)
        print(results)
        assert len(results) > 0

    def test_extract_body(self, discovery):
        data = discovery.extract_body(parse_data_input)
        print(data)
        assert (len(data["sentences"]) == 1) and (data["country"] == "GB")


class TestNLUConnection(object):
    def test_connect(self):
        print(NLUConnection())
        assert str(NLUConnection()).split(" ")[0] == "<sentiment.NLUConnection"


class TestTwitterConnection(object):
    def test_connect(self):
        connection = TwitterConnection().connection
        connection = str(connection).split(" ")[0]
        print(connection)
        assert connection == "<tweepy.api.API"


class TestSnapshotDashboardIntegration(object):
    def test_render_twitter_bar_chart(self):
        sentiment_engine = Sentiment(["BP_Press", "Shell"])
        sentiment_dataframe = sentiment_engine.process_sentiment()
        print(sentiment_dataframe)
        assert len(sentiment_dataframe) == 2

    def test_render_uk_averages(self):
        model = AveragePrice("diesel", 6)
        df = model.get_prediction()
        print(df)
        assert len(df) == 2

    def test_discovery_output(self):
        prediction = NewsArticle("fuel price uk").generate_prediction()
        print(prediction)
        assert prediction["movement"] == "Very likely to go up"

    def test_rac_output(self):
        newsletter = RACNewsletter(
            "https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases"
        )
        predictions = newsletter.generate_prediction()
        print(predictions)
        assert predictions["movement"] == "Very likely to come down"
