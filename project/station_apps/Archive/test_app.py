import pytest
from master_class_file import *
from app1_fixtures import *
from index_fixtures import *


class TestSarimaEngine(object):
    @pytest.fixture
    def sarima(self):
        df = AggregatePriceModel("unleaded", 1).extract()
        return SarimaEngine("unleaded", 1, df)

    def test_init(self, sarima):
        assert sarima.fuel_type == "unleaded"

    def test_extract(self, sarima):
        df1, df, p, d, q = sarima.extract()
        assert (p == 1) and (d == 1) and (q == 3)

    def test_fit(self, sarima):
        df1, df, p, d, q = sarima.extract()
        results, exog_forecast = sarima.fit(df1, df, p, d, q)
        assert (
            str(results).split(" ")[0]
            == "<statsmodels.tsa.statespace.sarimax.SARIMAXResultsWrapper"
        )

    def test_transform(self, sarima):
        fcast = sarima.transform()
        assert len(fcast) == 1

    def test_prediction_engine(self, sarima):
        df = sarima.prediction_engine()
        assert isinstance(df["Prediction"].iloc[0], (int, float))


class TestTextClassificationEngine(object):
    def test_fit(self):
        model = TextClassificationEngine()
        assert str(model.classifier) == "<NaiveBayesClassifier trained on 28 instances>"

    def test_prediction_engine(self):
        overall, pos, neg = TextClassificationEngine().prediction_engine(
            text_classification_data
        )
        assert overall == "neg"


class TestNeuralNetworkEngine(object):
    @pytest.fixture
    def engine(self):
        df = AggregatePriceModel(
            "regional-diesel.xlsx", 1, "Northern Ireland"
        ).extract()
        return NeuralNetworkEngine(5, df, 1, "Scotland", "M")

    def test_init(self, engine):
        epoch = engine.epoch
        horizon = engine.horizon
        feature = engine.feature
        frequency = engine.frequency
        assert (
            (epoch == 5)
            and (horizon == 1)
            and (feature == "Scotland")
            and (frequency == "M")
        )

    def test_transform(self, engine):
        scaler, test, scaled_train, scaled_test = engine.scale()
        assert isinstance(scaled_train, np.ndarray) and isinstance(
            scaled_test, np.ndarray
        )

    def test_fit(self, engine):
        scaler, test, scaled_train, scaled_test = engine.scale()
        model = engine.fit(scaled_train, scaled_test, 1, 1)
        model = str(model).split(" ")[0]
        assert model == "<keras.engine.sequential.Sequential"

    def test_transform(self, engine):
        scaler, test_predictions = engine.transform()
        assert len(test_predictions) == 2

    def test_prediction_engine(self, engine):
        df = engine.prediction_engine()
        assert "2019" == str(df.index[0]).split("-")[0]


class TestAggregatePriceModel(object):
    @pytest.fixture
    def model(self):
        return AggregatePriceModel("regional-diesel.xlsx", 1, "Northern Ireland")

    def test_update_horizon(self, model):
        horizon = model.horizon
        assert horizon == 1

    def test_extract(self, model):
        df = model.extract()
        assert df["Northern Ireland"].iloc[0] == 101.6

    def test_predict(self, model):
        df = model.predict()
        assert df["Prediction"].iloc[0] > 100


class TestWebScraper(object):
    @pytest.fixture
    def web_scraper(self):
        return WebScraper("https://www.rac.co.uk/drive/advice/fuel-watch/")

    def test_init(self, web_scraper):
        url = web_scraper.url
        assert url == "https://www.rac.co.uk/drive/advice/fuel-watch/"

    def test_get_html(self, web_scraper):
        html = web_scraper.get_html(web_scraper.url)
        html = str(html)
        assert "</html>" in html

    def test_scrape_url(self, web_scraper):
        data = web_scraper.scrape_url(scrape_url_input)
        assert (
            data[0]["title"]
            == "March sees welcome relief at the pumps as fuel drops by 2.5p a litre"
        )

    def test_scrape_urls(self, web_scraper):
        data = web_scraper.scrape_urls()
        print(len(data))
        assert "The price of fuel fell" in data[0]["content"]

    def test_scrape_predictions(self, web_scraper):
        diesel, petrol, super_unleaded, lpg = web_scraper.scrape_predictions()
        assert diesel is not None


