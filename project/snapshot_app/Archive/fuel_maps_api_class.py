from mapbox import Geocoder
import googlemaps
import datetime
import pandas as pd
from sqlalchemy import create_engine
from mapbox import Directions
import plotly.graph_objs as go


class DatabaseConnector:
    def __init__(self):
        self.db_path = "sqlite:///fuelapidata.db"
        self.connection = self.connect()

    def connect(self):
        return create_engine(self.db_path)


class DatabaseModel:
    def __init__(self):
        self.connection = DatabaseConnector().connection

    def save(self, df, table):
        excel = table + ".xlsx"
        df.to_excel(excel)
        if "GoogleMapsPlacesNearby" in table:
            table = "GoogleMapsPlacesNearby"
        df.to_sql(table, con=self.connection, if_exists="append", index=False)

    def read(self, table):
        return pd.read_sql(f"select * from {table}", self.connection)

    def to_dataframe(self, obj):
        return pd.DataFrame(obj)


class MapboxConnection:
    def __init__(self):
        self.key = "pk.eyJ1IjoidnMyMDE5IiwiYSI6ImNqd29ydWh5cDFkajQ0NG9sc3FwbGtyY2IifQ.H9Y11sNtzZ1bOAzgu_mnVA"
        self.geocoder = self.geocoder()
        self.directions = self.directions()

    def geocoder(self):
        # print((Geocoder(access_token=self.key),"MapboxConnection geocoder output ")
        return Geocoder(access_token=self.key)

    def directions(self):
        # print((Directions(access_token=self.key),"MapboxConnection directions output ")
        return Directions(access_token=self.key)


class GoogleMapsConnection:
    def __init__(self):
        self.key = "AIzaSyACLiEJ-WKtflBnbBAL_mAnurUbWHuVoN4"
        self.places = self.places()

    def places(self):
        # print((googlemaps.Client(key=self.key),"Google places output ")
        return googlemaps.Client(key=self.key)


class MapboxDirections:
    def __init__(self, origin, destination=None):
        self.origin = origin
        self.destination = destination
        self.geocoder_connection = MapboxConnection().geocoder
        self.directions_connection = MapboxConnection().directions
        # if destination is not None:
        #     self.data = self.call_api()
        self.routes = {
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

    def reset_directions(self):
        self.routes = {
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
        # print((self.routes,"MapboxDirections reset_directions output")

    @staticmethod
    def generate_latlon(post_code):
        # print((post_code,"MapboxDirections generate_latlon input")
        response = MapboxConnection().geocoder.forward(post_code, country=["gb"])
        # print((response.geojson()['features'][0]['center'], "MapboxDirections generate_latlon output")
        return response.geojson()["features"][0]["center"]

    def get_address(self):
        address = (
            MapboxConnection()
            .geocoder.forward(self.origin, country=["gb"])
            .geojson()["features"]
        )
        # print((address, "MapboxDirections get_address output")
        return address

    def generate_post_code(self, lng, lat):
        # print((lng, lat, "MapboxDirections generate_post_code input")
        response = self.geocoder_connection.reverse(lon=lng, lat=lat)
        # print((response.geojson()['features'], "MapboxDirections generate_post_code output")
        return response.geojson()["features"]

    def update_directions_details(self, coord, api_data):
        self.routes["Origin"].append(api_data[0]),
        self.routes["Destination"].append(api_data[1]),
        self.routes["Start-Address"].append(api_data[2]),
        self.routes["End-Address"].append(api_data[3]),
        self.routes["Distance-Text"].append(api_data[4]),
        self.routes["Distance-Value"].append(api_data[5]),
        self.routes["Duration-Text"].append(api_data[6]),
        self.routes["Duration-Value"].append(api_data[7]),
        self.routes["Lat"].append(coord[1]),
        self.routes["Lng"].append(coord[0])
        # print((self.routes,"MapboxDirections update_directions_details output")

    def call_api(self):
        latlon_origin = MapboxDirections.generate_latlon(self.origin)
        latlon_destination = MapboxDirections.generate_latlon(self.destination)
        origin_dict = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [latlon_origin[0], latlon_origin[1]],
            },
        }
        destination_dict = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [latlon_destination[0], latlon_destination[1]],
            },
        }
        response = self.directions_connection.directions(
            [origin_dict, destination_dict], "mapbox/driving-traffic"
        )
        driving_routes = response.geojson()
        return driving_routes, latlon_origin, latlon_destination

    def configure_api_data(self):
        driving_routes, latlon_origin, latlon_destination = self.call_api()
        # print((driving_routes,latlon_origin,latlon_destination,"MapboxDirections configure_api_data input")
        distance_value = driving_routes["features"][0]["properties"]["distance"]
        distance_text = driving_routes["features"][0]["properties"]["distance"] / 1000
        duration_value = driving_routes["features"][0]["properties"]["duration"]
        duration_text = driving_routes["features"][0]["properties"]["duration"] / 60
        coordinates = driving_routes["features"][0]["geometry"]["coordinates"]
        origin_address = self.generate_post_code(latlon_origin[0], latlon_origin[1])
        origin_address = origin_address[0]["place_name"]
        destination_address = self.generate_post_code(
            latlon_destination[0], latlon_destination[1]
        )
        destination_address = destination_address[0]["place_name"]
        api_data = [
            self.origin,
            self.destination,
            origin_address,
            destination_address,
            distance_text,
            distance_value,
            duration_text,
            duration_value,
            coordinates,
        ]
        # print((api_data,"MapboxDirections configure_api_data output")
        return api_data

    def save(self):
        api_data = self.configure_api_data()
        # print((api_data,"MapboxDirections save_api_data input")
        for coord in api_data[8]:
            self.update_directions_details(coord, api_data)
        db = DatabaseModel()
        df = db.to_dataframe(self.routes)
        db.save(df, "DirectionsAPI")
        self.reset_directions()
        # print((df,"MapboxDirections save_api_data output")
        return df


