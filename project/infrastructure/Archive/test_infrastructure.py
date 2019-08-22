# [1] Pytest library is used to write the unit and integration tests using @pytest.fixture and the in built python assert statement, URL: https://docs.pytest.org/en/latest/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
# [4] Adapted from: File:06-General-Forecasting-Models/05-ARMA-and-ARIMA.ipynb, URL: https://www.udemy.com/python-for-time-series-data-analysis/
# [5] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
# [6] Adapted from: Author:Andy Hayden, Date:May 24 '13 at 7:31, URL:https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [7] Adapted from: Author:LondonRob, Date:Aug 9 '13 at 11:12, URL:https://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe
# [8] Adapted from: Notebook:07-Deep-Learning-Models/01-RNN-Example.ipynb, URL: https://www.udemy.com/python-for-time-series-data-analysis/

import pytest  # [1]
from .utility import *
from .prediction_model import *
from .database import *
import pandas as pd  # [2]
from ..snapshot_app.average_price import *
from ..infrastructure.database import DatabaseModel


class TestUtility(object):
    def test_get_today_date(self):
        print(Utility.get_today_date())
        assert isinstance(Utility.get_today_date(), str)

    def test_to_uppercase(self):
        print(Utility.to_uppercase("abc"))
        assert Utility.to_uppercase("abc") == "ABC"

    def test_to_dataframe(self):
        print(Utility.to_dataframe({}))
        assert not isinstance(Utility.to_dataframe({}), dict)


class TestExponentialSmoothingModel(object):
    @pytest.fixture
    def model(self):
        df = pd.read_excel("Testing_ArimaModel_init.xlsx", index_col=0)  # [3]
        return ExponentialSmoothingModel(df, "Price", 1, "Unleaded", "ASDA", "BA11 5LA")

    @pytest.fixture
    def data(self):  # [4]
        df = pd.read_excel("Testing_ArimaModel_init.xlsx", index_col=0)  # [3]
        model = ExponentialSmoothingModel(
            df, "Price", 1, "Unleaded", "ASDA", "BA11 5LA"
        )
        l_updated = len(model.df) - model.horizon
        train = model.df.iloc[:l_updated]
        test = model.df.iloc[l_updated:]
        return (train, test)

    def test_calculate_error(self, model, data):
        m = ExponentialSmoothing(data[0][model.name]).fit()
        error = model.calculate_error(m, data[0], data[1], model.name)
        error_2 = model.evaluate_simple(data[0], data[1], model.name)
        print(error, error_2)
        assert error == error_2

    def test_evaluate_simple(self, model, data):
        error = model.evaluate_simple(data[0], data[1], model.name)
        print(error)
        assert isinstance(error, float)

    def test_evaluate_smoothing(self, model, data):
        error = model.evaluate_smoothing(data[0], data[1], model.name)
        print(error)
        assert error < 0.5

    def test_evaluate_add(self, model, data):
        error = model.evaluate_add(data[0], data[1], model.name)
        print(error)
        assert error == 0.0625

    def test_evaluate_multiplicative(self, model, data):
        error = model.evaluate_multiplicative(data[0], data[1], model.name)
        print(model.error_mul)
        assert model.error_mul == None

    def test_evauate(self, model):
        model.evaluate()
        print(model.error_simple)
        assert isinstance(model.error_simple, (int, float))

    def test_fit(self, model):
        model.evaluate()
        minimum_error = min(
            [
                model.error_simple,
                model.error_smoothing,
                model.error_add,
                model.error_mul,
            ]
        )
        model = model.fit(minimum_error)
        print(model)
        assert isinstance(model["selected_model"], str)

    def test_predict(self, model):
        df = model.predict()
        print(df)
        assert len(df) == 1


