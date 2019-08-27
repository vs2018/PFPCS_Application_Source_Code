# [1] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [2] Adapted from: https://www.oipapio.com/question-4559816
# [3] Adapted from: Author, mrbTT, Date:Oct 26 '18 at 17:31, URL:https://stackoverflow.com/questions/46217529/pandas-datetimeindex-frequency-is-none-and-cant-be-set
# [4] Adapted from: Author:johnchase, Date:Jan 8 '16 at 17:51, URL:https://stackoverflow.com/questions/34682828/extracting-specific-selected-columns-to-new-dataframe-as-a-copy
# [5] Adapted from: https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
# [6] Adapted from: Author: Matti John, Date:Jun 8 '13 at 16:20, URL:https://stackoverflow.com/questions/17001389/pandas-resample-documentation
# [7] Adapted from: Author:jezrael, Date:Nov 12 '17 at 7:14, URL:https://stackoverflow.com/questions/47246384/pandas-monthly-resample-15th-day
# [8] Adapted from: Author:jezrael, Date:Dec 23 '16 at 11:39, URL:https://stackoverflow.com/questions/41300653/pandas-resample-apply-custom-function
# [9]Adapted from: Author:lexual, Date:Jul 6 '12 at 1:48, URL:https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
# [10] Adapted from: imolit, Jul 8 '15 at 15:17, URL:https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
# [11] Source: Author:EdChum, Date:Jan 25 '15 at 10:37, URL:https://stackoverflow.com/questions/28135436/concatenate-rows-of-two-dataframes-in-pandas


import pandas as pd  # [1]

from ..infrastructure.database import DatabaseModel
from ..infrastructure.prediction_model import PredictionModel
from ..infrastructure.utility import Utility


class AveragePrice:
    def __init__(self, fuel_type, horizon, region=None):
        self.region = region
        self.fuel_type = fuel_type
        self.horizon = int(horizon)
        self.update_horizon()

    def update_horizon(self):
        if (self.region is None) and "supermarket" in self.fuel_type:
            if self.horizon == 1:
                self.horizon = 31
            elif self.horizon == 3:
                self.horizon = 91
            elif self.horizon == 6:
                self.horizon = 181
        return None

    def first_day(self, df):  # [2]
        if len(df):
            return df[0]

    def prepare_timeseries(self):
        if "supermarket" in self.fuel_type:
            data = DatabaseModel().read("aggregate", "supermarket")
            df = Utility.to_datetimeindex(data)
            df = df.resample(rule="1D").interpolate()  # [5] [6]
            df = df[[f"{self.fuel_type}"]].copy()  # [4]
        else:
            data = DatabaseModel().read("aggregate", "non_supermarket")
            df = Utility.to_datetimeindex(data)
            df = df.resample(rule="MS").apply(self.first_day)  # [2] [7] [8]
            df = df[[self.fuel_type, f"{self.fuel_type}-wholesale"]].copy()  # [4]
        return df

    # tested
    def get_prediction(self):
        df = self.prepare_timeseries()
        latest_price_df = df.iloc[[-1]]
        if "supermarket" in self.fuel_type:
            model = PredictionModel(
                df, self.horizon, f"{self.fuel_type}", self.fuel_type, "D", "N/A", "N/A"
            )
            forecast = model.predict()
            latest_price_df.rename(
                columns={f"{self.fuel_type}": "Prediction"}, inplace=True
            )  # [9]
            forecast.rename(columns={"Price": "Prediction"}, inplace=True)  # [9]
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
            latest_price_df = df[df.index == "2019-06-01"]  # [10]
            latest_price_df.rename(
                columns={self.fuel_type: "Prediction"}, inplace=True
            )  # [9]
            forecast.rename(columns={self.fuel_type: "Prediction"}, inplace=True)  # [9]
        merged_df = pd.concat([latest_price_df, forecast.iloc[[-1]]])  # [11]
        return merged_df