class TestText(object):
    @pytest.fixture
    def text(self):
        return Text("https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases")

    def test_badge_input(self, text):
        df = pd.read_excel("Text_badget_input_test.xlsx")
        colour, movement = text.badge_input(df)
        assert (colour, movement) == ("#FF0000", "up")

    def test_update_classifications(self, text):
        classifications, dates = text.update_classifications(transform_input)
        assert (classifications, dates) == ([-1, -1], ["2019-06-23", "2019-06-25"])

    def test_load(self, text):
        df = text.load([-1, -1], ["2019-06-23", "2019-06-25"])
        assert str(df.index[1]) == "2019-06-25 00:00:00"


class TestNews(object):
    @pytest.fixture
    def news(self):
        return News("https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases")

    @pytest.fixture
    def data(self, news):
        web_scraper = WebScraper(news.query_input)
        return web_scraper.scrape_urls()

    def test_init(self, news):
        assert (
            news.query_input
            == "https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases"
        )

    def test_query(self, news):
        output = [
            "down",
            "#008000",
            "No change forecast",
            "Likely to come down",
            "No change forecast",
            "No change forecast",
        ]
        result = news.query()
        assert result == output

    def test_classify(self, news, data):
        df = news.classify(data)
        assert df["Classification"].iloc[0] == 1.0


class TestNaturalLanguage(object):
    def test_connect(self):
        assert (
            str(NaturalLanguage()).split(" ")[0] == "<master_class_file.NaturalLanguage"
        )


class TestDiscoveryConnection(object):
    @pytest.fixture
    def api(self):
        return DiscoveryConnection()

    def test_connect(self, api):
        connection = str(api.connection).split(" ")[0]
        assert connection == "<ibm_watson.discovery_v1.DiscoveryV1"

    def test_news_collection(self, api):
        assert len(api.news_collection) == 5


class TestDiscovery(object):
    @pytest.fixture
    def discovery(self):
        return Discovery("fuel price uk")

    def test_call_api(self, discovery):
        data = discovery.call_api()
        assert len(data["results"]) > 0

    def test_classify(self, discovery):
        data = discovery.call_api()
        df = discovery.classify(data)
        assert isinstance(df["Classification"].iloc[0], (int, float))

    def test_filter_text(self, discovery):
        bool_nocaps, bool_caps = discovery.filter_text("fuel price uk")
        assert bool_nocaps == True

    def test_save_wordcloud(self):
        from pathlib import Path

        image = Path("assets/wordcloud.png")
        if image.is_file():
            result = True
        assert result == True

    def test_query(self, discovery):
        result = discovery.query()
        assert result == ("up", "#FF0000", "2019-06-23", "2019-07-20")

    def test_transform(self, discovery):
        df = discovery.transform(transform_input)
        assert len(df.index) > 0

    def test_extract(self, discovery):
        data = discovery.call_api()
        dict = discovery.extract(data)
        assert dict[0]["country"] == "GB"

    def test_parse_data(self, discovery):
        sentences, country = discovery.parse_data(parse_data_input)
        assert len(sentences) == 1 and country == "GB"


class TestTwitterConnection(object):
    def test_connect(self):
        connection = TwitterConnection().connection
        connection = str(connection).split(" ")[0]
        assert connection == "<tweepy.api.API"