class TestARIMAModel(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def model(self):
        df = AveragePrice("unleaded", 1).prepare_timeseries()
        df = df.dropna()  # [5]
        print(df)
        return ARIMAModel(df, "unleaded", 1, "unleaded", "N/A", "N/A")

    def test_evaluate(self, model):  # [4]
        (p, d, q) = auto_arima(model.df[model.name], seasonal=False).order
        error = model.evaluate(p, d, q)
        print(error)
        assert isinstance(error, float)

    def test_fit(self, model):  # [4]
        (p, d, q) = auto_arima(model.df[model.name], seasonal=False).order
        model = model.fit(p, d, q)
        print(model)
        assert model["selected_model"].split("(")[0] == "ARIMA"

    def test_predict(self, model):
        df = model.predict()
        print(df)
        assert len(df) == 1


class TestSARIMAXModel(object):
    @pytest.fixture
    def sarimax(self):
        df = AveragePrice("unleaded", 1).prepare_timeseries()
        return SARIMAXModel("unleaded", 1, df)

    def test_init(self, sarimax):
        print(sarimax.fuel_type)
        assert sarimax.fuel_type == "unleaded"

    def test_prepare_test(self, sarimax):
        df = sarimax.clean()
        df_training = sarimax.prepare_training(df)
        exog_forecast = sarimax.prepare_test(df_training, df)
        print(exog_forecast)
        assert len(exog_forecast) == 1

    def test_evaluate(self, sarimax):
        df = sarimax.clean()
        p, d, q = sarimax.compile(df)
        df_training = sarimax.prepare_training(df)
        error = sarimax.evaluate(df, df_training, p, d, q)
        print(error)
        assert error >= 0

    def test_fit(self, sarimax):
        df = sarimax.clean()
        p, d, q = sarimax.compile(df)
        model = sarimax.fit(df, p, d, q)
        print(model)
        assert (
            str(model).split(" ")[0]
            == "<statsmodels.tsa.statespace.sarimax.SARIMAXResultsWrapper"
        )

    def test_compile(self, sarimax):
        df = sarimax.clean()
        p, d, q = sarimax.compile(df)
        print(p, d, q)
        assert p >= 0

    def test_clean(self, sarimax):
        df = sarimax.clean()
        print(df)
        assert len(sarimax.df) > len(df)

    def test_prepare_training(self, sarimax):
        df = sarimax.clean()
        df_training = sarimax.prepare_training(df)
        print(df_training)
        assert len(df) == 54

    def test_initialise(self, sarimax):
        fcast = sarimax.initialise()
        print(fcast)
        assert len(fcast) == 1

    def test_predict(self, sarimax):
        df = sarimax.predict()
        print(df)
        assert isinstance(df["Prediction"].iloc[0], (int, float))  # [6]


class TestPredictionModel(object):
    @pytest.fixture
    def model(self):
        df = AveragePrice("unleaded", 1).prepare_timeseries()
        return PredictionModel(df, 1, "unleaded", "unleaded", "M", "N/A", "N/A", True)

    @pytest.fixture
    def cleaned_model(self):
        df = AveragePrice("unleaded", 1).prepare_timeseries()
        df = df.dropna()  # [5]
        df = df.drop(["unleaded-wholesale"], axis=1)  # [7]
        return PredictionModel(df, 1, "unleaded", "unleaded", "M", "N/A", "N/A", False)

    def test_prepare(self, model):
        model.prepare()
        print(model.df)
        assert len(model.df) == 54

    def test_sarimax_model(self, model):
        model.sarimax_model()
        print(model.sarimax_error)
        assert isinstance(model.sarimax_error, (int, float))

    def test_arima_model(self, cleaned_model):
        cleaned_model.arima_model()
        print(cleaned_model.arima_error)
        assert isinstance(cleaned_model.arima_error, (int, float))

    def test_rnn_model(self, cleaned_model):
        cleaned_model.rnn_model()
        print(cleaned_model.rnn_error)
        assert isinstance(cleaned_model.rnn_error, (int, float))

    def test_stat_model(self, cleaned_model):
        cleaned_model.stat_model()
        print(cleaned_model.stat_error)
        assert isinstance(cleaned_model.stat_error, (int, float))

    def test_predict(self, model):
        df = model.predict()
        print(df)
        assert len(df) == 1

    def test_evaluate(self, cleaned_model):
        cleaned_model.arima_model()
        cleaned_model.rnn_model()
        cleaned_model.stat_model()
        error = cleaned_model.evaluate()
        print(error)
        assert isinstance(error, (int, float))

    def test_update_rnn_model(self, cleaned_model):
        df = cleaned_model.update_rnn_model()
        print(df)
        assert len(df) == 1


class TestRNNModel(object):
    @pytest.fixture
    def engine(self):
        df = AveragePrice("unleaded", 1).prepare_timeseries()
        df = df.dropna()
        df = df.drop(["unleaded-wholesale"], axis=1)  # [7]
        return RNNModel(1, df, 1, "unleaded", "M")

    def test_get_model(self, engine):  # [8]
        length = len(engine.df) - engine.horizon
        train = engine.df.iloc[:length]
        test = engine.df.iloc[length:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        model = engine.get_model(scaled_train, scaled_test, engine.horizon, 1)
        print(model)
        assert len(str(model)) > 5

    def test_compile(self, engine):  # [8]
        length = len(engine.df) - engine.horizon
        train = engine.df.iloc[:length]
        test = engine.df.iloc[length:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        model = engine.get_model(scaled_train, scaled_test, engine.horizon, 1)
        test_predictions = engine.compile(test, scaled_train, model)
        print(test_predictions)
        assert len(test_predictions) == 2

    def test_evaluate(self, engine):  # [8]
        length = len(engine.df) - engine.horizon
        train = engine.df.iloc[:length]
        test = engine.df.iloc[length:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        model = engine.get_model(scaled_train, scaled_test, engine.horizon, 1)
        test_predictions = engine.compile(test, scaled_train, model)
        data = scaler.inverse_transform(test_predictions)
        error = engine.evaluate(test, data[0 : len(test)])
        print(error)
        assert error >= 0

    def test_update(self, engine):
        df = engine.predict()
        df = engine.update(df, "unleaded", "TESCO", "EN1 1AA")
        print(df)
        assert len(df) == 1

    def test_update(self, engine):
        df = engine.predict()
        df = engine.update(df, "unleaded", "TESCO", "EN1 1AA")
        print(df)
        assert len(df) == 1

    def test_predict_index(self, engine):
        idx = engine.predict_index()
        print(idx)
        assert len(idx) == 2

    def test_reset(self, engine):
        result = engine.reset()
        print(result)
        assert result == None

    def test_fit(self, engine):  # [8]
        length = len(engine.df) - engine.horizon
        train = engine.df.iloc[:length]
        test = engine.df.iloc[length:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        model = engine.fit(scaled_train, scaled_test, engine.horizon, 1)
        print(model)
        assert len(str(model)) > 5

    def test_predict(self, engine):
        df = engine.predict()
        print(df)
        assert len(df) == 2
