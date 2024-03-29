# [1] Requests library - post function to post HTTP request, URL: https://2.python-requests.org/en/master/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] Source: Author:rainer, Date:Mar 21 '13 at 21:24, URL:https://stackoverflow.com/questions/15558392/how-to-check-if-character-in-string-is-a-letter-python
# [4] Source: Author: WeNYoBen, Date:Jan 17 '18 at 2:18, URL:https://stackoverflow.com/questions/48292656/pandas-select-unique-values-from-column
# [5] Source: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-distance-matrix
# [6] Adapted from: Author:Pranzell, Date:Dec 5 '18 at 8:38, URL:https://stackoverflow.com/questions/11322430/how-to-send-post-request
# [7] Source: Author: user1907906, Date: May 12 '15 at 9:49, URL: https://stackoverflow.com/questions/30187231/using-json-dumpsstring-to-dump-a-string
# [8] Adapted from: Author:kennytm, Date:Sep 22 '10 at 5:48, URL:https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
# [9] Adapted from: Author: BrenBarn, Date:Aug 22 '12 at 3:21, URL:https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values
# [10] Adapted from: Author:jezrael, Date:Jun 11 '17 at 9:03, URL:https://stackoverflow.com/questions/44482095/dataframe-filtering-rows-by-column-values
# [11] Source: Author:n8yoder, Date:Dec 15 '15 at 19:25, URL:https://stackoverflow.com/questions/13035764/remove-rows-with-duplicate-indices-pandas-dataframe-and-timeseries
# [12] Source: Author:ely, Date:Jul 2 '12 at 2:43, URL:https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
# [13] Adapted from: Author:chrisb, Date:Nov 5 '14 at 17:50, URL:https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
# [14]: Source: Author:Michael Hoff, Date:Jul 23 '16 at 13:42, URL:https://stackoverflow.com/questions/38542419/could-pandas-use-column-as-index
# [15] Source: Author: stallingOne, Date: Apr 26 at 13:46, URL:https://stackoverflow.com/questions/21738566/how-to-set-a-variable-to-be-todays-date-in-python-pandas
# [16] Adapted from: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# [17] Source: Author: WeNYoBen, Date:Dec 26 '18 at 3:48, URL:https://stackoverflow.com/questions/53927219/pandas-concat-two-data-frames-one-with-and-one-without-headers
# [18] Adapted from: https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
# [19] Adapted from: Author: Matti John, Date:Jun 8 '13 at 16:20, URL:https://stackoverflow.com/questions/17001389/pandas-resample-documentation
# [20] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [21] Adapted from: Author: Giuseppe Salerno, Date: Jun 6 '18 at 15:31, URL: https://stackoverflow.com/questions/50724231/pandas-resample-function-issue-from-minute-to-millisecond-ersampling

import requests #[1]
import json
import pandas as pd #[2]
from prediction_model import PredictionModel
from map import Map


