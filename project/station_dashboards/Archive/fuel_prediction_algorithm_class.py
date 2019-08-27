import pandas as pd
import numpy as np

# Load specific forecasting tools
from statsmodels.tsa.arima_model import ARMA, ARMAResults, ARIMA, ARIMAResults
from statsmodels.graphics.tsaplots import (
    plot_acf,
    plot_pacf,
)  # for determining (p,q) orders
from pmdarima import auto_arima  # for determining ARIMA orders
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.tools import diff

from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


class ArimaModel:
    def __init__(self, df, name, horizon, fuel, brand, post_code):
        # df.to_excel("Testing_ArimaModel_init.xlsx")
        self.df = df
        self.name = name
        self.horizon = horizon
        self.fuel = fuel
        self.brand = brand
        self.post_code = post_code
        # self.prediction = self.prediction()
        self.error = None
        self.error_simple = None
        self.error_smoothing = None
        self.error_add = None
        self.error_mul = None
        # print((self.name,self.horizon,self.fuel,self.brand,self.post_code,"ArimaModel init output")

    # tested
    def arima_predict(self, model, train, test, name):
        # print((model,"ArimaModel arima_predict input")
        start = len(train)
        end = len(train) + len(test) - 1
        predictions = model.predict(start=start, end=end, dynamic=False, typ="levels")
        error = rmse(test[name], predictions)
        # print((error,"ArimaModel arima_predict output")
        return error

    # tested
    def non_arima_predict(self, model, train, test, name):
        # print((model,"ArimaModel predict input")
        start = len(train)
        end = len(train) + len(test) - 1
        predictions = model.predict(start=start, end=end)
        error = rmse(test[name], predictions)
        # print((error,"ArimaModel predict output")
        return error

    # tested
    def arima_predictions(self, train, test, name, p, d, q):
        # print((train, test, name,p,d,q,"ArimaModel arima_predictions input")
        model = ARIMA(train[name], order=(p, d, q)).fit()
        error = self.arima_predict(model, train, test, name)
        # print((error,"ArimaModel arima_predictions output")
        return error
        # start=len(train)
        # end=len(train)+len(test)-1
        # predictions = results.predict(start=start, end=end, dynamic=False, typ='levels')
        # error = rmse(test[name], predictions)
        # return error

    # tested
    def simple_predictions(self, train, test, name):
        # print((train, test, name,"ArimaModel simple_predictions input")
        model = ExponentialSmoothing(train[name]).fit()
        error = self.non_arima_predict(model, train, test, name)
        # print((error,"ArimaModel simple_predictions output")
        return error
        # start=len(train)
        # end=len(train)+len(test)-1
        # predictions = results.predict(start=start, end=end)
        # error = rmse(test[name], predictions)
        # return error

    # tested
    def smoothed_predictions(self, train, test, name):
        # print((train, test, name,"ArimaModel smoothed_predictions input")
        model = SimpleExpSmoothing(train[name]).fit(
            smoothing_level=2 / (12 + 1), optimized=False
        )
        error = self.non_arima_predict(model, train, test, name)
        # print((error,"ArimaModel smoothed_predictions output")
        return error
        # start=len(train)
        # end=len(train)+len(test)-1
        # predictions = results.predict(start=start, end=end)
        # error = rmse(test[name], predictions)
        # return error

    # tested
    def additive_predictions(self, train, test, name):
        # print((train, test, name,"ArimaModel additive_predictions input")
        model = ExponentialSmoothing(train[name], trend="add").fit()
        error = self.non_arima_predict(model, train, test, name)
        # print((error,"ArimaModel additive_predictions output")
        return error
        # start=len(train)
        # end=len(train)+len(test)-1
        # predictions = results.predict(start=start, end=end)
        # error = rmse(test[name], predictions)
        # return error

    # tested
    def multiplicative_predictions(self, train, test, name):
        # print((train, test, name,"ArimaModel multiplicative_predictions input")
        model = ExponentialSmoothing(
            train[name], trend="mul", seasonal="mul", seasonal_periods=12
        ).fit()
        error = self.non_arima_predict(model, train, test, name)
        # print((error,"ArimaModel multiplicative_predictions output")
        return error
        # start=len(train)
        # end=len(train)+len(test)-1
        # predictions = results.predict(start=start, end=end)
        # error = rmse(test[name], predictions)
        # #print((error,"ArimaModel multiplicative_predictions output")
        # return error

    # tested
    def split_datasets(self):
        l_updated = len(self.df) - self.horizon
        train = self.df.iloc[:l_updated]
        test = self.df.iloc[l_updated:]
        # print((train,test,"ArimaModel split_datasets input")
        return train, test

    # tested
    def set_errors(self, p, d, q):
        # print((p,d,q,"ArimaModel set_errors input")
        train, test = self.split_datasets()
        try:
            self.error = self.arima_predictions(train, test, self.name, p, d, q)
        except Exception as e:
            # print((e,"ARIMA ALGORITHM ERROR")
            self.error = self.simple_predictions(train, test, self.name)

        self.error_simple = self.simple_predictions(train, test, self.name)

        self.error_smoothing = self.smoothed_predictions(train, test, self.name)

        self.error_add = self.additive_predictions(train, test, self.name)

        try:
            self.error_mul = self.multiplicative_predictions(train, test, self.name)
        except Exception as e:
            # print((e,"ARIMA ALGORITHM ERROR")
            self.error_mul = self.additive_predictions(train, test, self.name)
        # print((self.error,self.error_simple,self.error_smoothing,self.error_add,self.error_mul,"ArimaModel set_errors output")

    # def fit_arima(self,p,d,q):
    #     #print((p,d,q,"ArimaModel fit_arima input")
    #     if (p == 2) and (d == 1) and (q == 2):
    #         results = ExponentialSmoothing(self.df[self.name]).fit()
    #         model_selected = "Simple"
    #         error = self.error_simple
    #     else:
    #         model = ARIMA(self.df[self.name],order=(p,d,q))
    #         results = model.fit()
    #         model_selected = f'ARIMA({p,d,q})'
    #         error = self.error
    #     #print((results,model_selected,error,"ArimaModel fit_arima output")
    #     return results,model_selected,error

    # tested
    def fit(self, minimum_error_model, p, d, q):
        # print((minimum_error_model,p,d,q,"ArimaModel fit input")
        if minimum_error_model == self.error_simple:
            results = ExponentialSmoothing(self.df[self.name]).fit()
            model_selected = "Simple"
            error = self.error_simple
        elif minimum_error_model == self.error_smoothing:
            results = SimpleExpSmoothing(self.df[self.name]).fit(
                smoothing_level=2 / (12 + 1), optimized=False
            )
            model_selected = "Smoothing"
            error = self.error_smoothing
        elif minimum_error_model == self.error_add:
            results = ExponentialSmoothing(self.df[self.name], trend="add").fit()
            model_selected = "Additive"
            error = self.error_add
        elif minimum_error_model == self.error_mul:
            results = ExponentialSmoothing(self.df[self.name], trend="mul").fit()
            model_selected = "Multiplicative"
            error = self.error_mul
        else:
            if (p == 2) and (d == 1) and (q == 2):
                results = ExponentialSmoothing(self.df[self.name]).fit()
                model_selected = "Simple"
                error = self.error_simple
            else:
                model = ARIMA(self.df[self.name], order=(p, d, q))
                results = model.fit()
                model_selected = f"ARIMA({p,d,q})"
                error = self.error
        # print((results,model_selected,error,"ArimaModel fit output")
        return results, model_selected, error

    # tested
    def forecast_price(self, model_selected, results, p, d, q):
        # print((model_selected,results,p,d,q,"ArimaModel forecast_price input")
        if model_selected == f"ARIMA({p,d,q})":
            result = results.predict(
                len(self.df), len(self.df) + (self.horizon - 1), typ="levels"
            )
        else:
            result = results.predict(len(self.df), len(self.df) + (self.horizon - 1))
        # print((result,"ArimaModel forecast_price output")
        return result

    # tested
    def prediction(self):
        (p, d, q) = auto_arima(self.df[self.name], seasonal=False).order
        self.set_errors(p, d, q)
        minimum_error = min(
            [
                self.error,
                self.error_simple,
                self.error_smoothing,
                self.error_add,
                self.error_mul,
            ]
        )
        model_selected = None
        results, model_selected, error = self.fit(minimum_error, p, d, q)
        fcast = self.forecast_price(model_selected, results, p, d, q)
        # print((fcast,"testing inside prediction method")
        forecast_price = []
        for i in range(len(fcast)):
            # print((i,range(len(fcast)))
            # print((fcast[i],"error")
            forecast_price.append(
                {
                    "Date": fcast.index[i],
                    "Prediction": fcast[i],
                    "Error": error,
                    "Model": model_selected,
                    "Fuel": self.fuel,
                    "Brand": self.brand,
                    "Post Code": self.post_code,
                }
            )
        df1 = pd.DataFrame(forecast_price)
        df1.set_index("Date", inplace=True)
        # print((df1,"ArimaModel prediction output")
        return df1
