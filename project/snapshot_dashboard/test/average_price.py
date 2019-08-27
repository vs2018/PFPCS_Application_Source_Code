import pandas as pd

from database import DatabaseModel
from prediction_model import PredictionModel
from utility import Utility


class AveragePrice:
    # tested
    def __init__(self, fuel_type, horizon, region=None):
        self.region = region
        self.fuel_type = fuel_type
        self.horizon = int(horizon)
        self.update_horizon()
        # print(fuel_type,horizon,region,"AggregatePriceModel init variables")

    # tested
    def update_horizon(self):
        if (self.region is None) and "supermarket" in self.fuel_type:
            if self.horizon == 1:
                self.horizon = 31
            elif self.horizon == 3:
                self.horizon = 91
            elif self.horizon == 6:
                self.horizon = 181
        return None

    # Adapted from https://www.oipapio.com/question-4559816
    def first_day(self, df):
        if len(df):
            # print(entry[0],"first day output")
            return df[0]

    # tested

    def prepare_timeseries(self):
        if self.region:
            data = DatabaseModel().read("aggregate", self.fuel_type)
            df = Utility.to_datetimeindex(data)
            # df = pd.read_excel(self.fuel_type, index_col='Date', parse_dates=True)
            # Adapted from mrbTT, Oct 26 '18 at 17:31, https://stackoverflow.com/questions/46217529/pandas-datetimeindex-frequency-is-none-and-cant-be-set
            df.index.freq = "M"
            # Adapted from johnchase, Jan 8 '16 at 17:51, https://stackoverflow.com/questions/34682828/extracting-specific-selected-columns-to-new-dataframe-as-a-copy
            df = df[[self.region]].copy()
            print(df, "region_vishal")
        elif "supermarket" in self.fuel_type:
            data = DatabaseModel().read("aggregate", "supermarket")
            df = Utility.to_datetimeindex(data)
            # df = pd.read_excel('supermarket-comparison.xlsx', index_col='Date', parse_dates=True)
            # Adapted from https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
            df = df.resample(rule="1D").interpolate()
            # Adapted from johnchase, Jan 8 '16 at 17:51, https://stackoverflow.com/questions/34682828/extracting-specific-selected-columns-to-new-dataframe-as-a-copy
            df = df[[f"{self.fuel_type}"]].copy()
        else:
            data = DatabaseModel().read("aggregate", "non_supermarket")
            df = Utility.to_datetimeindex(data)
            # df = pd.read_excel('daily-updated.xlsx', index_col='Date', parse_dates=True)
            # Adapted from jezrael, Nov 12 '17 at 7:14, https://stackoverflow.com/questions/47246384/pandas-monthly-resample-15th-day
            # Adapted from https://www.oipapio.com/question-4559816
            df = df.resample(rule="MS").apply(self.first_day)
            # Adapted from johnchase, Jan 8 '16 at 17:51, https://stackoverflow.com/questions/34682828/extracting-specific-selected-columns-to-new-dataframe-as-a-copy
            df = df[[self.fuel_type, f"{self.fuel_type}-wholesale"]].copy()
        # print(df,"AggregatePriceModel extract output")
        return df

    # tested
    def get_prediction(self):
        df = self.prepare_timeseries()
        latest_price_df = df.iloc[[-1]]
        # if self.region:
        #     df.to_excel("Test_neural_network_region.xlsx")
        #     model = PredictionModel(
        #         df, self.horizon, self.region, self.fuel_type, "M", "N/A", "N/A"
        #     )
        #     forecast = model.predict()
        #     # model = NeuralNetworkEngine(5, df, self.horizon,self.region, "M")
        #     # forecast = model.prediction_engine()
        #     forecast.rename(columns={self.region: "Prediction"}, inplace=True)
        #     latest_price_df.rename(columns={self.region: "Prediction"}, inplace=True)
        if "supermarket" in self.fuel_type:
            model = PredictionModel(
                df, self.horizon, f"{self.fuel_type}", self.fuel_type, "D", "N/A", "N/A"
            )
            forecast = model.predict()
            # model = NeuralNetworkEngine(1, df, self.horizon,"Price", "D")
            # forecast = model.prediction_engine()
            # Adapted from lexual, Jul 6 '12 at 1:48, https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
            latest_price_df.rename(
                columns={f"{self.fuel_type}": "Prediction"}, inplace=True
            )
            forecast.rename(columns={"Price": "Prediction"}, inplace=True)
        else:
            model = PredictionModel(
                df,
                self.horizon,
                self.fuel_type,
                self.fuel_type,
                "M",
                "N/A",
                "N/A",
                True,
            )
            forecast = model.predict()
            #
            # model = SarimaEngine(self.fuel_type,self.horizon,df)
            # forecast = model.prediction_engine()
            # Adapted from unutbu, Jun 12 '13 at 17:44, https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
            latest_price_df = df[df.index == "2019-06-01"]
            # Adapted from lexual, Jul 6 '12 at 1:48, https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
            latest_price_df.rename(columns={self.fuel_type: "Prediction"}, inplace=True)
            forecast.rename(columns={self.fuel_type: "Prediction"}, inplace=True)
        # Adapted EdChum, Jan 25 '15 at 10:37, from https://stackoverflow.com/questions/28135436/concatenate-rows-of-two-dataframes-in-pandas
        merged_df = pd.concat([latest_price_df, forecast.iloc[[-1]]])
        print(merged_df, "AggregatePriceModel predict output")
        return merged_df
