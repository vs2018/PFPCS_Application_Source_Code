# [1] Requests library - get function to send HTTP request, URL: https://2.python-requests.org/en/master/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] PyMongo API - to catch PyMongo exceptions , URL: https://api.mongodb.com/python/current/api/pymongo/errors.html
# [4] Adapted from: Author:alishobeiri, Date:Aug '17, URL:https://community.plot.ly/t/how-to-integrate-google-maps-address-autocompletion-in-dash/5515/2
# [5] Source: https://panel.ukvehicledata.co.uk/Code-Examples-Python.aspx
# [6] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
# [7] Adapted from: Author: Andre Holzner, Date: Sep 6 '15 at 16:02, URL:https://stackoverflow.com/questions/32425334/splitting-a-string-in-a-python-dataframe
# [8] Source: Author:lexual, Date:Jul 6 '12 at 1:48, URL:https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
# [9] Source: Author:Zero, Date:Jul 27 '18 at 4:23, URL:https://stackoverflow.com/questions/31247763/round-columns-in-pandas-dataframe
# [10] Adapted from: Author:ely, Date:Jul 2 '12 at 2:43, URL:https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
# [11] Adapted from: Author:Ben, Date:Mar 12 '14 at 3:24, URL:https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column
# [12] Source: https://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.DataFrame.drop_duplicates.html
# [13] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [14] Source: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/directions.md
# [15] Source: Author:Trillionaire Sanai, Date:Mar 9 at 18:18, URL:https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
# [16] Source: Author: silvado, Date: Oct 15 '13 at 10:09, URL:https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
# [17] Adapted from: Author: unutbu, Date: Jun 12 '13 at 17:44, URL:https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
# [18] Source: Author: 陳耀融, Date:Oct 30 '17 at 0:32, URL:https://stackoverflow.com/questions/47006617/finding-max-min-value-of-individual-columns
# [19]: Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html
# [20] Adapted from: Author: jezrael, Date: Sep 5 '17 at 11:53, URL:https://stackoverflow.com/questions/46054318/tilde-sign-in-python-dataframe
# [21] Adapted from: Author: user666, Date: Oct 28 '15 at 0:58, URL: https://stackoverflow.com/questions/26244309/how-to-analyze-all-duplicate-entries-in-this-pandas-dataframe/33381151#33381151
# [22] Adapted from: Author: Michael Hoff, Date:Jul 23 '16 at 13:42, URL:https://stackoverflow.com/questions/38542419/could-pandas-use-column-as-index
# [23] Source: Author: WeNYoBen, Date:Dec 26 '18 at 3:48, URL:https://stackoverflow.com/questions/53927219/pandas-concat-two-data-frames-one-with-and-one-without-headers
# [24] Source: Author: WeNYoBen, Date:Jan 17 '18 at 2:18, URL:https://stackoverflow.com/questions/48292656/pandas-select-unique-values-from-column
# [25] Source: Author:phihag, Date:Sep 6 '12 at 22:23, URL:https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
# [26] Source: Author: Hyperboreus, Date: Oct 4 '13 at 14:52, URL: https://stackoverflow.com/questions/19184335/is-there-a-need-for-rangelena

import requests  # [1]
import pandas as pd  # [2]
import json

from station_processor import Processor
from map import Map, Directions, Place, MapboxConnection
from gui_component import UIComponent
from utility import Utility
from database import DatabaseModel
import pymongo  # [3]


