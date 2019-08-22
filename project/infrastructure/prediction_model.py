# [1] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [2] NumPy library used for data processing, URL: https://www.numpy.org/
# [3] StatsModels library - ARIMA class to create an ARIMA model, URL: https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima_model.ARIMA.html
# [4] Pmdarima library - auto_arima function to calculate p,d and q parameters for ARIMA/SARIMAX, URL: http://www.alkaline-ml.com/pmdarima/1.0.0/modules/generated/pmdarima.arima.auto_arima.html
# [5] StatsModels library - rmse function to calculate the root mean squared error value, URL: https://www.statsmodels.org/stable/generated/statsmodels.tools.eval_measures.rmse.html
# [6] StatsModels library - ExponentialSmoothing class to create ExponentialSmoothing predictive model, URL: https://www.statsmodels.org/dev/generated/statsmodels.tsa.holtwinters.ExponentialSmoothing.html
# [7] StatsModels library - SimpleExpSmoothing class to create a Simple Exponential Smoothing model, URL: https://www.statsmodels.org/dev/generated/statsmodels.tsa.holtwinters.SimpleExpSmoothing.html
# [8] Scikit-Learn library - MinMaxScaler class to scale the datasets, URL: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
# [9] Keras API - TimeseriesGenerator class to generate batches of data, URL: https://keras.io/preprocessing/sequence/
# [10] Keras API - Sequential class for compiling and fitting model and prediction, URL: https://keras.io/models/sequential/
# [11] Keras API - Dense class to create a densely connected neural network layer, URL: https://keras.io/layers/core/
# [12] Keras API - LSTM class to create Long Short Term memory layer, URL: https://keras.io/layers/recurrent/
# [13] Dateutil library - relativedelta class to append prediction time horizon to todays date, URL: https://dateutil.readthedocs.io/en/stable/relativedelta.html
# [14] StatsModels library - SARIMAX class to create SARIMAX model, URL: https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
# [15] TensorFlow API - to clear default graph stack, URL: https://www.tensorflow.org/api_docs/python/tf/reset_default_graph
# [16] Keras API - to destroy current TensorFlow graph, URL: https://keras.io/backend/
# [17] Adapted from: Notebook: 06-General-Forecasting-Models/07-Exogenous-Variables-SARIMAX.ipynb, URL: https://www.udemy.com/python-for-time-series-data-analysis/
# [18] Adapted from: Notebook: 06-General-Forecasting-Models/05-ARMA-and-ARIMA.ipynb, URL: https://www.udemy.com/python-for-time-series-data-analysis/
# [19] Adapted from: Author:Andy Hayden, Date:Dec 9 '12 at 9:40, URL:https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it
# [20] Adapted from: Author:yoniLavi, Date:Sep 3 '16 at 21:03, URL:https://stackoverflow.com/questions/16945518/finding-the-index-of-the-value-which-is-the-min-or-max-in-python/16945868
# [21] Adapted from: Notebook: 06-General-Forecasting-Models/00-Introduction-to-Forecasting, URL: https://www.udemy.com/python-for-time-series-data-analysis/
# [22] Adapted from: Notebook: 05-Time-Series-Analysis-with-Statsmodels/03-Holt-Winters-Methods, URL: https://www.udemy.com/python-for-time-series-data-analysis/
# [23] Adapted from: https://www.statsmodels.org/dev/examples/notebooks/generated/exponential_smoothing.html
# [24] Adapted from: Author: Nader Hisham, Date:Oct 5 '17 at 3:53, URL:https://stackoverflow.com/questions/18837262/convert-python-dict-into-a-dataframe
# [25] Adapted from: Author: Michael Hoff, Date:Jul 23 '16 at 13:42, URL:https://stackoverflow.com/questions/38542419/could-pandas-use-column-as-index
# [26] Source: Notebook 07-Deep-Learning-Models/01-RNN-Example.ipynb, URL:https://www.udemy.com/python-for-time-series-data-analysis/
# [27] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.tail.html
# [28] Adapted from: Author:lexual, Date:Jul 6 '12 at 1:48, URL:https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
# [29] Adapted from: Author: Mahendra, Date:Dec 10 '10 at 6:22, URL:https://stackoverflow.com/questions/546321/how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime/4406260#4406260
# [30] Adapted from: Author:Steve B., Date:Jan 13 '09 at 22:41, URL:https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date/441152#441152
# [31] Source: Author:g-eoj, Date:Sep 2 '18 at 23:39, URL:https://stackoverflow.com/questions/52133347/how-can-i-clear-a-model-created-with-keras-and-tensorflowas-backend
# [32] Source: Author:Phizaz, Date:Sep 2 '18 at 17:28, URL:https://stackoverflow.com/questions/52133347/how-can-i-clear-a-model-created-with-keras-and-tensorflowas-backend


