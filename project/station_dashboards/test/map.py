# [1] Mapbox Search Service Gocoding API to calculate coordinates/addresses, URL: https://docs.mapbox.com/api/search/
# [2] Google Places API to fetch petrol station coordinates, URL: https://developers.google.com/places/web-service/intro
# [3] Mapbox Navigation Service Directions API to calculate route coordinates, URL: https://docs.mapbox.com/api/navigation/#directions
# [4] Source: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/access_tokens.md
# [5] Source: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/geocoding.md
# [6] Source: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/directions.md
# [7] Source: https://github.com/googlemaps/google-maps-services-python
# [8] Source: https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/places.py
# [9] Source: Author: waitingkuo, Date: May 10 '13 at 7:07, URL:https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas


from mapbox import Geocoder
import googlemaps
from mapbox import Directions
from database import DatabaseModel
from utility import Utility
from gps import GPS


class MapboxConnection:
    def __init__(self):
        self.key = "pk.eyJ1IjoidnMyMDE5IiwiYSI6ImNqd29ydWh5cDFkajQ0NG9sc3FwbGtyY2IifQ.H9Y11sNtzZ1bOAzgu_mnVA"
        self.geocoder_client = self.geocoder_client()
        self.directions_client = self.directions_client()

    def geocoder_client(self):  # [4] [5]
        # print((Geocoder(access_token=self.key),"MapboxConnection geocoder output ")
        return Geocoder(access_token=self.key)

    def directions_client(self):  # [4] [6]
        # print((Directions(access_token=self.key),"MapboxConnection directions output ")
        return Directions(access_token=self.key)


class GooglePlacesConnection:
    def __init__(self):
        self.key = "AIzaSyACLiEJ-WKtflBnbBAL_mAnurUbWHuVoN4"
        self.client = self.client()

    def client(self):  # [7]
        # print((googlemaps.Client(key=self.key),"Google places output ")
        return googlemaps.Client(key=self.key)


class Map(GPS):
    def __init__(self, origin, destination=None):
        self.origin = origin
        self.destination = destination
        self.geocoder_connection = MapboxConnection().geocoder_client
        self.directions_connection = MapboxConnection().directions_client
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

    def reset(self):
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
        return None
        # print((self.routes,"MapboxDirections reset_directions output")

    @staticmethod
    def generate_latlon(post_code):  # [5]
        # print((post_code,"MapboxDirections generate_latlon input")
        response = MapboxConnection().geocoder_client.forward(post_code, country=["gb"])
        # print((response.geojson()['features'][0]['center'], "MapboxDirections generate_latlon output")
        return response.geojson()["features"][0]["center"]

    def generate_address(self):  # [5]
        address = (
            MapboxConnection()
            .geocoder_client.forward(self.origin, country=["gb"])
            .geojson()["features"]
        )
        # print((address, "MapboxDirections get_address output")
        return address

    def generate_post_code(self, lng, lat):  # [5]
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
        return None
        # print((self.routes,"MapboxDirections update_directions_details output")

    def call_api(self, latlon_origin, latlon_destination):  # [6]
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
        return driving_routes

    def configure_api_data(self):
        latlon_origin = Map.generate_latlon(self.origin)
        latlon_destination = Map.generate_latlon(self.destination)
        driving_routes = self.call_api(latlon_origin, latlon_destination)
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
        DatabaseModel().save(
            self.routes, "directions", f"{self.origin}-{self.destination}"
        )
        df = Utility.to_dataframe(self.routes)
        self.reset()
        # print((df,"MapboxDirections save_api_data output")
        return df


class Place(GPS):
    def __init__(self, origin, destination, df):
        self.origin = origin
        self.destination = destination
        self.df = df
        self.places_connection = GooglePlacesConnection().client
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

    def reset(self):
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
        return None
        # print((self.places,"GoogleMapsPlaces reset_places output")

    def update_station_location(self, station):
        # print((station,"GoogleMapsPlaces update_station_location input")
        self.places["Station-Lat"].append(station["geometry"]["location"]["lat"])
        self.places["Station-Lng"].append(station["geometry"]["location"]["lng"])
        result = Map(self.origin, self.destination).generate_post_code(
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
        return None

    def update_station_details(self, station):
        # print((station,"GoogleMapsPlaces update_station_details input")
        self.places["Station"].append(station["name"])
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
        return None
        # print((self.places,"GoogleMapsPlaces update_station_details output")

    def call_api(self, lat, lng):  # [8]
        data = self.places_connection.places_nearby(
            location=[lat, lng], radius="1600", type="gas_station"
        )
        # print((data,"GoogleMapsPlaces call_api output")
        return data

    def configure_api_data(self):
        for index, row in self.df.iterrows():  # [9]
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
        DatabaseModel().save(self.places, "places", f"{self.origin}-{self.destination}")
        df = Utility.to_dataframe(self.places)
        self.reset()
        # print((df,"GoogleMapsPlaces save output")
        return df
