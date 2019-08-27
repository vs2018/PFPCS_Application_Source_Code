# [1] Requests library - get function to send HTTP request, URL: https://2.python-requests.org/en/master/
# [2] Source: https://panel.ukvehicledata.co.uk/Code-Examples-Python.aspx
# [3] Source: https://www.metric-conversions.org/volume/uk-gallons-to-liters.htm
# [4] Adapted from: Author:jezrael, Date:Jun 11 '17 at 9:03, URL:https://stackoverflow.com/questions/44482095/dataframe-filtering-rows-by-column-values
# [5] Source: Author: EdChum, Date:Jun 13 '16 at 10:45, URL:https://stackoverflow.com/questions/37787698/how-to-sort-pandas-dataframe-from-one-column
# [6] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [7] Source: Author:Reimar, Date:May 10 '17 at 16:15, URL:https://stackoverflow.com/questions/26133538/round-a-single-column-in-pandas
# [8] Source: Author: 陳耀融, Date:Oct 30 '17 at 0:32, URL:https://stackoverflow.com/questions/47006617/finding-max-min-value-of-individual-columns


import requests  # [1]
import json

from station_processor import Processor
from database import DatabaseModel
from station import JourneyStation
from utility import Utility
from map import Map


class Vehicle:
    """Class generates personalised fuel price insights for the Journey Saver Dashboard, given a vehicle registration number"""
    def __init__(self, reg):
        """Constructs an object with vehicle details with a user provided vehicle registration"""
        self.registration = reg
        self.data = None
        self.save()

    def get_spec(self):

        if self.data["Response"]["StatusCode"] == "Success":
            """Generates vehicle details"""
            tank = self.data["Response"]["DataItems"]["TechnicalDetails"]["Dimensions"][
                "FuelTankCapacity"
            ]
            highway = self.data["Response"]["DataItems"]["TechnicalDetails"][
                "Consumption"
            ]["ExtraUrban"]["Mpg"]
            city = self.data["Response"]["DataItems"]["TechnicalDetails"][
                "Consumption"
            ]["UrbanCold"]["Mpg"]
            combined = self.data["Response"]["DataItems"]["TechnicalDetails"][
                "Consumption"
            ]["Combined"]["Mpg"]
            model = self.data["Response"]["DataItems"]["VehicleRegistration"][
                "MakeModel"
            ]
            fuel = self.data["Response"]["DataItems"]["VehicleRegistration"]["FuelType"]
            highway = round(self.to_mpg(highway), 2)
            city = round(self.to_mpg(city), 2)
            combined = round(self.to_mpg(combined), 2)
            spec = {
                "model": model,
                "fuel": fuel,
                "capacity": tank,
                "highway": highway,
                "city": city,
                "combined": combined,
            }
            return spec


    def save(self):
        """Calls the UK Vehicle Data API to fetch vehicle details"""
        try:
            data = DatabaseModel().read("vehicle", self.registration)

        except Exception as e:
            result = requests.get(
                f"https://uk1.ukvehicledata.co.uk/api/datapackage/VehicleData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_VRM={self.registration}"
            )  # [2]
            data = result.json()  # [2]
            if data["Response"]["StatusCode"] == "Success":
                DatabaseModel().save(data, "vehicle", self.registration)
        self.data = data
        return data

    def get_tank_capacity(self):
        """Get vehicle fuel tank capacity"""
        return self.data["Response"]["DataItems"]["TechnicalDetails"]["Dimensions"][
            "FuelTankCapacity"
        ]

    def get_fuel_type(self):
        """Get vehicle fuel type"""
        return self.data["Response"]["DataItems"]["VehicleRegistration"]["FuelType"]

    def to_mpg(self, mpg):
        """Convert Miles Per Gallon to Litres"""
        return mpg / 4.54609  # [3]

    def prepare(self, hoverData, origin, destination, fuel_type):
        """Fetch routes and petrol station coordinates for personalised analysis"""
        station_post_code = hoverData["points"][0]["customdata"]
        today = Utility.get_today_date()
        station = JourneyStation(origin, fuel_type, destination)
        df = station.get_journey_data()
        df_station = df[
            (df["PostCode"] == station_post_code)
            & (df["Date"] == today)
            & (df["FuelType"] == fuel_type)
        ]  # [4]
        df_directions = station.get_directions()
        df_places = station.get_places(df_directions)
        post_codes = JourneyStation.generate_station_post_codes(df_places)
        data = {
            "df": df,
            "df_station": df_station,
            "df_directions": df_directions,
            "station_post_code": station_post_code,
        }
        return data

    def analysis(self, hoverData, origin, destination, tank, fuel_type):
        """Generates the personalised fuel price analysis for the Journey Saver Dashboard"""
        spec = self.get_spec()
        data = self.prepare(hoverData, origin, destination, fuel_type)
        savings = self.prepare_savings(
            spec["capacity"], float(tank), data["df"], data["df_station"]
        )

        savings_analysis = self.saving_analysis(
            savings["predicted_price"],
            savings["station_price"],
            savings["full_tank"],
            savings["selected_station_brand"],
            data["station_post_code"],
            fuel_type,
        )

        comparison = self.prepare_comparison(
            data["df_directions"],
            spec["city"],
            savings["min"],
            savings["station_price"],
            data["df"],
        )

        comparison_analysis = self.comparison_analysis(
            savings["difference"],
            savings["min"],
            fuel_type,
            comparison["cheapest_brand"],
            comparison["cheapest_location"],
            savings["loss"],
            comparison["annual_loss"],
            savings["selected_station_brand"],
        )

        distance = self.prepare_distance(
            origin,
            destination,
            data["station_post_code"],
            spec["combined"],
            savings["station_price"],
        )

        distance = self.distance_analysis(
            savings["selected_station_brand"],
            data["station_post_code"],
            distance["distance"],
            distance["duration"],
            distance["journey_cost"],
        )

        analysis = {
            "distance": distance,
            "cost": savings_analysis["selected_s"],
            "difference": comparison_analysis["difference"],
            "loss": comparison_analysis["losses"],
            "saving": comparison_analysis["comparison"],
            "day": savings_analysis["saving"],
        }
        return analysis

    def saving_analysis(
        self,
        predicted_price,
        station_price,
        full_tank,
        selected_station_brand,
        station_post_code,
        fuel_type,
    ):
        """Generates analysis highlighting whether to fill the tank today or tomorrow"""
        if predicted_price < station_price:
            predicted_saving = station_price - predicted_price
            predicted_saving = (predicted_saving * full_tank) / 100
            analysis_3 = f"Save £{round(predicted_saving,2)} if you fill your tank at this petrol station tomorrow as prices are predicted to fall tomorrow"
        else:
            predicted_saving = predicted_price - station_price
            predicted_saving = (predicted_saving * full_tank) / 100
            analysis_3 = f"You will lose £{round(predicted_saving,2)} if you fill your tank at this petrol station tomorrow as prices are predicted to rise tomorrow"
        selected_station = f"It will cost £{round(((station_price * full_tank)/100),2)} to fill the fuel tank with {fuel_type} at {selected_station_brand}, located at {station_post_code}"
        analysis = {"saving": analysis_3, "selected_s": selected_station}
        return analysis

    def comparison_analysis(
        self,
        difference,
        min,
        fuel_type,
        cheapest_brand,
        cheapest_location,
        loss,
        annual_loss,
        selected_station_brand,
    ):
        """Generates analysis comparing select petrol station price to cheapest petrol station found on journey, along with annual savings possible"""
        if difference > 0:
            analysis_difference = f"Price of fuel per litre is {difference} pence higher than the cheapest petrol station on your journey, {cheapest_brand} located at {cheapest_location}, where the price is {min} pence"
            analysis_loss = (
                f"You will lose £{loss} if you fill your tank at this petrol station"
            )
        else:
            analysis_difference = f"{cheapest_brand} at {cheapest_location} is the cheapest station on your journey"
            analysis_loss = f"This is the cheapest petrol station on your journey"

        analysis_4 = f"Assuming a daily commute (5 days a week), you could save up to £{annual_loss} per year if you fill at the cheapest petrol station on your journey, {cheapest_brand} located at {cheapest_location}"
        analysis = {
            "difference": analysis_difference,
            "losses": analysis_loss,
            "comparison": analysis_4,
        }
        return analysis

    def prepare_comparison(self, df_route, city, min, station_price, df_raw):
        """Prepare data for comparison_analysis method"""
        journey_distance = df_route["Distance-Value"].iloc[0] / 1000
        min_annual_cost = (((journey_distance * 260) / city) * min) / 100
        station_annual_cost = (((journey_distance * 260) / city) * station_price) / 100
        annual_loss = round((station_annual_cost - min_annual_cost), 2)
        sorted_df = df_raw.sort_values("Price")  # [5]
        cheapest_brand = sorted_df["Brand"].iloc[0]  # [6]
        cheapest_location = sorted_df["PostCode"].iloc[0]  # [6]
        comparison = {
            "cheapest_location": cheapest_location,
            "cheapest_brand": cheapest_brand,
            "annual_loss": annual_loss,
        }
        return comparison

    def round_offroutes(self, latlon, df_offroutes):
        """Round latitude and longitude coordinates to 2 decimal places to compare to persisted data which has been rounded to an accuracy of 2 decimal places"""
        lon = round(latlon[0], 2)
        lat = round(latlon[1], 2)
        decimals = 2
        df_offroutes["lat_destination"] = df_offroutes["lat_destination"].apply(
            lambda x: round(x, decimals)
        )  # [7]
        df_offroutes["lat_origin"] = df_offroutes["lat_origin"].apply(
            lambda x: round(x, decimals)
        )  # [7]
        df_offroutes["lon_destination"] = df_offroutes["lon_destination"].apply(
            lambda x: round(x, decimals)
        )  # [7]
        df_offroutes["lon_origin"] = df_offroutes["lon_origin"].apply(
            lambda x: round(x, decimals)
        )  # [7]

        return {"df_offroutes": df_offroutes, "lon": lon, "lat": lat}

    def round_offroute(self, df_offroute, combined, station_price):
        """Round distance and duration route information to 2 places"""
        distance = df_offroute["route_information"].iloc[0]  # [6]
        distance_array = distance.split(" ")
        distance = round(float(distance_array[1]), 2)
        duration = round(float(distance_array[4]), 2)
        try:
            journey_cost = round(
                (
                    (((float(distance) / float(combined)) * float(station_price / 100)))
                    * 2
                ),
                2,
            )
        except ZeroDivisionError as e:
            journey_cost = 0

        return {
            "distance": distance,
            "duration": duration,
            "journey_cost": journey_cost,
        }


    def filter_coordinates(self, df_offroutes, lon, lat):
        """Find relevant route for selected petrol station"""
        df_offroute = df_offroutes[
            (df_offroutes["lat_destination"] == lat)
            & (df_offroutes["lon_destination"] == lon)
        ]  # [4]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_origin"] == lat)
                & (df_offroutes["lon_origin"] == lon)
            ]  # [4]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_origin"] == lat)
                & (df_offroutes["lon_destination"] == lon)
            ]  # [4]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_destination"] == lat)
                & (df_offroutes["lon_origin"] == lon)
            ]  # [4]
        return df_offroute

    def prepare_distance(
        self, origin, destination, station_post_code, combined, station_price
    ):
        """Prepare data for the distance_analysis method"""
        try:
            data = DatabaseModel().read(
                "journey_stations_route", f"{origin}-{destination}"
            )
        except TypeError:
            data = DatabaseModel().read(
                "journey_route_information", f"{origin}-{destination}"
            )

        df_offroutes = Utility.to_dataframe(data)

        latlon = Map.generate_latlon(station_post_code)
        off_routes = self.round_offroutes(latlon, df_offroutes)
        df_offroute = self.filter_coordinates(
            off_routes["df_offroutes"], off_routes["lon"], off_routes["lat"]
        )

        off_route = self.round_offroute(df_offroute, combined, station_price)
        distance = {
            "distance": off_route["distance"],
            "duration": off_route["duration"],
            "journey_cost": off_route["journey_cost"],
        }
        return distance

    def distance_analysis(
        self,
        selected_station_brand,
        station_post_code,
        distance,
        duration,
        journey_cost,
    ):
        """Information on how much it will cost to drive to a selected petrol station along a journey"""
        return f"It will take you {duration} minutes to reach {selected_station_brand} at {station_post_code}, {distance} miles from the journey route, and cost you £{journey_cost} in fuel to drive back and forth"

    def prepare_savings(self, capacity, tank, df_raw, df):
        """Prepare data for savings_analysis method"""
        full_tank = capacity - tank
        min = round(df_raw["Price"].min(), 2)  # [8]
        max = df_raw["Price"].max()  # [8]
        station_price = df["Price"].iloc[0]  # [6]
        difference = round((station_price - min), 2)
        loss = round(((full_tank * difference) / 100), 2)
        if loss < 0:
            save_loss = "save"
        else:
            save_loss = "lose"
        predicted_price = df["1-Day Price Prediction"].iloc[0]  # [6]
        selected_station_brand = df["Brand"].iloc[0]  # [6]
        savings = {
            "full_tank": full_tank,
            "min": min,
            "station_price": station_price,
            "difference": difference,
            "loss": loss,
            "predicted_price": predicted_price,
            "selected_station_brand": selected_station_brand,
        }
        return savings

    def get_tank_data(self):
        """Get vehicle mileage information for mileage analysis"""
        capacity = self.data["Response"]["DataItems"]["TechnicalDetails"]["Dimensions"][
            "FuelTankCapacity"
        ]
        highway = self.data["Response"]["DataItems"]["TechnicalDetails"]["Consumption"][
            "ExtraUrban"
        ]["Mpg"]
        city = self.data["Response"]["DataItems"]["TechnicalDetails"]["Consumption"][
            "UrbanCold"
        ]["Mpg"]
        combined = self.data["Response"]["DataItems"]["TechnicalDetails"][
            "Consumption"
        ]["Combined"]["Mpg"]
        model = self.data["Response"]["DataItems"]["VehicleRegistration"]["MakeModel"]
        fuel = self.data["Response"]["DataItems"]["VehicleRegistration"]["FuelType"]
        highway = self.to_mpg(highway)
        city = self.to_mpg(city)
        combined = self.to_mpg(combined)
        data = {
            "capacity": capacity,
            "highway": highway,
            "city": city,
            "combined": combined,
            "model": model,
            "fuel": fuel,
        }
        return data

    def tank_analysis(self, tank):
        """Generate mileage analysis for vehicle using current fuel tank level specified by user"""
        d = self.get_tank_data()
        tank = float(tank)
        highway_commentary = f"Current fuel level will take you {round((tank * d['highway']),1)} miles on the highway"
        city_commentary = f"Current fuel level will take you {round((tank * d['city']),1)} miles on city roads"
        combined_commentary = f"Current fuel level will take you {round((d['combined'] * tank),1)} miles on the highway and city roads"
        if (d["capacity"] - tank) > 0:
            fuel_analysis = f"Add {round((d['capacity'] - tank),1)} litres of {d['fuel']} to fill your tank to capacity"
        else:
            fuel_analysis = f"Your tank is currently full"
        analysis = {
            "highway_commentary": highway_commentary,
            "city_commentary": city_commentary,
            "combined_commentary": combined_commentary,
            "fuel_analysis": fuel_analysis,
        }
        return analysis