class GoogleMapsPlaces:
    def __init__(self, origin, destination, df):
        self.origin = origin
        self.destination = destination
        self.df = df
        self.places_connection = GoogleMapsConnection().places
        # self.data = self.call_api()
        self.places = {
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

    def reset_places(self):
        self.places = {
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
        # print((self.places,"GoogleMapsPlaces reset_places output")

    # def generate_post_code(self, lng, lat):
    #     #print((lng, lat,"GoogleMapsPlaces generate_post_code input")
    #     mapbox = MapboxDirections(self.origin, self.destination)
    #     latlon = mapbox.generate_post_code(lng, lat)
    #     #print((latlon[0]['context'][0]['text'],"GoogleMapsPlaces generate_post_code output")
    #     return latlon[0]['context'][0]['text']

    # def update_core_details(self,row,station):
    #     #print((row,station,"GoogleMapsPlaces update_core_details input")
    #     self.places['Start-Address'].append(row['Start-Address']),
    #     self.places['End-Address'].append(row['End-Address']),
    #     self.places['Distance-Text'].append(row['Distance-Text']),
    #     self.places['Distance-Value'].append(row['Distance-Value']),
    #     self.places['Duration-Text'].append(row['Duration-Text']),
    #     self.places['Duration-Value'].append(row['Duration-Value']),
    #     self.places['Origin'].append(self.origin)
    #     self.places['Destination'].append(self.destination)
    #     self.places['Route-Lat'].append(row['Lat'])
    #     self.places['Route-Lng'].append(row['Lng'])
    #     #print((self.places,"GoogleMapsPlaces update_core_details output")

    def update_station_location(self, station):
        # print((station,"GoogleMapsPlaces update_station_location input")
        result = MapboxDirections(self.origin, self.destination).generate_post_code(
            station["geometry"]["location"]["lng"],
            station["geometry"]["location"]["lat"],
        )
        print(result, "testing update_station_location during integration test")
        station_post_code = result[0]["context"][0]["text"]
        print(
            station_post_code, "testing update_station_location during integration test"
        )
        self.places["Station-PostCode"].append(station_post_code)
        print(
            self.places["Station-PostCode"],
            "GoogleMapsPlaces update_station_location output",
        )

    def update_station_details(self, station):
        # print((station,"GoogleMapsPlaces update_station_details input")
        self.places["Station"].append(station["name"])
        self.places["Station-Lat"].append(station["geometry"]["location"]["lat"])
        self.places["Station-Lng"].append(station["geometry"]["location"]["lng"])
        try:
            self.places["Open"].append(station["opening_hours"]["open_now"])
        except:
            self.places["Open"].append("N/A")
        try:
            self.places["Rating"].append(station["rating"])
        except:
            self.places["Rating"].append("N/A")
        try:
            self.places["Total-Ratings"].append(station["user_ratings_total"])
        except:
            self.places["Total-Ratings"].append("N/A")
        try:
            self.places["Amenities"].append(" ".join(station["types"]))
        except:
            self.places["Amenities"].append("N/A")
        # print((self.places,"GoogleMapsPlaces update_station_details output")

    def call_api(self, lat, lng):
        data = self.places_connection.places_nearby(
            location=[lat, lng], radius="1600", type="gas_station"
        )
        # print((data,"GoogleMapsPlaces call_api output")
        return data

    def configure_api_data(self):
        for index, row in self.df.iterrows():
            d = self.call_api(row["Lat"], row["Lng"])
            # d = self.places_connection.places_nearby(
            #     location=[row['Lat'], row['Lng']], radius="1600", type="gas_station")
            for station in d["results"]:
                self.places["Start-Address"].append(row["Start-Address"]),
                self.places["End-Address"].append(row["End-Address"]),
                self.places["Distance-Text"].append(row["Distance-Text"]),
                self.places["Distance-Value"].append(row["Distance-Value"]),
                self.places["Duration-Text"].append(row["Duration-Text"]),
                self.places["Duration-Value"].append(row["Duration-Value"]),
                self.places["Origin"].append(self.origin)
                self.places["Destination"].append(self.destination)
                self.places["Route-Lat"].append(row["Lat"])
                self.places["Route-Lng"].append(row["Lng"])
                self.update_station_location(station)
                self.update_station_details(station)
        # print((d,"GoogleMapsPlaces call_api output")
        return d
        # data = self.save_api_data(self.places)
        # return data

    def save(self):
        self.configure_api_data()
        db = DatabaseModel()
        df = db.to_dataframe(self.places)
        db.save(df, f"GoogleMapsPlacesNearby")
        self.reset_places()
        # print((df,"GoogleMapsPlaces save output")
        return df