class Station:
    """Class generates the fuel price table, with current and predicted prices by petrol station, for the Nearest Station and Journey Saver Dashboards"""
    def __init__(self, origin, fuel_type, destination=None):
        """Constructs a station object with fuel price results from a user query"""
        self.origin = Utility.to_uppercase(origin)
        self.destination = Utility.to_uppercase(destination)
        self.fuel_type = fuel_type
        self.data = {
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

    @staticmethod
    def address(value):  # [4]
        """Generates an address, from a user provided postcode, by calling the Mapbox Geocoding API"""
        try:
            mapbox = Map(value)
            addresses = mapbox.generate_address()
            for address in addresses:
                if address["place_type"] == ["address"]:
                    result = [
                        {
                            "label": address["place_name"],
                            "value": address["context"][0]["text"],
                        }
                    ]
                result = [{"label": address["place_name"], "value": address["text"]}]
        except KeyError:
            result = [{"label": "", "value": ""}]
        return result

    def call_api(self, post_code=None):
        """Fetches fuel prices from the UK Vehicle Data - Fuel Price API"""
        date = Utility.get_today_date()
        if post_code == None:
            try:
                data = DatabaseModel().read("fuel_price_api", f"{date}-{self.origin}")
            except Exception as e:
                result = requests.get(
                    f"https://uk1.ukvehicledata.co.uk/api/datapackage/FuelPriceData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_postcode={self.origin}"
                )  # [5]
                data = result.json()  # [5]
                with open(f"{self.origin}.json", "w", encoding="utf-8") as outfile: #[25]
                    json.dump(data, outfile, ensure_ascii=False, indent=2) #[25]
                DatabaseModel().save(data, "fuel_price_api", f"{date}-{self.origin}")
        else:
            try:
                data = DatabaseModel().read("fuel_price_api", f"{date}-{self.origin}")
            except Exception as e:
                result = requests.get(
                    f"https://uk1.ukvehicledata.co.uk/api/datapackage/FuelPriceData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_postcode={post_code}"
                )  # [5]
                data = result.json()  # [5]
                with open(f"{post_code}.json", "w", encoding="utf-8") as outfile: #[25]
                    json.dump(data, outfile, ensure_ascii=False, indent=2) #[25]
                DatabaseModel().save(data, "fuel_price_api", f"{date}-{self.origin}")
        return data

    def update_table(self, df):
        """Updates the fuel price DataFrame for the UIComponent class to create a Dash DataTable user interface componentd"""
        df.to_excel("Test_Station_get_data_df.xlsx")  # [6]
        df = Utility.drop_duplicate(df, ["PostCode"])
        df["TimeRecorded"] = df["TimeRecorded"].str.split().str[0]  # [7]
        df.rename(
            {
                "PostCode": "Post Code",
                "DistanceFromSearchPostcode": "Distance",
                "1-Day Price Prediction": "Prediction",
                "TimeRecorded": "DateRecorded",
                "1-Day Prediction Confidence": "Error",
            },
            axis=1,
            inplace=True,
        )  # [8]
        cols = ["Distance", "Price", "Prediction", "Error"]
        df[cols] = df[cols].round(2)  # [9]
        df1 = df[["Brand", "Post Code", "Price", "Prediction", "DateRecorded"]]  # [10]
        return {"df": df, "df1": df1}

    def update(self, latlon, date, data, d, prediction, p):
        """Updates the station object with petrol station fuel price attributes"""
        self.data["Lat"].append(latlon[1])
        self.data["Lon"].append(latlon[0])
        self.data["Date"].append(date)
        self.data["SearchPostCode"].append(data["Request"]["DataKeys"]["Postcode"])
        self.data["DistanceFromSearchPostcode"].append(d["DistanceFromSearchPostcode"])
        self.data["Brand"].append(d["Brand"])
        self.data["Name"].append(d["Name"])
        self.data["Street"].append(d["Street"])
        self.data["Town"].append(d["Town"])
        self.data["County"].append(d["County"])
        self.data["PostCode"].append(d["Postcode"])
        self.data["FuelType"].append(p["FuelType"])
        self.data["1-Day Price Prediction"].append(prediction["1-Day Price Prediction"])
        self.data["1-Day Prediction Confidence"].append(
            prediction["1-Day Prediction Confidence"]
        )
        self.data["1-Day Prediction Model"].append(prediction["1-Day Prediction Model"])
        self.data["Price"].append(p["LatestRecordedPrice"]["InPence"])
        self.data["TimeRecorded"].append(p["LatestRecordedPrice"]["TimeRecorded"])
        return None

    def reset(self):
        """Resets station object for a new petrol station fuel price attributes"""
        self.data = {
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
        return None

    def get_route_data(self, destination):
        """Fetches petrol station routes from application persistence layer"""
        today = Utility.get_today_date()
        data = DatabaseModel().read("directions", f"{self.origin}-{destination}")
        df = Utility.to_dataframe(data)
        return df

    def call_processor(self, data, date):
        """Calls Processor class to generate a DataFrame with historical and predicted fuel prices for all petrol stations found"""
        for d in data["Response"]["DataItems"]["FuelStationDetails"]["FuelStationList"]:
            for p in d["FuelPriceList"]:
                if p["FuelType"] == self.fuel_type:
                    try:
                        latlon = Map.generate_latlon(d["Postcode"])
                    except IndexError:
                        latlon = Map.generate_latlon(
                            data["Request"]["DataKeys"]["Postcode"]
                        )
                    try:
                        db = DatabaseModel()
                        master = db.get_master()
                        processor = Processor(
                            d["Brand"],
                            d["Town"],
                            d["County"],
                            d["Postcode"],
                            self.fuel_type,
                            p["LatestRecordedPrice"]["InPence"],
                            data["Request"]["DataKeys"]["Postcode"],
                            master,
                        )
                        prediction = processor.get_predictions()
                        self.update(latlon, date, data, d, prediction, p)
                    except (UnboundLocalError, AttributeError) as e:
                        continue
        return None


class JourneyStation(Station):
    """Inherits from the parent Station class and is responsible for generating the Journey Saver Dashboard map"""
    def __init__(self, origin, fuel_type, destination):
        """Constructor to generate an object with fuel price and map data for the Journey Saver Dashboard"""
        super().__init__(origin, fuel_type, destination)
        self.route_data = {
            "origin": [],
            "destination": [],
            "lat_origin": [],
            "lat_destination": [],
            "lon_origin": [],
            "lon_destination": [],
            "route_information": [],
            "closest_coordinate": [],
            "k": [],
        }

    @staticmethod
    def generate_station_post_codes(df):
        """Generate list of postcodes that fall on the user provided journey route"""
        df.to_excel("Test_Station_get_unique_stations_df.xlsx")  # [6]
        unique_postcodes = (
            df["Station-PostCode"].drop_duplicates().values.tolist()
        )  # [11] [12]
        outcodes = []
        for unique_postcode in unique_postcodes:
            outcodes.append(unique_postcode.split(" ")[0])
        outcodes = list(set(outcodes))
        postcodes = []
        for outcode in outcodes:
            for postcode in unique_postcodes:
                if outcode in postcode:
                    postcodes.append(postcode)
                    break
        return postcodes

    def reset_route(self):
        """Reset JourneyStation object to save a new petrol station route"""
        self.route_data = {
            "origin": [],
            "destination": [],
            "lat_origin": [],
            "lat_destination": [],
            "lon_origin": [],
            "lon_destination": [],
            "route_information": [],
            "closest_coordinate": [],
            "k": [],
        }
        return None

    def update_route(self, closest_coordinate, route_information, k):
        """Update JourneyStation object with a new petrol station route"""
        self.route_data["origin"].append(self.origin)
        self.route_data["destination"].append(self.destination)
        self.route_data["lat_origin"].append(closest_coordinate[k][1])
        self.route_data["lat_destination"].append(closest_coordinate[k + 1][1])
        self.route_data["lon_origin"].append(closest_coordinate[k][0])
        self.route_data["lon_destination"].append(closest_coordinate[k + 1][0])
        self.route_data["route_information"].append(route_information)
        self.route_data["closest_coordinate"].append(closest_coordinate)
        self.route_data["k"].append(k)

        return None

    def generate_directions(self, df, df_route, i):  # [14]
        """Generate routes, using Mapbox Directions API, to each petrol station falling along the journey"""
        df.to_excel("Test_Journey_get_offroute_data_df.xlsx")  # [6]
        df_route.to_excel("Test_Journey_get_offroute_data_df_route.xlsx")  # [6]
        station_lat, station_lon = df["Lat"].iloc[i], df["Lon"].iloc[i]  # [13]
        distances, route_responses = [], []
        for j in range(len(df_route)):
            origin_dict = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [station_lon, station_lat],
                },
            }
            destination_dict = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [df_route["Lng"].iloc[j], df_route["Lat"].iloc[j]],
                },
            }
            try:
                response = MapboxConnection().directions_client.directions(
                    [origin_dict, destination_dict], "mapbox/driving-traffic"
                )  # [14]
                driving_route = response.geojson() # [14]
                route_responses.append(driving_route)
                distance_value = driving_route["features"][0]["properties"]["distance"]
                distances.append([distance_value, j])
            except KeyError as e:
                continue
        return {"distances": distances, "route_responses": route_responses}

    def generate_route_information(self, df, df_route):
        """Generate route information: distance and duration"""
        df.to_excel("Test_Journey_save_station_routes_df.xlsx")  # [6]
        df_route.to_excel("Test_Journey_save_station_routes_df_route.xlsx")  # [6]
        off_routes = []
        off_routes_data = []
        for i in range(len(df)): #[26]
            try:
                data = self.generate_directions(df, df_route, i)
                distances, route_responses = data["distances"], data["route_responses"]
                distances.sort(key=lambda x: x[0])  # [15]
                closest_coordinate_response = route_responses[distances[0][1]]
            except IndexError:
                continue
            distance_info = (
                closest_coordinate_response["features"][0]["properties"]["distance"]
                / 1000
            )
            duration_info = (
                closest_coordinate_response["features"][0]["properties"]["duration"]
                / 60
            )
            closest_coordinate = closest_coordinate_response["features"][0]["geometry"][
                "coordinates"
            ]
            route_information = (
                "Distance: "
                + str(int(distance_info))
                + " mi, Duration: "
                + str(int(duration_info))
                + " mins"
            )
            data = []
            for k in range(len(closest_coordinate) - 1): #[26]
                data.append(
                    {
                        "closest_coordinate": closest_coordinate,
                        "route_information": route_information,
                        "k": k,
                    }
                )
                off_routes.append(
                    UIComponent().render_off_route(
                        closest_coordinate, route_information, k
                    )
                )
                self.update_route(closest_coordinate, route_information, k)
            off_routes_data.append(data)

        DatabaseModel().save(
            self.route_data,
            "journey_route_information",
            f"{self.origin}-{self.destination}",
        )

        self.reset_route()
        return off_routes

    # tested

    def get_route_information(self, df):
        """Fetch petrol station from application persistence layer"""
        data = DatabaseModel().read(
            "journey_route_information", f"{self.origin}-{self.destination}"
        )

        off_routes = []
        for i in range(len(data["closest_coordinate"])): #[26]

            off_routes.append(
                UIComponent().render_off_route(
                    data["closest_coordinate"][i],
                    data["route_information"][i],
                    data["k"][i],
                )
            )

        return off_routes

    # tested

    def generate_routes(self, df_route, df):
        """Generate user interface routes on a map using UIComponent class"""
        df.to_excel("Test_Journey_map_routes_df.xlsx")  # [6]
        df_route.to_excel("Test_Journey_map_routes_df_route.xlsx")  # [6]
        routes = []
        route_information = (
            "Distance: "
            + str(int(df_route["Distance-Text"].iloc[0]))  # [13]
            + " mi, Duration: "
            + str(int(df_route["Duration-Text"].iloc[0]))  # [13]
            + " mins"
        )
        for i in range(len(df_route) - 1): #[26]
            routes.append(
                UIComponent().render_journey_route(df_route, route_information, i)
            )
        return routes

    def generate_map_data(self, df):
        """Generate a map with the journey route, and routes to each petrol station, from user inputs"""
        df.to_excel("Test_Journey_map_df.xlsx")  # [6]
        stations_list = super().get_route_data(self.destination)

        routes = self.generate_routes(stations_list, df)
        off_routes = self.generate_route_information(df, stations_list)

        df["Information"] = (
            df["Brand"]
            + ", "
            + df["FuelType"]
            + ": "
            + df["Price"].map(str)  # [16]
            + "p, "
            + df["Post Code"]
        )
        latlon_origin = Map.generate_latlon(self.origin)
        latlon_destination = Map.generate_latlon(self.destination)
        stations = UIComponent().render_stations(df)
        origin_coordinate = UIComponent().render_origin(
            latlon_origin[1],
            latlon_origin[0],
            stations_list["Start-Address"].iloc[0],  # [13]
        )
        destination_coordinate = UIComponent().render_origin(
            latlon_destination[1],
            latlon_destination[0],
            stations_list["End-Address"].iloc[0],  # [13]
        )

        data = {
            "stations_list": stations_list,
            "origin_coordinate": origin_coordinate,
            "destination_coordinate": destination_coordinate,
            "routes": routes,
            "off_routes": off_routes,
            "stations": stations,
        }
        return data

    def call_api(self, post_codes):
        """Call parent class to fetch fuel prices for petrol stations along a journey"""
        batch_data = []
        for post_code in post_codes:
            data = super().call_api(post_code)

            try:
                data["Response"]["DataItems"]["FuelStationDetails"]["FuelStationList"][
                    0
                ]
                batch_data.append(data)
            except KeyError as e:
                pass
        return batch_data

    def get_directions(self):
        """Generate a DataFrame with route coordinates using the Mapbox Directions API"""
        try:
            data = DatabaseModel().read(
                "directions", f"{self.origin}-{self.destination}"
            )
            df = Utility.to_dataframe(data)
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [3]
            mapbox = Map(self.origin, self.destination)
            df = mapbox.save()
        return df

    def get_places(self, df_directions):
        """Generate a DataFrame, using Google Places API, with petrol station coordinates found along a journey"""
        try:
            data = DatabaseModel().read("places", f"{self.origin}-{self.destination}")
            df = Utility.to_dataframe(data)
        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [3]
            places = Place(self.origin, self.destination, df_directions)
            df = places.save()
        return df

    def get_journey_data(self):
        """Generate fuel prices and map data for the Journey Saver Dashboard"""
        df_directions = self.get_directions()
        df_places = self.get_places(df_directions)
        post_codes = JourneyStation.generate_station_post_codes(df_places)
        today = Utility.get_today_date()
        try:
            today = Utility.get_today_date()
            data = DatabaseModel().read(
                "journey_fuel_prices",
                f"{today}-{self.origin}-{self.fuel_type}-{self.destination}",
            )
            df = Utility.to_dataframe(data)

        except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [3]
            df = self.save(post_codes)
        return df

    def save(self, post_codes):
        """Call parent class to generate DataFrame with historical and predicted fuel prices"""
        post_codes = self.remove_invalid_post_code(post_codes)
        batch_data = self.call_api(post_codes)
        date = Utility.get_today_date()
        for data in batch_data:
            super().call_processor(data, date)
        df = Utility.to_dataframe(self.data)
        if len(df) > 0:
            DatabaseModel().save(
                self.data,
                "journey_fuel_prices",
                f"{date}-{self.origin}-{self.fuel_type}-{self.destination}",
            )

        super().reset()
        return df

    def remove_invalid_post_code(self, post_codes):
        """Filter petrol station postcodes without an 'A' due to Fuel Price API restriction"""
        for post_code in post_codes:
            if "A" not in post_code:
                post_codes.remove(post_code)
        return post_codes