#
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
        assert handles == ["BP_Press", "Shell"]

    def test_get_user_timeline(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        assert len(timeline) == 5

    def test_tweet_dataframe_constructor(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        df = sentiment.tweet_dataframe_constructor(timeline)
        assert isinstance(df, pd.DataFrame) and len(df["sentiment"]) == 5

    def test_get_sentiment(self, api, sentiment):
        timeline = sentiment.get_user_timeline("Shell", api)
        df = sentiment.tweet_dataframe_constructor(timeline)
        y_ax = sentiment.get_sentiment(df)
        assert y_ax > 0

    def test_render_twitter_trace(self):
        render = UIComponent().render_twitter_trace("Shell", 0.1)
        assert render == go.Bar(x=["Shell"], y=[0.1], name="Shell")

    def test_bar_chart(self):
        data = [
            go.Bar(x=["BP_Press"], y=[0.2660348], name="BP_Press"),
            go.Bar(x=["Shell"], y=[0.1312202], name="Shell"),
        ]
        bar_chart = UIComponent.bar_chart(data)
        assert len(bar_chart["data"]) == 2

    def test_calculate_sentiment(self, sentiment):
        text = "Customers can save 10p per litre on fuel when they spend £60 or more on groceries at a Sainsbury's supermarket"
        sentiment = sentiment.calculate_sentiment(text)
        assert sentiment > 0

    def test_process_twitter_sentiments(self, sentiment):
        result = sentiment.process_twitter_sentiments()
        assert len(result) == 2


DatabaseModel().drop("DirectionsAPI")
DatabaseModel().drop("DirectionsOffRoute")
DatabaseModel().drop("stations")


class TestProcessor(object):
    #     #tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def processor(self):
        return Processor(
            "SHELL", "FROME", "SOMERSET", "BA11 2RY", "Unleaded", 126.9, "BA11 5LA"
        )

    def test_generate_outcode(self, processor):
        outcode = processor.generate_outcode(processor.post_code)
        assert outcode == "BA"

    def test_generate_matching_post_codes(self, processor):
        matches = processor.generate_matching_post_codes(
            "BA", generate_matching_post_codes_input
        )
        assert matches == ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]

    def test_generate_brand_filtered_df(self, processor):
        df = processor.generate_brand_filtered_df(False)
        assert len(df) == 27910

    def test_determine_brand_type(self, processor):
        result = processor.determine_brand_type()
        assert result == False

    def test_nearest_postcode(self, processor):
        df = processor.generate_brand_filtered_df(False)
        post_codes = processor.nearest_postcode(df)
        assert post_codes == ["BA2 7HY", "BA2 5RU", "BA1 6AJ", "BA2 3BA"]

    def test_get_relevant_postcodes(self, processor):
        df = processor.generate_brand_filtered_df(False)
        post_codes = processor.get_relevant_post_codes(df)
        assert len(post_codes) == 4

    def test_generate_latlon_obj(self, processor):
        obj = processor.generate_latlon_obj(
            ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]
        )
        assert obj[0]["latitude"] == 51.3778523492681

    def test_call_distance_api(self, processor):
        pc = ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]
        obj = processor.generate_latlon_obj(pc)
        sorted_pc = processor.call_distance_api(
            51.2429256459164, -2.29176511193396, obj, pc
        )
        assert sorted_pc[0] == "BA2 7HY"

    def test_transformer(self, processor):
        df = processor.transformer()
        assert df["DistanceFromSearchPostcode"].iloc[0] == 2.23

    def test_predictor(self, processor):
        df = processor.transformer()
        prediction = processor.predictor(df)
        assert isinstance(prediction["Prediction"].iloc[0], float)

    def test_loader(self, processor):
        prediction, confidence, model, result, df1 = processor.loader()
        assert (
            (prediction < 200)
            and (confidence >= 0)
            and (isinstance(model, str))
            and (len(result) == 1)
            and (len(df1) > 1)
        )

    def test_save(self, processor):
        result = processor.save()
        assert len(result["df"] == 21)


