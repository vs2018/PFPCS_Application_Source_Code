# [1] Requests library - get function to send HTTP request, URL: https://2.python-requests.org/en/master/
# [2] Adapted from: https://panel.ukvehicledata.co.uk/Code-Examples-Python.aspx
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
    def __init__(self, reg):
        self.registration = reg
        self.data = None
        self.save()

    # def get_data(self):
    #     return self.data
    # tested
    def get_spec(self):
        print(self.data, "get_spec vishal")
        if self.data["Response"]["StatusCode"] == "Success":
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
            # Adapted from https://www.w3schools.com/python/ref_func_round.asp
            highway = round(self.to_mpg(highway), 2)
            city = round(self.to_mpg(city), 2)
            combined = round(self.to_mpg(combined), 2)
            # print(model,fuel,tank,highway,city,combined,"Vehicle get_spec output")
            spec = {
                "model": model,
                "fuel": fuel,
                "capacity": tank,
                "highway": highway,
                "city": city,
                "combined": combined,
            }
            return spec

    # tested

    def save(self):
        try:
            # data = Utility.open_no_date(f"vehicle-{self.registration}")
            data = DatabaseModel().read("vehicle", self.registration)

        except Exception as e:
            # print(e)
            # Adapted from https://panel.ukvehicledata.co.uk/Code-Examples-Python.aspx
            result = requests.get(
                f"https://uk1.ukvehicledata.co.uk/api/datapackage/VehicleData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_VRM={self.registration}"
            )  # [2]
            data = result.json()  # [2]
            if data["Response"]["StatusCode"] == "Success":
                DatabaseModel().save(data, "vehicle", self.registration)
            # Utility.save_no_date(f"vehicle-{self.registration}",data)
        print(data["Response"]["StatusCode"], "Vehicle save output vishal")
        self.data = data
        return data

    # tested

    def get_tank_capacity(self):
        # print(self.data['Response']['DataItems']['TechnicalDetails']['Dimensions']['FuelTankCapacity'],"Vehicle get_tank_capacity output")
        return self.data["Response"]["DataItems"]["TechnicalDetails"]["Dimensions"][
            "FuelTankCapacity"
        ]

    # tested

    def get_fuel_type(self):
        # print(self.data['Response']['DataItems']['VehicleRegistration']['FuelType'],"Vehicle get_fuel_type output")
        return self.data["Response"]["DataItems"]["VehicleRegistration"]["FuelType"]

    # tested

    def to_mpg(self, mpg):
        # print(mpg / 4.54609,"Vehicle mpg output")
        return mpg / 4.54609  # [3]

    # tested

    def prepare(self, hoverData, origin, destination, fuel_type):
        # print(hoverData,origin,destination,fuel_type,"Vehicle analysis_dataframes input")
        station_post_code = hoverData["points"][0]["customdata"]
        today = Utility.get_today_date()
        station = JourneyStation(origin, fuel_type, destination)
        df = station.get_journey_data()
        # Adapted from piRSquared, Sep 11 '17 at 22:14, https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
        df_station = df[
            (df["PostCode"] == station_post_code)
            & (df["Date"] == today)
            & (df["FuelType"] == fuel_type)
        ]  # [4]
        # df_station = df[df['PostCode'] == station_post_code]
        df_directions = station.get_directions()
        df_places = station.get_places(df_directions)
        post_codes = JourneyStation.generate_station_post_codes(df_places)
        # #print(df,df_station,df_directions,station_post_code,"vishalanalysis")
        # print(df,df_station,df_directions,station_post_code,"Vehicle analysis_dataframes output")
        data = {
            "df": df,
            "df_station": df_station,
            "df_directions": df_directions,
            "station_post_code": station_post_code,
        }
        return data

    # tested

    def analysis(self, hoverData, origin, destination, tank, fuel_type):
        # print(hoverData, origin,destination,tank,fuel_type,"Vehicle analysis input")
        spec = self.get_spec()
        print(spec, "get spec in analysis vishal")
        data = self.prepare(hoverData, origin, destination, fuel_type)
        # print(route['Distance-Value'],"df route analysis")
        # #print(df_r,df,route,station,"#1")
        savings = self.prepare_savings(
            spec["capacity"], float(tank), data["df"], data["df_station"]
        )

        # #print(full,min,price,difference,loss,prediction,brand,"#2")
        savings_analysis = self.saving_analysis(
            savings["predicted_price"],
            savings["station_price"],
            savings["full_tank"],
            savings["selected_station_brand"],
            data["station_post_code"],
            fuel_type,
        )
        # #print(saving,selected_s,"#3")

        comparison = self.prepare_comparison(
            data["df_directions"],
            spec["city"],
            savings["min"],
            savings["station_price"],
            data["df"],
        )
        # #print(cheapest_l,cheapest_b,annual,"#4")

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
        # #print(difference,losses,comparison,"#5")

        distance = self.prepare_distance(
            origin,
            destination,
            data["station_post_code"],
            spec["combined"],
            savings["station_price"],
        )
        # #print(distance,duration,journey,"#6")

        distance = self.distance_analysis(
            savings["selected_station_brand"],
            data["station_post_code"],
            distance["distance"],
            distance["duration"],
            distance["journey_cost"],
        )
        # #print(distance,"#6")

        # print(distance,selected_s,difference,losses,comparison,saving,"Vehicle analysis output")
        analysis = {
            "distance": distance,
            "cost": savings_analysis["selected_s"],
            "difference": comparison_analysis["difference"],
            "loss": comparison_analysis["losses"],
            "saving": comparison_analysis["comparison"],
            "day": savings_analysis["saving"],
        }
        return analysis

    # tested

    def saving_analysis(
        self,
        predicted_price,
        station_price,
        full_tank,
        selected_station_brand,
        station_post_code,
        fuel_type,
    ):
        # print(predicted_price,station_price,full_tank,selected_station_brand,station_post_code,fuel_type,"Vehicle saving_analysis input")
        if predicted_price < station_price:
            predicted_saving = station_price - predicted_price
            predicted_saving = (predicted_saving * full_tank) / 100
            analysis_3 = f"Save £{round(predicted_saving,2)} if you fill your tank at this petrol station tomorrow as prices are predicted to fall tomorrow"
        else:
            predicted_saving = predicted_price - station_price
            predicted_saving = (predicted_saving * full_tank) / 100
            analysis_3 = f"You will lose £{round(predicted_saving,2)} if you fill your tank at this petrol station tomorrow as prices are predicted to rise tomorrow"
        selected_station = f"It will cost £{round(((station_price * full_tank)/100),2)} to fill the fuel tank with {fuel_type} at {selected_station_brand}, located at {station_post_code}"
        # print(analysis_3,selected_station,"Vehicle saving_analysis output")
        analysis = {"saving": analysis_3, "selected_s": selected_station}
        return analysis

    # tested

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
        # print(difference,min,fuel_type,cheapest_brand,cheapest_location,loss,annual_loss,selected_station_brand,"Vehicle comparison_analysis input")
        if difference > 0:
            analysis_difference = f"Price of fuel per litre is {difference} pence higher than the cheapest petrol station on your journey, {cheapest_brand} located at {cheapest_location}, where the price is {min} pence"
            analysis_loss = (
                f"You will lose £{loss} if you fill your tank at this petrol station"
            )
        else:
            analysis_difference = f"{cheapest_brand} at {cheapest_location} is the cheapest station on your journey"
            analysis_loss = f"This is the cheapest petrol station on your journey"

        analysis_4 = f"Assuming a daily commute (5 days a week), you could save up to £{annual_loss} per year if you fill at the cheapest petrol station on your journey, {cheapest_brand} located at {cheapest_location}"
        # print(analysis_difference,analysis_loss,analysis_4,"Vehicle comparison_analysis output")
        analysis = {
            "difference": analysis_difference,
            "losses": analysis_loss,
            "comparison": analysis_4,
        }
        return analysis

    # tested

    def prepare_comparison(self, df_route, city, min, station_price, df_raw):
        # print(df_route,city,min,station_price,df_raw,"Vehicle comparison_inputs inputs")
        # print(city,min,station_price,df_route,df_raw,"comparison inputs")
        journey_distance = df_route["Distance-Value"].iloc[0] / 1000
        # print(journey_distance,"journey distance")
        min_annual_cost = (((journey_distance * 260) / city) * min) / 100
        station_annual_cost = (((journey_distance * 260) / city) * station_price) / 100
        annual_loss = round((station_annual_cost - min_annual_cost), 2)
        sorted_df = df_raw.sort_values("Price")  # [5]
        cheapest_brand = sorted_df["Brand"].iloc[0]  # [6]
        cheapest_location = sorted_df["PostCode"].iloc[0]  # [6]
        # print(cheapest_location,cheapest_brand,annual_loss,"Vehicle comparison_inputs outputs")
        comparison = {
            "cheapest_location": cheapest_location,
            "cheapest_brand": cheapest_brand,
            "annual_loss": annual_loss,
        }
        return comparison

    # tested

    def round_offroutes(self, latlon, df_offroutes):
        # print(latlon,df_offroutes,"Vehicle round_offroutes inputs")
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
        # print(df_offroutes,latlon[0],latlon[1],"Vehicle round_offroutes output")

        return {"df_offroutes": df_offroutes, "lon": lon, "lat": lat}

    # def split_offroutes(self,latlon,df_offroutes):
    #     #print(latlon,df_offroutes,"Vehicle split_offroutes inputs")
    #     latlon[0] = float(str(latlon[0]).split(".")[0] + "." + str(latlon[0]).split(".")[1][:2])
    #     latlon[1] = float(str(latlon[1]).split(".")[0] + "." + str(latlon[1]).split(".")[1][:2])
    #     df_offroutes['lat_destination'] = df_offroutes['lat_destination'].apply(lambda x: float(str(x).split(".")[0] + "." + str(x).split(".")[1][:2]))
    #     df_offroutes['lat_origin'] = df_offroutes['lat_origin'].apply(lambda x: float(str(x).split(".")[0] + "." + str(x).split(".")[1][:2]))
    #     df_offroutes['lon_destination'] = df_offroutes['lon_destination'].apply(lambda x: float(str(x).split(".")[0] + "." + str(x).split(".")[1][:2]))
    #     df_offroutes['lon_origin'] = df_offroutes['lon_origin'].apply(lambda x: float(str(x).split(".")[0] + "." + str(x).split(".")[1][:2]))
    #     #print(df_offroutes,latlon[0],latlon[1],"Vehicle split_offroutes outputs")
    #     return df_offroutes,latlon[0],latlon[1]
    # tested
    def round_offroute(self, df_offroute, combined, station_price):
        # print(df_offroute,combined,station_price,"Vehicle round_offroute inputs")

        # #print(df_offroute,"vishaloffrouteinput")
        # #print(station_price,"roundoffroutestationprice")
        distance = df_offroute["route_information"].iloc[0]  # [6]
        distance_array = distance.split(" ")
        distance = round(float(distance_array[1]), 2)
        duration = round(float(distance_array[4]), 2)
        try:
            # print(combined,distance,station_price,"round off route")
            journey_cost = round(
                (
                    (((float(distance) / float(combined)) * float(station_price / 100)))
                    * 2
                ),
                2,
            )
        except ZeroDivisionError as e:
            journey_cost = 0
        # print(distance,duration,journey_cost,"Vehicle round_offroute inputs")

        return {
            "distance": distance,
            "duration": duration,
            "journey_cost": journey_cost,
        }

    # tested

    def filter_coordinates(self, df_offroutes, lon, lat):
        # print(df_offroutes,latlon_0,latlon_1,"Vehicle filter_coordinates inputs")
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
        # print(df_offroute,"Vehicle filter_coordinates outputs")
        return df_offroute

    # tested

    def prepare_distance(
        self, origin, destination, station_post_code, combined, station_price
    ):
        # print(origin,destination,station_post_code,combined,station_price,"Vehicle distance_inputs inputs")
        # df_offroutes = DatabaseModel().read("DirectionsOffRoute")
        try:
            data = DatabaseModel().read(
                "journey_stations_route", f"{origin}-{destination}"
            )
        except TypeError:
            data = DatabaseModel().read(
                "journey_route_information", f"{origin}-{destination}"
            )

        df_offroutes = Utility.to_dataframe(data)
        # #print(df_offroutes,'databasereadvishaloffroutes')
        # df_offroutes = df_offroutes[(df_offroutes['origin'] == origin) & (df_offroutes['destination'] == destination)]
        # #print(df_offroutes,'databasereadvishaloffroutesfiltered')
        latlon = Map.generate_latlon(station_post_code)
        off_routes = self.round_offroutes(latlon, df_offroutes)
        df_offroute = self.filter_coordinates(
            off_routes["df_offroutes"], off_routes["lon"], off_routes["lat"]
        )
        # #print(df_offroute,"distanceinputsvishal")
        # #print(df_offroute,"filtereddistanceinputsvishal")
        # if df_offroute.empty:
        #     df_offroutes,latlon[0],latlon[1] = self.split_offroutes(latlon,df_offroutes)
        #     df_offroute = self.filter_coordinates(df_offroutes,latlon[0],latlon[1])
        off_route = self.round_offroute(df_offroute, combined, station_price)
        # print(distance,duration,journey_cost,"Vehicle distance_inputs inputs")
        distance = {
            "distance": off_route["distance"],
            "duration": off_route["duration"],
            "journey_cost": off_route["journey_cost"],
        }
        return distance

    # tested
    def distance_analysis(
        self,
        selected_station_brand,
        station_post_code,
        distance,
        duration,
        journey_cost,
    ):
        # print(selected_station_brand,station_post_code,distance,duration,journey_cost,"Vehicle distance_analysis inputs")
        # return f"{selected_station_brand} at {station_post_code} is off route by {distance} km. It will take you {duration*2} mins to make this excursion and cost you £{journey_cost} to drive to and back from the station."
        return f"It will take you {duration} minutes to reach {selected_station_brand} at {station_post_code}, {distance} miles from the journey route, and cost you £{journey_cost} in fuel to drive back and forth"

    # tested

    def prepare_savings(self, capacity, tank, df_raw, df):
        # print(capacity,tank,df_raw,df,"Vehicle savings_inputs inputs")
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
        # print(full_tank,min,station_price,difference,loss,predicted_price,selected_station_brand,"Vehicle savings_inputs outputs")
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

    # tested
    def get_tank_data(self):
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
        # print(capacity,highway,city,combined,model,fuel,"Vehicle get_tank_data outputs")
        data = {
            "capacity": capacity,
            "highway": highway,
            "city": city,
            "combined": combined,
            "model": model,
            "fuel": fuel,
        }
        return data

    # def tank_analysis(self, tank):
    #     # print(tank,"Vehicle tank_analysis inputs")
    #     d = self.get_tank_data()
    #     tank = float(tank)
    #     # #print(tank,highway,"tank_analysis")p
    #     highway_commentary = f"Driving on the highway, your current fuel in the tank will take you {round((tank * d['highway']),1)} miles. "
    #     city_commentary = f"Driving in the city, your current fuel in the tank will take you {round((tank * d['city']),1)} miles. "
    #     combined_commentary = f"Driving in both city and highway, your current fuel in the tank will take you {round((d['combined'] * tank),1)} miles. "
    #     if (d['capacity'] - tank) > 0:
    #         fuel_analysis = f"To top up your fule tank to its full capacity, you can put in {round((d['capacity'] - tank),1)} litres of {d['fuel']}. "
    #     else:
    #         fuel_analysis = f"Your tank is currently full"
    #     # print(highway_commentary,city_commentary, combined_commentary,fuel_analysis,"Vehicle tank_analysis outputs")
    #     analysis = {
    #         "highway_commentary": highway_commentary,
    #         "city_commentary": city_commentary,
    #         "combined_commentary": combined_commentary,
    #         "fuel_analysis": fuel_analysis,
    #     }
    #     return analysis

    def tank_analysis(self, tank):
        # print(tank,"Vehicle tank_analysis inputs")
        d = self.get_tank_data()
        tank = float(tank)
        # #print(tank,highway,"tank_analysis")p
        highway_commentary = f"Current fuel level will take you {round((tank * d['highway']),1)} miles on the highway"
        city_commentary = f"Current fuel level will take you {round((tank * d['city']),1)} miles on city roads"
        combined_commentary = f"Current fuel level will take you {round((d['combined'] * tank),1)} miles on the highway and city roads"
        if (d["capacity"] - tank) > 0:
            fuel_analysis = f"Add {round((d['capacity'] - tank),1)} litres of {d['fuel']} to fill your tank to capacity"
        else:
            fuel_analysis = f"Your tank is currently full"
        # print(highway_commentary,city_commentary, combined_commentary,fuel_analysis,"Vehicle tank_analysis outputs")
        analysis = {
            "highway_commentary": highway_commentary,
            "city_commentary": city_commentary,
            "combined_commentary": combined_commentary,
            "fuel_analysis": fuel_analysis,
        }
        return analysis