class NearestStation(Station):
    """Inherits from the parent Station Class and is responsible for generating the data for the Nearest Station Dashboard"""
    def __init__(self, post_code, fuel_type):
        """Constructs an object with user inputs for the Nearest Station Dashboard"""
        super().__init__(post_code, fuel_type)

    def get_station_data(self, station):
        """Fetch fuel prices from the applications persistence layer"""
        today = Utility.get_today_date()
        data = DatabaseModel().read(
            "station_fuel_prices", f"{today}-{self.origin}-{self.fuel_type}"
        )
        df = Utility.to_dataframe(data)

        return df[(df["PostCode"] == station)]  # [17]

    def generate_brand_analysis(self, data):
        """Calculates proportion of supermarkets vs other fuel retailers found in a user query, for a pie chart"""
        df = Utility.to_dataframe(data)
        df = Utility.drop_duplicate(df, ["Post Code"])
        total = len(df)
        supermarket = 0
        non_supermarket = 0
        for i in range(len(df)): #[26]
            for station in ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]:
                if station in df["Brand"].iloc[i]:  # [13]
                    supermarket += 1
        non_supermarket = total - supermarket

        return {"supermarket": supermarket, "non_supermarket": non_supermarket}

    def generate_metrics(self, data, slider, radio):
        """Generates data for the petrol station analysis bar chart"""
        df = Utility.to_dataframe(data)
        df = df[df["Distance"] <= slider]  # [17]
        price_min, price_max = df["Price"].min(), df["Price"].max()  # [18]
        prediction_min, prediction_max = (
            df["Prediction"].min(),
            df["Prediction"].max(),
        )  # [18]
        if prediction_max > price_max:
            max = prediction_max
        else:
            max = price_max
        if prediction_min < price_min:
            min = prediction_min
        else:
            min = price_min
        if (radio == "Brand") or (radio == "Post Code"):
            df = Utility.sort_columns(df, ["Price", "Prediction"])
        else:
            df = Utility.sort_columns(df, ["Distance", "Price", "Prediction"])
        df = df.loc[~df[radio].duplicated(keep="first")]  # [17] [19] [20] [21]
        return {"df": df, "min": min, "max": max}

    def generate_search_analysis(self, rows):
        """Generates data highlighting fuel price statistics from a particular user query"""
        df = Utility.to_dataframe(rows)
        brand_today = df[df["Price"] == df["Price"].min()]["Brand"].iloc[
            0
        ]  # [13] [17] [18]
        postcode_today = df[df["Price"] == df["Price"].min()]["Post Code"].iloc[
            0
        ]  # [13] [17] [18]
        distance_today = df[df["Price"] == df["Price"].min()]["Distance"].iloc[
            0
        ]  # [13] [17] [18]
        brand_tomorrow = df[df["Prediction"] == df["Prediction"].min()]["Brand"].iloc[
            0
        ]  # [13] [17] [18]
        postcode_tomorrow = df[df["Prediction"] == df["Prediction"].min()][
            "Post Code"
        ].iloc[
            0
        ]  # [13] [17] [18]
        distance_tomorrow = df[df["Prediction"] == df["Prediction"].min()][
            "Distance"
        ].iloc[
            0
        ]  # [13] [17] [18]
        analysis = {
            "brand_today": brand_today,
            "postcode_today": postcode_today,
            "distance_today": distance_today,
            "brand_tomorrow": brand_tomorrow,
            "postcode_tomorrow": postcode_tomorrow,
            "distance_tomorrow": distance_tomorrow,
        }
        return analysis

    def generate_station_timeseries(self, hoverData, rows):
        """Generates a time series for a user selected petrol station, showing historical and predicted fuel prices"""
        df_rows = Utility.to_dataframe(rows)

        try:
            if hoverData["points"][0]["customdata"] != "":
                station_post_code = hoverData["points"][0]["customdata"]
            else:
                station_post_code = df_rows["Post Code"].iloc[0]  # [13]
        except (KeyError, TypeError):
            station_post_code = df_rows["Post Code"].iloc[0]  # [13]

        df = self.get_station_data(station_post_code)
        brand = df.iloc[0]["Brand"]  # [13]
        station_post_code = df.iloc[0]["PostCode"]  # [13]
        if df["1-Day Prediction Confidence"].iloc[0] > 200:  # [13]
            hoverData = {"points": [{"customdata": ""}]}
            df = self.get_station_data(df_rows["Post Code"].iloc[0])  # [13]

        db = DatabaseModel()
        master = db.get_master()
        prediction = Processor(
            df.iloc[0]["Brand"],
            df.iloc[0]["Town"],
            df.iloc[0]["County"],
            df.iloc[0]["PostCode"],
            df.iloc[0]["FuelType"],
            df.iloc[0]["Price"],
            df.iloc[0]["SearchPostCode"],
            master,
        )  # [13]
        prediction = prediction.get_predictions()
        df1, predicted_df = prediction["df"], prediction["prediction"]
        df1.set_index("Date", inplace=True)  # [22]
        df1.rename(columns={"Price": "Prediction"}, inplace=True)  # [8]
        df = pd.concat([df1, predicted_df])  # [23]
        data = {"df": df, "brand": brand, "station_post_code": station_post_code}
        return data

    def generate_routes(self, stations_list):
        """Generates routes, along with distance and duration information, between user entered postcode and petrol stations found in the query"""
        routes = []
        for idx, station in enumerate(stations_list):
            try:
                df_route = super().get_route_data(station)
            except (TypeError, pymongo.errors.ServerSelectionTimeoutError) as e:  # [3]
                try:
                    mapbox = Map(self.origin, station)
                    df_route = mapbox.save()
                except IndexError as e:
                    mapbox = Map(self.origin, stations_list[idx - 1])
                    df_route = mapbox.save()
            route_information = (
                "Distance: "
                + str(int(df_route["Distance-Text"].iloc[0]))  # [13]
                + " mi, Duration: "
                + str(int(df_route["Duration-Text"].iloc[0]))  # [13]
                + " mins"
            )
            for i in range(len(df_route) - 1): #[26]
                routes.append(
                    UIComponent().render_routes(df_route, route_information, i)
                )

        return {"routes": routes, "df_route": df_route}

    # tested
    def generate_map_data(self, df):
        """Generates data to render a map on the Nearest Station dashboard"""
        df.to_excel("Test_NearestPump_map_input.xlsx")  # [6]
        stations_list = (
            df[df["SearchPostCode"] == self.origin]["Post Code"].unique().tolist()
        )  # [17] [24]
        data = self.generate_routes(stations_list)
        routes, df_route = data["routes"], data["df_route"]
        latlon = Map.generate_latlon(self.origin)
        search_lat = latlon[1]
        search_lon = latlon[0]
        df["Information"] = (
            df["Brand"]
            + ", "
            + df["FuelType"]
            + ": "
            + df["Price"].map(str)  # [16]
            + "p, "
            + df["Post Code"]
        )
        stations = UIComponent().render_stations(df)
        origin_coordinate = UIComponent().render_origin(
            search_lat, search_lon, self.origin
        )

        data = {
            "df_route": df_route,
            "origin_coordinate": origin_coordinate,
            "stations": stations,
            "routes": routes,
        }
        return data

    def get_stations(self):
        """Fetches fuel prices from the applications persistence layer"""
        try:
            today = Utility.get_today_date()
            data = DatabaseModel().read(
                "station_fuel_prices", f"{today}-{self.origin}-{self.fuel_type}"
            )
            df = Utility.to_dataframe(data)
        except (pymongo.errors.ServerSelectionTimeoutError, TypeError) as e:  # [3]
            df = self.save()
        return df

    def save(self):
        """Generates a DataFrame with historical and predicted fuel prices for a particular user query"""
        data = super().call_api()
        date = Utility.get_today_date()
        super().call_processor(data, date)
        df = Utility.to_dataframe(self.data)
        if len(df) > 0:
            DatabaseModel().save(
                self.data,
                "station_fuel_prices",
                f"{date}-{self.origin}-{self.fuel_type}",
            )
        super().reset()
        return df