from .model import Model
import pandas as pd  # [1]
import numpy as np  # [2]
from statsmodels.tsa.arima_model import ARIMA  # [3]
from pmdarima import auto_arima  # [4]
from statsmodels.tools.eval_measures import rmse  # [5]
from statsmodels.tsa.holtwinters import ExponentialSmoothing  # [6]
from statsmodels.tsa.holtwinters import SimpleExpSmoothing  # [7]
from sklearn.preprocessing import MinMaxScaler  # [8]
from keras.preprocessing.sequence import TimeseriesGenerator  # [9]
from keras.models import Sequential  # [10]
from keras.layers import Dense  # [11]
from keras.layers import LSTM  # [12]
from dateutil.relativedelta import relativedelta  # [13]
from datetime import date, timedelta
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX  # [14]
import tensorflow
import keras


class SARIMAXModel(Model):
    def __init__(self, fuel_type, horizon, df):
        self.fuel_type = fuel_type
        self.horizon = int(horizon)
        self.df = df
        self.error = None

    def prepare_test(self, df, df1):  # [17]
        exog_name = self.fuel_type + "-wholesale"
        return df[len(df1) :][[exog_name]]

    def fit(self, df1, p, d, q):  # [17]
        exog_name = self.fuel_type + "-wholesale"
        model = SARIMAX(
            df1[self.fuel_type],
            exog=df1[exog_name],
            order=(p, d, q),
            enforce_invertibility=False,
        )
        return model.fit()

    def compile(self, df1):  # [17]
        (p, d, q) = auto_arima(df1[self.fuel_type]).order
        return p, d, q

    def evaluate(self, df1, df, p, d, q):  # [17]
        l_updated = len(df1) - self.horizon
        train = df1.iloc[:l_updated]
        test = df1.iloc[l_updated:]
        exog_name = self.fuel_type + "-wholesale"
        model = SARIMAX(
            train[self.fuel_type],
            exog=train[exog_name],
            order=(p, d, q),
            enforce_invertibility=False,
        )
        results = model.fit()
        start = len(train)
        end = len(train) + len(test) - 1
        predictions = results.predict(start=start, end=end, exog=test[[exog_name]])
        self.error = rmse(test[self.fuel_type], predictions)  # [18]
        return self.error

    def clean(self):  # [17]
        return self.df.dropna()

    def prepare_training(self, df1):  # [17]
        sliced_length = len(df1) + self.horizon
        return self.df[0:sliced_length]

    def initialise(self):  # [17]
        df1 = self.clean()
        df = self.prepare_training(df1)
        p, d, q = self.compile(df1)
        model = self.fit(df1, p, d, q)
        error = self.evaluate(df1, df, p, d, q)
        exog_forecast = self.prepare_test(df, df1)
        fcast = model.predict(
            len(df1), len(df1) + (self.horizon - 1), exog=exog_forecast
        )
        return fcast

    def predict(self):  # [19]
        fcast = self.initialise()
        date_horizon = date.today()
        idx = pd.date_range(str(date_horizon), periods=self.horizon, freq="M")
        cols = ["Prediction"]
        df = pd.DataFrame(fcast.values, idx, cols)
        return df