class Processor:
    """The Processor class creates a time series dataset for a particular petrol station, to generate predictions for Journey Saver and Nearest Station Dashboards"""
    def __init__(
        self, brand, town, county, post_code, fuel_type, price, search, master
    ):
        """Constructs a Processor object with details of a particular petrol station"""
        self.brand = brand
        self.town = town
        self.county = county
        self.post_code = post_code
        self.fuel_type = fuel_type
        self.price = price
        self.search = search
        self.master = master

    def generate_outcode(self, post_code):
        """Generates an outcode eg a postcode of EN1 1AA will have an outcode of EN1"""
        outcode = post_code.split(" ")[0]
        result = ""
        for chr in outcode:
            if chr.isalpha():  # [3]
                result += chr

        return result

    def filter_post_codes(self, df):
        """Generates a list of petrol station postcodes, from the master csv file with historical petrol station prices, with outcode of self.post_code"""
        unique_post_codes = df["PostCode"].unique().tolist()  # [4]
        outcode = self.generate_outcode(self.post_code)
        matching_post_codes = []
        for pc in unique_post_codes:
            outcode_master = self.generate_outcode(pc)

            if outcode == outcode_master:
                matching_post_codes.append(pc)
        return matching_post_codes

    def generate_coordinates(self, matching_pc_list):
        """Generates list of latitude and longitude coordinates for filtered petrol station postcodes"""
        latlon_list = []
        for idx, pc in enumerate(matching_pc_list):
            try:
                latlon = Map.generate_latlon(pc)
            except IndexError as e:
                latlon = Map.generate_latlon(matching_pc_list[idx - 1])
            lat, lon = latlon[1], latlon[0]
            latlon_list.append((lat, lon))
        latlon_obj = []
        for data in latlon_list:
            latlon_obj.append({"latitude": data[0], "longitude": data[1]})
        return latlon_obj

    def call_api(self, lat, lon, obj, matching_pc_list):  # [5]
        """Calculates distance, by calling the Distance Matrix API, between self.post_code and filtered petrol station postcodes, and sorts by nearest petrol station"""
        api_data = {
            "origins": [{"latitude": lat, "longitude": lon}],
            "destinations": obj,
            "travelMode": "driving",
        }

        headers = {"Content-Type": "application/json", "Content-Length": "450"}
        r = requests.post(
            "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=AmM7OZ0sgIaFYe-IFV1nQQ7Q-IO2Yd--qdtoTO9OTKOHOe4gS4osOrtgsWVa5lxx",
            data=json.dumps(api_data),  # [7]
            headers=headers,
        )  # [6]
        r = r.json()  # [1]
        distances = []
        for idx, data in enumerate(r["resourceSets"][0]["resources"][0]["results"]):
            distances.append(
                {"post_code": matching_pc_list[idx], "distance": data["travelDistance"]}
            )
        sorted_list = sorted(distances, key=lambda k: k["distance"])  # [8]
        sorted_post_codes = [d["post_code"] for d in sorted_list]
        return sorted_post_codes

    def find_nearest_stations(self, df):
        """Generates a sorted list of petrol stations by distance from self.post_code, the users entered postcode"""
        latlon = Map.generate_latlon(self.post_code)
        lat, lon = latlon[1], latlon[0]
        matching_pc = self.filter_post_codes(df)
        obj = self.generate_coordinates(matching_pc)
        nearest_pc_list = self.call_api(lat, lon, obj, matching_pc)
        return nearest_pc_list

    def filter_brand(self, bool):
        """Filters master csv file containing historical petrol station prices by brand type, supermarket or non-supermarket retailer"""
        unique_brands = self.master["Brand"].unique().tolist()  # [4]

        supermarkets = ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]
        brands_filter = []
        for supermarket in supermarkets:
            for self.brand in unique_brands:
                if supermarket in self.brand:
                    brands_filter.append(self.brand)
        if bool == True:
            df = self.master[self.master["Brand"].isin(brands_filter)]  # [9]
        else:
            df = self.master[~self.master["Brand"].isin(brands_filter)]  # [9]
        return df

    def determine_brand(self):
        """Determines instantiated petrol station retailer type, supermarket or non-supermarket"""
        for supermarket in ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]:
            if supermarket in self.brand:
                result = True
            else:
                result = False
        return result

    def get_station_history(self):
        """Generates a petrol station time series DataFrame with historical fuel prices"""
        dataframe_post_codes = self.master["PostCode"].unique().tolist()  # [4]

        if self.post_code not in dataframe_post_codes:
            brand = self.determine_brand()
            df = self.filter_brand(brand)

            post_code_list = self.find_nearest_stations(df)
            for p_code in post_code_list:
                post_code = p_code
                df1 = self.master[
                    (self.master["PostCode"] == p_code)
                    & (self.master["FuelType"] == self.fuel_type)
                ]  # [10]
                if len(df1) > 0:
                    break
        else:
            df1 = self.master[
                (self.master["PostCode"] == self.post_code)
                & (self.master["FuelType"] == self.fuel_type)
                & (self.master["Brand"] == self.brand)
            ]  # [10]
        df1 = df1.loc[~df1.index.duplicated(keep="first")]  # [11]
        return df1

    def transform_timeseries(self, df1):
        """Updates petrol station time series DataFrame, eg missing and duplicated data"""
        df2 = df1[["Date", "Price"]]  # [12]
        df2["Date"] = pd.to_datetime(df2["Date"])  # [13]
        df2.set_index("Date", inplace=True)  # [14]
        today = pd.Timestamp("today").strftime("%Y-%m-%d")  # [15]
        df_today = pd.DataFrame({"Date": [str(today)], "Price": self.price})  # [16]
        df_today["Date"] = pd.to_datetime(df_today["Date"])  # [13]
        df_today.set_index("Date", inplace=True)  # [14]
        df2 = pd.concat([df2, df_today])  # [17]
        df2 = df2.loc[~df2.index.duplicated(keep="first")]  # [11]
        df2 = df2.resample(rule="1D").interpolate()  # [18] [19] [21]
        return df2

    def get_predictions(self):
        """Generates petrol station time series DataFrame with historical and predicted fuel price to display on Nearest Station and Journey Saver Dashboard"""
        p_obj = {
            "1-Day Price Prediction": self.price,
            "1-Day Prediction Confidence": 99999,
            "1-Day Prediction Model": "N/A",
            "prediction": None,
            "df": None,
        }
        try:
            p_obj["df"] = self.get_station_history()
            df = self.transform_timeseries(p_obj["df"])
            model = PredictionModel(
                df, 1, "Price", self.fuel_type, "D", self.brand, self.post_code
            )
            p_obj["prediction"] = model.predict()
            p_obj["1-Day Prediction Confidence"] = p_obj["prediction"]["Error"].iloc[
                0
            ]  # [20]
            p_obj["1-Day Price Prediction"] = p_obj["prediction"]["Prediction"].iloc[
                0
            ]  # [20]
            p_obj["1-Day Prediction Model"] = p_obj["prediction"]["Model"].iloc[
                0
            ]  # [20]
            return p_obj
        except (IndexError, AttributeError) as e:

            return p_obj