class TestArimaModel(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def model(self):
        df = pd.read_excel("Testing_ArimaModel_init.xlsx", index_col=0)
        print(df, "printing fixture df")
        return ArimaModel(df, "Price", 1, "Unleaded", "ASDA", "BA11 5LA")

    @pytest.fixture
    def data(self):
        df = pd.read_excel("Testing_ArimaModel_init.xlsx", index_col=0)
        model = ArimaModel(df, "Price", 1, "Unleaded", "ASDA", "BA11 5LA")
        return model.split_datasets()

    def test_simple_predictions(self, model, data):
        error = model.simple_predictions(data[0], data[1], "Price")
        assert error == 0.0625

    def test_arima_predictions(self, model, data):
        error = model.arima_predictions(data[0], data[1], "Price", 0, 1, 1)
        assert error == 0.05524121362984147

    def test_arima_predict(self, model, data):
        arima = ARIMA(data[0]["Price"], order=(0, 1, 1)).fit()
        error = model.arima_predict(arima, data[0], data[1], "Price")
        assert error == 0.05524121362984147

    def test_smoothed_predictions(self, model, data):
        error = model.smoothed_predictions(data[0], data[1], "Price")
        assert error == 0.400097958633836

    def test_non_arima_predict(self, model, data):
        exp = ExponentialSmoothing(data[0]["Price"]).fit()
        error = model.non_arima_predict(exp, data[0], data[1], "Price")
        assert error == 0.0625

    def test_additive_predictions(self, model, data):
        error = model.additive_predictions(data[0], data[1], "Price")
        assert error == 0.0625

    def test_multiplicative_predictions(self, model, data):
        error = model.multiplicative_predictions(data[0], data[1], "Price")
        assert str(error) == "nan"

    def test_split_datasets(self, model):
        train, test = model.split_datasets()
        assert len(train) > 1 and len(test) == 1

    def test_prediction(self, model):
        df = model.prediction()
        assert df["Model"].iloc[0] == "Simple"

    def test_set_errors(self, model):
        model.set_errors(1, 0, 1)
        assert isinstance(model.error, float)
        # assert isinstance(model.error,float) == 0.0625

    def test_fit(self, model):
        model.set_errors(1, 0, 1)
        results, model_selected, error = model.fit(0.0625, 1, 0, 1)
        assert (
            (str(results).split(".")[0] == "<statsmodels")
            and isinstance(model_selected, str)
            and isinstance(error, float)
        )

    def test_forecast_price(self, model):
        model.set_errors(1, 0, 1)
        results, model_selected, error = model.fit(0.0625, 1, 0, 1)
        result = model.forecast_price(model_selected, results, 1, 0, 1)
        assert len(result) == 1


class TestGoogleMapsPlaces(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def map(self):
        df = MapboxDirections("BA11 5AP", "BA11 5LB").save()
        return GoogleMapsPlaces("BA11 5AP", "BA11 5LB", df)

    def test_reset_places(self, map):
        map.reset_places()
        assert map.places == {
            "Start-Address": [],
            "End-Address": [],
            "Distance-Text": [],
            "Distance-Value": [],
            "Duration-Text": [],
            "Duration-Value": [],
            "Origin": [],
            "Destination": [],
            "Route-Lat": [],
            "Route-Lng": [],
            "Station": [],
            "Station-Lat": [],
            "Station-Lng": [],
            "Station-PostCode": [],
            "Open": [],
            "Rating": [],
            "Total-Ratings": [],
            "Amenities": [],
        }

    def test_update_station_location(self, map):
        map.update_station_location(station)
        assert map.places["Station-PostCode"] == ["BA11 5LA"]

    def test_update_station_details(self, map):
        map.update_station_details(station)
        assert "gas_station" in map.places["Amenities"][0]

    def test_call_api(self, map):
        response = map.call_api(51.22032, -2.31717)
        assert response["status"] == "OK"

    def test_configure_api_data(self, map):
        map.configure_api_data()
        assert 5614.4 in map.places["Distance-Value"]

    def test_save(self, map):
        df = map.save()
        assert len(df) == 72


class TestMapboxDirections(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def map(self):
        return MapboxDirections("BA11 5AP", "BA11 5LB")

    @pytest.fixture
    def data(self):
        mapbox = MapboxDirections("BA11 5AP", "BA11 5LB")
        return mapbox.configure_api_data()

    def test_reset_directions(self, map):
        map.reset_directions()
        assert map.routes == {
            "Origin": [],
            "Destination": [],
            "Start-Address": [],
            "End-Address": [],
            "Distance-Text": [],
            "Distance-Value": [],
            "Duration-Text": [],
            "Duration-Value": [],
            "Lat": [],
            "Lng": [],
        }

    def test_generate_latlon(self, map):
        response = MapboxDirections.generate_latlon("BA11 5LA")
        assert response == [-2.30448401366007, 51.2273911883167]

    def test_get_address(self, map):
        address = map.get_address()
        assert (
            address[0]["place_name"]
            == "BA11 5AP, Frome, Somerset, England, United Kingdom"
        )

    def test_generate_post_code(self, map):
        response = map.generate_post_code(-2.3335548, 51.2167441)
        assert response[0]["context"][0]["text"] == "BA11 4QE"

    def test_update_directions_details(self, map, data):
        map.update_directions_details([[-2.31109], [51.22234]], data)
        assert map.routes["Start-Address"] == [
            "55 Tower View, Frome, Frome, BA11 5AP, United Kingdom"
        ]

    def test_configure_api_data(self, map):
        # api_data = map.configure_api_data(driving_routes,[-2.31705241493394, 51.2203620750975],[-2.31109549671642, 51.2224372245192])
        # assert api_data[3] == '81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom'
        api_data = map.configure_api_data()
        assert (
            api_data[3] == "81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom"
        )

    def test_call_api(self, map):
        routes, origin, destination = map.call_api()
        assert (
            (routes["features"][0]["properties"]["duration"] >= 100)
            and (origin == [-2.31705241493394, 51.2203620750975])
            and (destination == [-2.31109549671642, 51.2224372245192])
        )

    def test_save(self, map):
        df = map.save()
        assert df["Duration-Value"].iloc[0] >= 100


class TestGoogleMapsConnection(object):
    def test_places(self):
        maps = GoogleMapsConnection()
        assert str(maps.places).split(" ")[0] == "<googlemaps.client.Client"


class TestMapboxConnection(object):
    def test_geocoder(self):
        mapbox = MapboxConnection()
        assert (
            str(mapbox.geocoder).split(" ")[0] == "<mapbox.services.geocoding.Geocoder"
        )

    def test_directions(self):
        mapbox = MapboxConnection()
        assert (
            str(mapbox.directions).split(" ")[0]
            == "<mapbox.services.directions.Directions"
        )


class TestStation(object):
    @pytest.fixture
    def station(self):
        return Station("BA11 5LB", "Unleaded", "BA11 5AP")

    @pytest.fixture
    def nearest_station(self):
        return Station("BA11 5LA", "Unleaded")

    def test_address(self, station):
        result = station.address("BA11 5LB")
        assert result == [
            {
                "label": "BA11 5LB, Frome, Somerset, England, United Kingdom",
                "value": "BA11 5LB",
            }
        ]

    def test_call_api(self, nearest_station):
        result = nearest_station.call_api()
        output = FileHelper.open("BA11 5LA")
        assert result == output

    def test_get_stations(self, nearest_station):
        result = nearest_station.get_stations()
        assert result["Price"].iloc[0] >= 124.7

    def test_get_directions(self, station):
        df = station.get_directions()
        assert isinstance(df["Duration-Value"].iloc[0], float)

    def test_get_places(self, station):
        df = station.get_directions()
        df = station.get_places(df)
        assert "gas_station" in df["Amenities"].iloc[0]

    def test_get_journey_data(self, station):
        df = station.get_journey_data()
        assert df["DistanceFromSearchPostcode"].iloc[0] == 0.07

    def test_get_unique_stations(self, station):
        df = station.get_directions()
        df = station.get_places(df)
        stations = Station.get_unique_stations(df)
        assert stations == ["BA11 5LA"]

    def test_get_data(self, station):
        df = station.get_journey_data()
        df1, df = station.get_data(df)
        assert (df1["DateR"].iloc[0] == "19/07/2019") and (df["Brand"].iloc[-1] == "BP")

    def test_predict(self, nearest_station):
        data = FileHelper.open("BA11 5LA")
        nearest_station.predict(data, "2019-07-19")
        assert "2019-07-19" in nearest_station.data["Date"]

    def test_reset_data(self, nearest_station):
        data = FileHelper.open("BA11 5LA")
        nearest_station.predict(data, "2019-07-19")
        nearest_station.reset_data()
        obj = {
            "Date": [],
            "SearchPostCode": [],
            "DistanceFromSearchPostcode": [],
            "Brand": [],
            "Name": [],
            "Street": [],
            "Town": [],
            "County": [],
            "PostCode": [],
            "FuelType": [],
            "Price": [],
            "1-Day Price Prediction": [],
            "1-Day Prediction Confidence": [],
            "1-Day Prediction Model": [],
            "TimeRecorded": [],
            "Lat": [],
            "Lon": [],
        }
        assert nearest_station.data == obj

    def test_get_station_data(self, nearest_station):
        df = nearest_station.get_station_data("BA11 5LA")
        assert df["PostCode"].iloc[0] == "BA11 5LA"

    def test_get_route_data(self, station):
        df = station.get_route_data("BA11 5AP")
        assert df["Origin"].iloc[0] == "BA11 5LB"


class TestJourney(object):
    @pytest.fixture
    def journey(self):
        return Journey("BA11 5LB", "Unleaded", "BA11 5AP")

    def test_reset_route_data(self, journey):
        journey.reset_route_data()
        output = {
            "origin": [],
            "destination": [],
            "lat_origin": [],
            "lat_destination": [],
            "lon_origin": [],
            "lon_destination": [],
            "route_information": [],
        }
        assert journey.route_data == output

    def test_save_route(self, journey):
        journey.save_route(
            [
                (-2.30425, 51.22757),
                (-2.30395, 51.22741),
                (-2.30377, 51.22726),
                (-2.30348, 51.22714),
            ],
            "Distance: 0 km, Duration: 0 mins",
            0,
        )
        output = {
            "origin": ["BA11 5LB"],
            "destination": ["BA11 5AP"],
            "lat_origin": [51.22757],
            "lat_destination": [51.22741],
            "lon_origin": [-2.30425],
            "lon_destination": [-2.30395],
            "route_information": ["Distance: 0 km, Duration: 0 mins"],
        }
        assert journey.route_data == output

    def test_save(self, journey):
        df = journey.save(["BA11 5LA"])
        assert df["Brand"].iloc[-1] == "BP"

    def test_remove_invalid_post_code(self, journey):
        post_codes = journey.remove_invalid_post_code(["BA11 5LA"])
        assert post_codes == ["BA11 5LA"]

    def test_call_api(self, journey):
        batch_data = journey.call_api(["BA11 5LA"])
        assert (
            batch_data[0]["Response"]["DataItems"]["FuelStationDetails"][
                "FuelStationCount"
            ]
            == 7
        )

    def test_save_station_routes(self, journey):
        df = pd.read_excel("Test_Journey_map_routes_df.xlsx")
        df_route = pd.read_excel("Test_Journey_map_routes_df_route.xlsx")
        off_routes = journey.save_station_routes(df, df_route)
        assert len(off_routes) > 0

    def test_get_station_routes(self, journey):
        df = pd.read_excel("Test_Journey_map_routes_df.xlsx")
        off_routes = journey.get_station_routes(df)
        assert len(off_routes) > 0

    def test_get_offroute_data(self, journey):
        df = pd.read_excel("Test_Journey_get_offroute_data_df.xlsx")
        df_route = pd.read_excel("Test_Journey_get_offroute_data_df_route.xlsx")
        distances, route_responses = journey.get_offroute_data(df, df_route, 1)
        assert (len(distances) > 1) and (len(route_responses) > 1)

    def test_map_routes(self, journey):
        df = pd.read_excel("Test_Journey_map_routes_df.xlsx")
        df_route = pd.read_excel("Test_Journey_map_routes_df_route.xlsx")
        off_routes, routes = journey.map_routes(df_route, df)
        assert (len(off_routes) > 0) and (len(routes) > 0)

    def test_map(self, journey):  # couldnt find DirectionsAPI table
        df = pd.read_excel("Test_Journey_map_df.xlsx")
        stations_list, origin_coordinate, destination_coordinate, routes, off_routes, stations = journey.map(
            df
        )
        assert (
            (
                stations_list["Start-Address"].iloc[0]
                == "81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom"
            )
            and (len(origin_coordinate) == 1)
            and (len(destination_coordinate) == 1)
            and (len(routes) > 10)
            and (len(off_routes) > 10)
            and (len(stations) == 1)
        )


class TestVehicle(object):
    # tested on BA11 5LB / BA11 5AP on 21 July 2019 price data
    @pytest.fixture
    def car(self):
        return Vehicle("AV04YGE")

    def test_get_spec(self, car):
        model, fuel, tank, highway, city, combined = car.get_spec()
        assert (
            (model == "PEUGEOT 206 GTI 180")
            and (fuel == "PETROL")
            and (tank == 50.0)
            and (highway == 42.1)
            and (city == 23.9)
            and (combined == 32.8)
        )

    def test_save(self, car):
        result = car.save()
        output = FileHelper.open_no_date(f"vehicle-{car.registration}")
        assert result == output

    def test_get_tank_capacity(self, car):
        tank = car.get_tank_capacity()
        assert tank == 50.0

    def test_get_fuel_type(self, car):
        fuel = car.get_fuel_type()
        assert fuel == "PETROL"

    def test_mpg(self, car):
        result = car.mpg(50)
        assert result == (50 / 4.54609)

    def test_analysis_dataframes(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        df, df_station, df_directions, station = car.analysis_dataframes(
            hover, "BA11 5LB", "BA11 5AP", "Unleaded"
        )
        assert (
            (station == "BA11 4NZ")
            and (df_directions["Duration-Value"].iloc[0] >= 0)
            and (df_station["Brand"].iloc[0] == "ESSO")
            and (df["DistanceFromSearchPostcode"].iloc[0] == 0.07)
        )

    def test_analysis(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        distance, selected_s, difference, losses, comparison, saving = car.analysis(
            hover, "BA11 5LB", "BA11 5AP", "10", "Unleaded"
        )
        assert (
            (isinstance(distance, str))
            and (
                selected_s
                == "£52.36 to fill up Unleaded fuel at ESSO located at BA11 4NZ"
            )
            and (
                difference
                == "5.2 p more expensive than the minimum price which is 125.7 of Unleaded in your search which is ASDA located at BA11 5LA"
            )
            and (
                comparison
                == "On a daily commute (5 days a week), you could save up to £7.84 per year if you fill at ASDA located at BA11 5LA rather than this station"
            )
            and (
                saving
                == "If you make this journey tomorrow, you will lose £0.0 to fill up your tank compared to filling it up today at this station"
            )
            and (losses == "Loss of £2.08")
        )

    def test_saving_analysis(self, car):
        saving, cost = car.saving_analysis(
            130.9, 130.9, 40.0, "ESSO", "BA11 4NZ", "Unleaded"
        )
        assert (
            saving
            == "If you make this journey tomorrow, you will lose £0.0 to fill up your tank compared to filling it up today at this station"
        ) and (cost == "£52.36 to fill up Unleaded fuel at ESSO located at BA11 4NZ")

    def test_comparison_analysis(self, car):
        difference, losses, comparison = car.comparison_analysis(
            6.2, 124.7, "Unleaded", "ASDA", "BA11 5LA", 2.48, 9.35, "ESSO"
        )
        assert (
            (
                difference
                == "6.2 p more expensive than the minimum price which is 124.7 of Unleaded in your search which is ASDA located at BA11 5LA"
            )
            and (losses == "Loss of £2.48")
            and (
                comparison
                == "On a daily commute (5 days a week), you could save up to £9.35 per year if you fill at ASDA located at BA11 5LA rather than this station"
            )
        )

    def test_distance_analysis(self, car):
        analysis = car.distance_analysis("ESSO", "BA11 4NZ", 5.0, 8.0, 1.81)
        assert (
            analysis
            == "ESSO at BA11 4NZ is off route by 5.0 km. It will take you 16.0 mins to make this excursion and cost you £1.81 to drive to and back from the station."
        )

    def test_comparison_inputs(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        capacity, highway, city, combined, model, fuel = car.get_tank_data()
        df_r, df, route, station = car.analysis_dataframes(
            hover, "BA11 5LB", "BA11 5AP", "Unleaded"
        )
        full, min, price, difference, loss, prediction, brand = car.savings_inputs(
            capacity, 40.0, df_r, df
        )
        cheapest_l, cheapest_b, annual = car.comparison_inputs(
            route, city, min, price, df_r
        )
        assert (
            (cheapest_l == "BA11 5LA") and (cheapest_b == "ASDA") and (annual == 7.84)
        )

    def test_distance_inputs(self, car):
        distance, duration, journey_cost = car.distance_inputs(
            "BA11 5LB", "BA11 5AP", "BA11 4NZ", 7.214991344210079, 130.9
        )
        assert (distance == 5.0) and (duration >= 5.0) and (journey_cost == 1.81)

    def test_round_offroutes(self, car):
        df_offroutes = DatabaseModel().read("DirectionsOffRoute")
        df_offroutes = df_offroutes[
            (df_offroutes["origin"] == "BA11 5LB")
            & (df_offroutes["destination"] == "BA11 5AP")
        ]
        latlon = MapboxDirections.generate_latlon("BA11 4NZ")
        df_offroutes, lon, lat = car.round_offroutes(latlon, df_offroutes)
        assert len(df_offroutes) >= 10 and lon == -2.38 and lat == 51.2

    def test_filter_coordinates(self, car):
        df_offroutes = DatabaseModel().read("DirectionsOffRoute")
        df_offroutes = df_offroutes[
            (df_offroutes["origin"] == "BA11 5LB")
            & (df_offroutes["destination"] == "BA11 5AP")
        ]
        latlon = MapboxDirections.generate_latlon("BA11 4NZ")
        df_offroutes, lon, lat = car.round_offroutes(latlon, df_offroutes)
        df_offroute = car.filter_coordinates(df_offroutes, lon, lat)
        assert (abs(df_offroute["lat_destination"].iloc[0]) > 0) and (
            abs(df_offroute["lon_origin"].iloc[0]) > 0
        )

    def test_tank_analysis(self, car):
        highway, city, combined, fuel = car.tank_analysis(10)
        assert (
            (
                highway
                == "Driving on the highway, your current fuel in the tank will take you 92.6 miles. "
            )
            and (
                city
                == "Driving in the city, your current fuel in the tank will take you 52.6 miles. "
            )
            and (
                combined
                == "Driving in both city and highway, your current fuel in the tank will take you 72.1 miles. "
            )
            and (
                fuel
                == "To top up your fule tank to its full capacity, you can put in 40.0 litres of PETROL. "
            )
        )

    def test_get_tank_data(self, car):
        capacity, highway, city, combined, model, fuel = car.get_tank_data()
        assert (
            (capacity == 50.0)
            and (highway == 9.260705353391595)
            and (city == 5.2572650343481975)
            and (combined == 7.214991344210079)
            and (model == "PEUGEOT 206 GTI 180")
            and (fuel == "PETROL")
        )

    def test_savings_inputs(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        capacity, highway, city, combined, model, fuel = car.get_tank_data()
        df_r, df, route, station = car.analysis_dataframes(
            hover, "BA11 5LB", "BA11 5AP", "Unleaded"
        )
        full, min, price, difference, loss, prediction, brand = car.savings_inputs(
            capacity, 40.0, df_r, df
        )
        assert (
            (full == 10.0)
            and (min == 125.7)
            and (price == 130.9)
            and (difference == 5.2)
            and (0.52 == 0.52)
            and (prediction == 130.9)
            and (brand == "ESSO")
        )

    def test_round_offroute(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        capacity, highway, city, combined, model, fuel = car.get_tank_data()
        df_r, df, route, station = car.analysis_dataframes(
            hover, "BA11 5LB", "BA11 5AP", "Unleaded"
        )
        full, min, price, difference, loss, prediction, brand = car.savings_inputs(
            capacity, 40.0, df_r, df
        )
        df_offroutes = DatabaseModel().read("DirectionsOffRoute")
        df_offroutes = df_offroutes[
            (df_offroutes["origin"] == "BA11 5LB")
            & (df_offroutes["destination"] == "BA11 5AP")
        ]
        latlon = MapboxDirections.generate_latlon("BA11 4NZ")
        df_offroutes, lon, lat = car.round_offroutes(latlon, df_offroutes)
        df_offroute = car.filter_coordinates(df_offroutes, lon, lat)
        distance, duration, journey_cost = car.round_offroute(
            df_offroute, combined, price
        )
        assert (distance == 5.0) and (duration > 1.0) and (journey_cost == (1.81))


class TestNearestPump(object):
    @pytest.fixture
    def pump(self):
        return NearestPump("EN1 1AA", "Diesel")

    def test_save(self, pump):
        df = pump.save()
        assert df["Brand"].iloc[0] == "ASDA"

    def test_get_brand_analysis(self, pump):
        supermarket, non_supermarket = pump.get_brand_analysis(get_brand_analysis_input)
        assert supermarket == 5 and non_supermarket == 5

    def test_get_metrics(self, pump):
        df, min, max = pump.get_metrics(get_brand_analysis_input, 5, "Brand")
        assert (len(df) == 8) and (min == 124.64) and (max == 131.9)

    def test_get_data_analysis(self, pump):
        brand_today, postcode_today, distance_today, brand_tomorrow, postcode_tomorrow, distance_tomorrow = pump.get_data_analysis(
            get_brand_analysis_input
        )
        assert (
            (brand_today == "GULF")
            and (postcode_today == "EN3 4EJ")
            and (distance_today == 1.49)
            and (brand_tomorrow == "GULF")
            and (postcode_tomorrow == "EN3 4EJ")
            and (distance_tomorrow == 1.49)
        )

    def test_get_station_prices(self, pump):
        df, brand, station_post_code = pump.get_station_prices(
            "", get_brand_analysis_input
        )
        assert (
            (len(df) == 22) and (brand == "GULF") and (station_post_code == "EN3 4EJ")
        )

    def test_map_routes(self, pump):
        stations_list = [
            "N17 7LY",
            "EN9 1JH",
            "EN8 0TA",
            "N18 3HF",
            "N9 7HL",
            "EN3 4EJ",
            "E4 8ST",
            "EN4 8QX",
            "EN4 0JY",
            "EN8 7RS",
        ]
        routes, df_route = pump.map_routes(stations_list)
        assert (len(df_route) > 0) and (routes[-1] is not None)

    def test_map(self, pump):
        df = pd.read_excel("Test_NearestPump_map_input.xlsx")
        df_route, origin_coordinate, stations, routes = pump.map(df)
        marker = [
            go.Scattermapbox(
                {
                    "hoverinfo": "text",
                    "lat": [51.651933305609],
                    "lon": [-0.077090770465367],
                    "marker": {"color": "black", "size": 16},
                    "mode": "markers",
                    "name": "Results",
                    "text": "EN1 1AA",
                }
            )
        ]
        assert (
            (isinstance(len(df_route), int))
            and (origin_coordinate == marker)
            and (len(stations) == 1)
            and (len(routes) > 1)
        )