class PredictionModel:
    def __init__(
        self,
        df,
        horizon,
        name=None,
        fuel=None,
        frequency=None,
        brand=None,
        post_code=None,
        sarimax=False,
    ):
        self.df = df
        self.name = name
        self.horizon = horizon
        self.fuel_type = fuel
        self.frequency = frequency
        self.brand = brand
        self.post_code = post_code
        self.sarimax = sarimax
        self.sarimax_error = None
        self.arima_error = None
        self.rnn_error = None
        self.stat_error = None

    def prepare(self):  # [17]
        self.df.dropna(inplace=True)
        column = self.fuel_type + "-wholesale"
        self.df.drop([column], axis=1, inplace=True)
        return None

    def sarimax_model(self):
        sarimax_model = SARIMAXModel(self.fuel_type, self.horizon, self.df)
        prediction = sarimax_model.predict()
        self.sarimax_error = sarimax_model.error
        return prediction

    def arima_model(self):
        arima_model = ARIMAModel(
            self.df, self.name, self.horizon, self.fuel_type, self.brand, self.post_code
        )
        prediction = arima_model.predict()
        self.arima_error = arima_model.error
        return prediction

    def rnn_model(self):
        if self.frequency == "D":
            rnn_model = RNNModel(1, self.df, self.horizon, self.name, "D")
        elif self.frequency == "M":
            rnn_model = RNNModel(1, self.df, self.horizon, self.name, "M")
        prediction = rnn_model.predict()
        self.rnn_error = rnn_model.error
        return prediction

    def stat_model(self):
        stat_model = ExponentialSmoothingModel(
            self.df, self.name, self.horizon, self.fuel_type, self.brand, self.post_code
        )
        prediction = stat_model.predict()
        self.stat_error = stat_model.error
        return prediction

    def evaluate(self):
        if self.sarimax == True:
            error_values = [
                self.arima_error,
                self.sarimax_error,
                self.rnn_error,
                self.stat_error,
            ]
        else:
            try:
                error_values = [self.arima_error, self.rnn_error, self.stat_error]
                if None in error_values:
                    raise ValueError
            except ValueError as e:
                error_values = [self.rnn_error, self.stat_error]
        return min(range(len(error_values)), key=error_values.__getitem__)  # [20]

    def update_rnn_model(self):
        rnn_model = RNNModel(1, self.df, self.horizon, self.name, self.frequency)
        return rnn_model.update(self.df, self.fuel_type, self.brand, self.post_code)

    def predict(self):
        if self.sarimax == True:
            sarimax_model_df = self.sarimax_model()
            self.prepare()
        try:
            arima_model_df = self.arima_model()
        except Exception as e:
            arima_model_df = self.stat_model()
        rnn_model_df = self.rnn_model()
        stat_model_df = self.stat_model()
        optimum_model = self.evaluate()
        try:
            if optimum_model < 2:
                df = arima_model_df
            elif optimum_model < 5:
                df = stat_model_df
            elif optimum_model == 5:
                df = rnn_model_df
                if self.post_code != "N/A":
                    df = self.update_rnn_model()
            else:
                df = sarimax_model_df
        except ValueError as e:
            df = stat_model_df
        return df


class ExponentialSmoothingModel(Model):
    def __init__(self, df, name, horizon, fuel, brand, post_code):
        self.df = df
        self.name = name
        self.horizon = horizon
        self.fuel = fuel
        self.brand = brand
        self.post_code = post_code
        self.error_simple = None
        self.error_smoothing = None
        self.error_add = None
        self.error_mul = None
        self.error = None

    def calculate_error(self, model, train, test, name):  # [21] [22]
        start = len(train)
        end = len(train) + len(test) - 1
        predictions = model.predict(start=start, end=end)
        error = rmse(test[name], predictions)  # [18]
        return error

    def evaluate_simple(self, train, test, name):  # [21] [22]
        model = ExponentialSmoothing(train[name]).fit()
        error = self.calculate_error(model, train, test, name)
        return error

    def evaluate_smoothing(self, train, test, name):  # [21] [22]
        model = SimpleExpSmoothing(train[name]).fit(
            smoothing_level=2 / (12 + 1), optimized=False
        )
        error = self.calculate_error(model, train, test, name)
        return error

    def evaluate_add(self, train, test, name):  # [21] [22]
        model = ExponentialSmoothing(train[name], trend="add").fit()
        error = self.calculate_error(model, train, test, name)
        return error

    def evaluate_multiplicative(self, train, test, name):  # [21] [22]
        model = ExponentialSmoothing(
            train[name], trend="mul", seasonal="mul", seasonal_periods=12
        ).fit()
        error = self.calculate_error(model, train, test, name)
        return error

    def evaluate(self):  # [18]
        l_updated = len(self.df) - self.horizon
        train = self.df.iloc[:l_updated]
        test = self.df.iloc[l_updated:]
        self.error_simple = self.evaluate_simple(train, test, self.name)

        self.error_smoothing = self.evaluate_smoothing(train, test, self.name)

        self.error_add = self.evaluate_add(train, test, self.name)

        try:
            self.error_mul = self.evaluate_multiplicative(train, test, self.name)
        except Exception as e:
            self.error_mul = self.evaluate_add(train, test, self.name)

        return None

    def fit(self, minimum_error_model):  # [21] [22]
        if minimum_error_model == self.error_simple:
            results = ExponentialSmoothing(self.df[self.name]).fit()
            model_selected = "Simple"
        elif minimum_error_model == self.error_smoothing:
            results = SimpleExpSmoothing(self.df[self.name]).fit(
                smoothing_level=2 / (12 + 1), optimized=False  # [23]
            )
            model_selected = "Smoothing"
        elif minimum_error_model == self.error_add:
            results = ExponentialSmoothing(self.df[self.name], trend="add").fit()
            model_selected = "Additive"
        elif minimum_error_model == self.error_mul:
            results = ExponentialSmoothing(self.df[self.name], trend="mul").fit()
            model_selected = "Multiplicative"
        return {"model": results, "selected_model": model_selected}

    def predict(self):  # [18]
        self.evaluate()
        minimum_error = min(
            [self.error_simple, self.error_smoothing, self.error_add, self.error_mul]
        )
        self.error = minimum_error
        model = self.fit(minimum_error)
        fcast = model["model"].predict(len(self.df), len(self.df) + (self.horizon - 1))
        forecast_price = []
        for i in range(len(fcast)):

            forecast_price.append(
                {
                    "Date": fcast.index[i],
                    "Prediction": fcast[i],
                    "Error": minimum_error,
                    "Model": model["selected_model"],
                    "Fuel": self.fuel,
                    "Brand": self.brand,
                    "Post Code": self.post_code,
                }
            )
        df1 = pd.DataFrame(forecast_price)  # [24]
        df1.set_index("Date", inplace=True)  # [25]
        return df1


class ARIMAModel(Model):
    def __init__(self, df, name, horizon, fuel, brand, post_code):
        self.df = df
        self.name = name
        self.horizon = horizon
        self.fuel = fuel
        self.brand = brand
        self.post_code = post_code
        self.error = None

    def evaluate(self, p, d, q):  # [18]
        l_updated = len(self.df) - self.horizon
        train = self.df.iloc[:l_updated]
        test = self.df.iloc[l_updated:]
        model = ARIMA(train[self.name], order=(p, d, q)).fit()
        start = len(train)
        end = len(train) + len(test) - 1
        predictions = model.predict(start=start, end=end, dynamic=False, typ="levels")
        self.error = rmse(test[self.name], predictions)
        return self.error

    def fit(self, p, d, q):  # [18]
        model = ARIMA(self.df[self.name], order=(p, d, q))
        results = model.fit()
        model_selected = f"ARIMA({p,d,q})"
        return {"model": results, "selected_model": model_selected}

    def predict(self):  # [18]
        (p, d, q) = auto_arima(self.df[self.name], seasonal=False).order
        error = self.evaluate(p, d, q)
        model = self.fit(p, d, q)
        fcast = model["model"].predict(
            len(self.df), len(self.df) + (self.horizon - 1), typ="levels"
        )
        forecast_price = []
        for i in range(len(fcast)):

            forecast_price.append(
                {
                    "Date": fcast.index[i],
                    "Prediction": fcast[i],
                    "Error": error,
                    "Model": model["selected_model"],
                    "Fuel": self.fuel,
                    "Brand": self.brand,
                    "Post Code": self.post_code,
                }
            )
        df1 = pd.DataFrame(forecast_price)  # [24]
        df1.set_index("Date", inplace=True)  # [25]
        return df1


class RNNModel(Model):
    def __init__(self, epoch, df, horizon, feature, frequency):
        self.epoch = epoch
        self.df = df
        self.horizon = horizon
        self.feature = feature
        self.frequency = frequency
        self.error = None

    def fit(self, scaled_train, scaled_test, n_input, n_features):  # [26]
        generator = TimeseriesGenerator(
            scaled_train, scaled_train, length=n_input, batch_size=1
        )
        model = Sequential()
        model.add(LSTM(100, activation="relu", input_shape=(n_input, n_features)))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        model.fit_generator(generator, epochs=self.epoch)
        return model

    def get_model(self, scaled_train, scaled_test, n_input, n_features):  # [26]

        model = self.fit(scaled_train, scaled_test, n_input, n_features)
        return model

    def compile(self, test, scaled_train, model):  # [26]
        n_input = self.horizon
        n_features = 1
        first_eval_batch = scaled_train[-self.horizon :]
        first_eval_batch = first_eval_batch.reshape((1, n_input, n_features))
        model.predict(first_eval_batch)
        test_predictions = []
        first_eval_batch = scaled_train[-n_input:]
        current_batch = first_eval_batch.reshape((1, n_input, n_features))
        np.append(current_batch[:, 1:, :], [[[99]]], axis=1)
        test_predictions = []
        first_eval_batch = scaled_train[-n_input:]
        current_batch = first_eval_batch.reshape((1, n_input, n_features))
        for i in range(len(test) + self.horizon):
            current_pred = model.predict(current_batch)[0]
            test_predictions.append(current_pred)
            current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
        return test_predictions

    def evaluate(self, test, data):  # [18]
        test["Predictions"] = data
        self.error = rmse(test[self.feature], test["Predictions"])
        return self.error

    def update(self, df, fuel, brand, post_code):
        df = df.tail(1)  # [27]
        df.rename(columns={self.feature: "Prediction"}, inplace=True)  # [28]
        df["Error"] = self.error
        df["Model"] = "Neural Network"
        df["Fuel"] = fuel
        df["Brand"] = brand
        df["Post Code"] = post_code
        return df

    def predict_index(self):
        if (self.frequency == "D") and (self.feature != "Classification"):
            date_horizon = date.today() + relativedelta(
                months=-(self.horizon - 1)
            )  # [29]
        elif (self.frequency == "D") and (self.feature == "Classification"):
            today = datetime.datetime.today()
            date_horizon = today - timedelta(days=self.horizon)  # [30]
        elif self.frequency == "M":
            date_horizon = date.today() + relativedelta(
                months=-(self.horizon - 1)
            )  # [29]
        idx = pd.date_range(
            str(date_horizon), periods=self.horizon * 2, freq=self.frequency
        )  # [19]
        return idx

    def reset(self):
        try:
            keras.backend.clear_session()  # [31]
            tensorflow.reset_default_graph()  # [32]
        except UnboundLocalError:
            pass
        return None

    def predict(self):  # [26] #[18]
        length = len(self.df) - self.horizon
        train = self.df.iloc[:length]
        test = self.df.iloc[length:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        model = self.get_model(scaled_train, scaled_test, self.horizon, 1)
        test_predictions = self.compile(test, scaled_train, model)
        data = scaler.inverse_transform(test_predictions)
        error = self.evaluate(test, data[0 : len(test)])
        idx = self.predict_index()
        df = pd.DataFrame(data, idx, [self.feature])  # [19]
        self.reset()
        return df
