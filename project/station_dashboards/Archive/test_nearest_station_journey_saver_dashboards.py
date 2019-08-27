# [1] Pytest library is used to write the unit and integration tests using @pytest.fixture and the in built python assert statement, URL: https://docs.pytest.org/en/latest/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
# [4] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe


import pytest  # [1]
from .gps import GPS
from .map import MapboxConnection, GooglePlacesConnection, Map, Place
from .station_processor import Processor
from .station import Station, JourneyStation, NearestStation
from .vehicle import Vehicle
from ..infrastructure.utility import Utility
import pandas as pd  # [2]
from app1_fixtures import *
from index_fixtures import *
from station_apps_fixtures import (
    render_map_card2_input,
    render_journey_result_input,
    render_journey_analysis_input,
)
from ..infrastructure.database import DatabaseModel
from .map import Map, Directions, Place, MapboxConnection


class TestJourneyStation(object):
    @pytest.fixture
    def journey(self):
        return JourneyStation("BA11 5LB", "Unleaded", "BA11 5AP")

    def test_generate_map_data(self, journey):  # couldnt find DirectionsAPI table
        df = pd.read_excel("Test_Journey_map_df.xlsx")  # [3]
        data = journey.generate_map_data(df)
        print(data)
        assert (
            data["stations_list"]["Start-Address"].iloc[0]
            == "81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom"
        )  # [4]

    def test_get_directions(self, journey):
        df = journey.get_directions()
        print(df)
        assert isinstance(df["Duration-Value"].iloc[0], float)  # [4]

    def test_get_places(self, journey):
        df = journey.get_directions()
        df = journey.get_places(df)
        print(df)
        assert "gas_station" in df["Amenities"].iloc[0]  # [4]

    def test_generate_station_post_codes(self, journey):
        df = journey.get_directions()
        df = journey.get_places(df)
        stations = JourneyStation.generate_station_post_codes(df)
        print(stations)
        assert stations == ["BA11 5LA"]

    def test_get_journey_data(self, journey):
        df = journey.get_journey_data()
        print(df)
        assert df["DistanceFromSearchPostcode"].iloc[0] == 0.07  # [4]

    def test_reset_route(self, journey):
        journey.reset_route()
        output = {
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
        print(journey.route_data)
        assert journey.route_data == output

    def test_update_route(self, journey):
        journey.update_route(
            [
                (-2.30425, 51.22757),
                (-2.30395, 51.22741),
                (-2.30377, 51.22726),
                (-2.30348, 51.22714),
            ],
            "Distance: 0 km, Duration: 0 mins",
            0,
        )
        output = {
            "origin": ["BA11 5LB"],
            "destination": ["BA11 5AP"],
            "lat_origin": [51.22757],
            "lat_destination": [51.22741],
            "lon_origin": [-2.30425],
            "lon_destination": [-2.30395],
            "route_information": ["Distance: 0 km, Duration: 0 mins"],
        }
        print(journey.route_data["lat_origin"])
        assert journey.route_data["lat_origin"] == [51.22757]

    def test_save(self, journey):
        df = journey.save(["BA11 5LA"])
        print(df)
        assert df["Brand"].iloc[-1] == "BP"  # [4]

    def test_remove_invalid_post_code(self, journey):
        post_codes = journey.remove_invalid_post_code(["BA11 5LA"])
        print(post_codes)
        assert post_codes == ["BA11 5LA"]

    def test_call_api(self, journey):
        batch_data = journey.call_api(["BA11 5LA"])
        print(batch_data)
        assert (
            batch_data[0]["Response"]["DataItems"]["FuelStationDetails"][
                "FuelStationCount"
            ]
            == 7
        )

    def test_generate_route_information(self, journey):
        df = pd.read_excel("Test_Journey_map_routes_df.xlsx")  # [3]
        df_route = pd.read_excel("Test_Journey_map_routes_df_route.xlsx")  # [3]
        off_routes = journey.generate_route_information(df, df_route)
        print(off_routes)
        assert len(off_routes) > 0

    def test_get_route_information(self, journey):
        df = pd.read_excel("Test_Journey_map_df.xlsx")  # [3]
        off_routes = journey.get_route_information(df)
        print(off_routes)
        assert len(off_routes) == 109

    def test_generate_directions(self, journey):
        df = pd.read_excel("Test_Journey_get_offroute_data_df.xlsx")  # [3]
        df_route = pd.read_excel("Test_Journey_get_offroute_data_df_route.xlsx")  # [3]
        data = journey.generate_directions(df, df_route, 1)
        print(data)
        assert len(data["distances"]) > 1

    def test_generate_routes(self, journey):
        df = pd.read_excel("Test_Journey_map_routes_df.xlsx")  # [3]
        df_route = pd.read_excel("Test_Journey_map_routes_df_route.xlsx")  # [3]
        routes = journey.generate_routes(df_route, df)
        print(routes)
        assert len(routes) > 0


class TestProcessor(object):
    #     #tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def processor(self):
        db = DatabaseModel()
        master = db.get_master()
        return Processor(
            "SHELL",
            "FROME",
            "SOMERSET",
            "BA11 2RY",
            "Unleaded",
            126.9,
            "BA11 5LA",
            master,
        )

    def test_generate_outcode(self, processor):
        outcode = processor.generate_outcode(processor.post_code)
        print(outcode)
        assert outcode == "BA"

    def test_filter_post_codes(self, processor):
        df = processor.filter_brand(False)
        matches = processor.filter_post_codes(df)
        print(matches)
        assert matches == ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]

    def test_filter_brand(self, processor):
        df = processor.filter_brand(False)
        print(df)
        assert len(df) == 27910

    def test_determine_brand(self, processor):
        result = processor.determine_brand()
        print(result)
        assert result == False

    def test_find_nearest_stations(self, processor):
        df = processor.filter_brand(False)
        post_codes = processor.find_nearest_stations(df)
        print(post_codes)
        assert post_codes == ["BA2 7HY", "BA2 5RU", "BA1 6AJ", "BA2 3BA"]

    def test_generate_coordinates(self, processor):
        obj = processor.generate_coordinates(
            ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]
        )
        print(obj)
        assert obj[0]["latitude"] == 51.3778523492681

    def test_call_api(self, processor):
        pc = ["BA2 3BA", "BA1 6AJ", "BA2 5RU", "BA2 7HY"]
        obj = processor.generate_coordinates(pc)
        sorted_pc = processor.call_api(51.2429256459164, -2.29176511193396, obj, pc)
        print(sorted_pc)
        assert sorted_pc[0] == "BA2 7HY"

    def test_get_station_history(self, processor):
        df = processor.get_station_history()
        print(df)
        assert df["DistanceFromSearchPostcode"].iloc[0] == 2.23  # [4]

    def test_transform_timeseries(self, processor):
        df = processor.get_station_history()
        df = processor.transform_timeseries(df)
        print(df)
        # assert len(df == 20)
        assert len(df) == 20

    def test_get_predictions(self, processor):
        result = processor.get_predictions()
        print(result)
        # assert len(result['df'] == 21)
        assert len(result["df"]) == 21


class TestPlace(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def place(self):
        df = Map("BA11 5AP", "BA11 5LB").save()
        return Place("BA11 5AP", "BA11 5LB", df)

    def test_reset(self, place):
        place.reset()
        print(place.places)
        assert place.places == {
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

    def test_update_station_location(self, place):
        place.update_station_location(station)
        print(place.places["Station-PostCode"])
        assert place.places["Station-PostCode"] == ["BA11 5LA"]

    def test_update_station_details(self, place):
        place.update_station_details(station)
        print(place.places["Amenities"][0])
        assert "gas_station" in place.places["Amenities"][0]

    def test_call_api(self, place):
        response = place.call_api(51.22032, -2.31717)
        print(response)
        assert response["status"] == "OK"

    def test_configure_api_data(self, place):
        place.configure_api_data()
        print(place.places["Distance-Value"])
        assert 5614.4 in place.places["Distance-Value"]

    def test_save(self, place):
        df = place.save()
        print(df)
        assert len(df) == 72


class TestMap(object):
    # tested on origin = BA11 5AP / destination = BA11 5LB on 21 July 2019 price data
    @pytest.fixture
    def map(self):
        return Map("BA11 5AP", "BA11 5LB")

    @pytest.fixture
    def data(self):
        mapbox = Map("BA11 5AP", "BA11 5LB")
        return mapbox.configure_api_data()

    def test_reset(self, map):
        map.reset()
        print(map.routes)
        assert map.routes == {
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

    def test_generate_latlon(self, map):
        response = Map.generate_latlon("BA11 5LA")
        print(response)
        assert response == [-2.30448401366007, 51.2273911883167]

    def test_generate_address(self, map):
        address = map.generate_address()
        print(address)
        assert (
            address[0]["place_name"]
            == "BA11 5AP, Frome, Somerset, England, United Kingdom"
        )

    def test_generate_post_code(self, map):
        response = map.generate_post_code(-2.3335548, 51.2167441)
        print(response)
        assert response[0]["context"][0]["text"] == "BA11 4QE"

    def test_update_directions_details(self, map, data):
        map.update_directions_details([[-2.31109], [51.22234]], data)
        print(map.routes["Start-Address"])
        assert map.routes["Start-Address"] == [
            "55 Tower View, Frome, Frome, BA11 5AP, United Kingdom"
        ]

    def test_configure_api_data(self, map):
        # api_data = map.configure_api_data(driving_routes,[-2.31705241493394, 51.2203620750975],[-2.31109549671642, 51.2224372245192])
        # assert api_data[3] == '81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom'
        api_data = map.configure_api_data()
        print(api_data)
        assert (
            api_data[3] == "81 Knights Maltings, Frome, Frome, BA11 5LB, United Kingdom"
        )

    def test_call_api(self, map):
        latlon_origin = Map.generate_latlon("BA11 5AP")
        latlon_destination = Map.generate_latlon("BA11 5LB")
        driving_routes = map.call_api(latlon_origin, latlon_destination)
        print(driving_routes)
        assert isinstance(driving_routes, dict)

    def test_save(self, map):
        df = map.save()
        print(df)
        assert df["Duration-Value"].iloc[0] >= 100  # [4]


class TestGooglePlacesConnection(object):
    def test_places(self):
        maps = GooglePlacesConnection()
        print(maps)
        assert str(maps.client).split(" ")[0] == "<googlemaps.client.Client"


class TestMapboxConnection(object):
    def test_geocoder(self):
        mapbox = MapboxConnection()
        print(mapbox)
        assert (
            str(mapbox.geocoder_client).split(" ")[0]
            == "<mapbox.services.geocoding.Geocoder"
        )

    def test_directions(self):
        mapbox = MapboxConnection()
        print(mapbox)
        assert (
            str(mapbox.directions_client).split(" ")[0]
            == "<mapbox.services.directions.Directions"
        )


class TestStation(object):
    @pytest.fixture
    def station(self):
        return Station("BA11 5LA", "Premium Diesel")

    def test_address(self, station):
        result = Station.address("BA11 5LA")
        print(result)
        assert result == [
            {
                "label": "BA11 5LA, Frome, Somerset, England, United Kingdom",
                "value": "BA11 5LA",
            }
        ]

    def test_call_api(self, station):
        result = station.call_api("BA11 5LA")
        print(result)
        assert (
            result["Response"]["DataItems"]["FuelStationDetails"]["FuelStationCount"]
            == 7
        )

    def test_call_processor(self, station):
        data = Utility.open_no_date("BA11 5LA")
        station.call_processor(data, "2019-08-06")
        print(station.data["Date"])
        assert "2019-08-06" in station.data["Date"]

    def test_reset(self, station):
        data = Utility.open_no_date("BA11 5LA")
        station.call_processor(data, "2019-08-06")
        station.reset()
        obj = {
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
        print(station.data)
        assert station.data == obj

    def test_get_route_data(self, station):
        station = Station("BA11 5LB", "Unleaded")
        df = station.get_route_data("BA11 5AP")
        print(df)
        assert len(df) == 29

    def test_update_table(self, station):
        df = pd.read_excel("Test_Station_get_data_df.xlsx")  # [3]
        df_dict = station.update_table(df)
        print(df_dict)
        assert isinstance(df_dict["df"]["Prediction"].iloc[0], (int, float))  # [4]

    def test_update(self, station):
        data = Utility.open_no_date("BA11 5LA")
        station.call_processor(data, "2019-08-06")
        print(station.data["SearchPostCode"])
        assert station.data["SearchPostCode"] == [
            "BA11 5LA",
            "BA11 5LA",
            "BA11 5LA",
            "BA11 5LA",
        ]


class TestVehicle(object):
    # tested on BA11 5LB / BA11 5AP on 21 July 2019 price data
    @pytest.fixture
    def car(self):
        return Vehicle("AV04YGE")

    def test_get_spec(self, car):
        d = car.get_spec()
        print(d)
        assert (
            (d["model"] == "PEUGEOT 206 GTI 180")
            and (d["fuel"] == "PETROL")
            and (d["capacity"] == 50.0)
            and (d["highway"] == 9.26)
            and (d["city"] == 5.26)
            and (d["combined"] == 7.21)
        )

    def test_save(self, car):
        result = car.save()
        output = Utility.open_no_date(f"vehicle-{car.registration}")
        print(result)
        assert (
            result["Response"]["StatusCode"]
            == "Success"
            == output["Response"]["StatusCode"]
            == "Success"
        )

    def test_get_tank_capacity(self, car):
        tank = car.get_tank_capacity()
        print(tank)
        assert tank == 50.0

    def test_get_fuel_type(self, car):
        fuel = car.get_fuel_type()
        print(fuel)
        assert fuel == "PETROL"

    def test_mpg(self, car):
        result = car.to_mpg(50)
        print(result)
        assert result == (50 / 4.54609)

    def test_prepare(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        d = car.prepare(hover, "BA11 5LB", "BA11 5AP", "Unleaded")
        print(d)
        assert (
            (d["station_post_code"] == "BA11 4NZ")
            and (d["df_directions"]["Duration-Value"].iloc[0] >= 0)  # [4]
            and (d["df_station"]["Brand"].iloc[0] == "ESSO")
            and (d["df"]["DistanceFromSearchPostcode"].iloc[0] == 0.07)
        )  # [4]

    def test_analysis(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        d = car.analysis(hover, "BA11 5LB", "BA11 5AP", "10", "Unleaded")
        print(d)
        assert (
            (isinstance(d["distance"], str))
            and (
                d["cost"]
                == "It will cost £53.16 to fill the fuel tank with Unleaded at ESSO, located at BA11 4NZ"
            )
            and (
                d["difference"]
                == "Price of fuel per litre is 6.2 pence higher than the cheapest petrol station on your journey, ASDA located at BA11 5LA, where the price is 126.7 pence"
            )
            and (
                d["saving"]
                == "Assuming a daily commute (5 days a week), you could save up to £9.35 per year if you fill at the cheapest petrol station on your journey, ASDA located at BA11 5LA"
            )
            and (
                d["day"]
                == "You will lose £0.02 if you fill your tank at this petrol station tomorrow as prices are predicted to rise tomorrow"
            )
            and (
                d["loss"]
                == "You will lose £2.48 if you fill your tank at this petrol station"
            )
        )

    def test_saving_analysis(self, car):
        d = car.saving_analysis(130.9, 130.9, 40.0, "ESSO", "BA11 4NZ", "Unleaded")
        print(d)
        assert (
            d["saving"]
            == "You will lose £0.0 if you fill your tank at this petrol station tomorrow as prices are predicted to rise tomorrow"
        ) and (
            d["selected_s"]
            == "It will cost £52.36 to fill the fuel tank with Unleaded at ESSO, located at BA11 4NZ"
        )

    def test_comparison_analysis(self, car):
        d = car.comparison_analysis(
            6.2, 124.7, "Unleaded", "ASDA", "BA11 5LA", 2.48, 9.35, "ESSO"
        )
        print(d)
        assert (
            (
                d["difference"]
                == "Price of fuel per litre is 6.2 pence higher than the cheapest petrol station on your journey, ASDA located at BA11 5LA, where the price is 124.7 pence"
            )
            and (
                d["losses"]
                == "You will lose £2.48 if you fill your tank at this petrol station"
            )
            and (
                d["comparison"]
                == "Assuming a daily commute (5 days a week), you could save up to £9.35 per year if you fill at the cheapest petrol station on your journey, ASDA located at BA11 5LA"
            )
        )

    def test_distance_analysis(self, car):
        analysis = car.distance_analysis("ESSO", "BA11 4NZ", 5.0, 8.0, 1.81)
        print(analysis)
        assert (
            analysis
            == "It will take you 8.0 minutes to reach ESSO at BA11 4NZ, 5.0 miles from the journey route, and cost you £1.81 in fuel to drive back and forth"
        )

    def test_prepare_comparison(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        d = car.get_tank_data()
        r = car.prepare(hover, "BA11 5LB", "BA11 5AP", "Unleaded")
        s = car.prepare_savings(d["capacity"], 40.0, r["df"], r["df_station"])
        d = car.prepare_comparison(
            r["df_directions"], d["city"], s["min"], s["station_price"], r["df"]
        )
        print(d)
        assert (
            (d["cheapest_location"] == "BA11 5LA")
            and (d["cheapest_brand"] == "ASDA")
            and (d["annual_loss"] == 9.35)
        )

    def test_prepare_distance(self, car):
        d = car.prepare_distance(
            "BA11 5LB", "BA11 5AP", "BA11 4NZ", 7.214991344210079, 130.9
        )
        print(d)
        assert (
            (d["distance"] == 5.0)
            and (d["duration"] >= 5.0)
            and (d["journey_cost"] == 1.81)
        )

    def test_round_offroutes(self, car):
        df_offroutes = DatabaseModel().read(
            "journey_route_information", f"BA11 5LB-BA11 5AP"
        )
        # df_offroutes = df_offroutes[(df_offroutes['origin'] == "BA11 5LB") & (df_offroutes['destination'] == "BA11 5AP")]
        latlon = Map.generate_latlon("BA11 4NZ")
        print(df_offroutes, "test_round_offroutes vishal")
        d = car.round_offroutes(latlon, Utility.to_dataframe(df_offroutes))
        print(d)
        assert len(d["df_offroutes"]) >= 10 and d["lon"] == -2.38 and d["lat"] == 51.2

    def test_filter_coordinates(self, car):
        df_offroutes = DatabaseModel().read(
            "journey_route_information", f"BA11 5LB-BA11 5AP"
        )
        # df_offroutes = df_offroutes[(df_offroutes['origin'] == "BA11 5LB") & (df_offroutes['destination'] == "BA11 5AP")]
        latlon = Map.generate_latlon("BA11 4NZ")
        d = car.round_offroutes(latlon, Utility.to_dataframe(df_offroutes))
        df_offroute = car.filter_coordinates(d["df_offroutes"], d["lon"], d["lat"])
        print(df_offroute)
        assert (abs(df_offroute["lat_destination"].iloc[0]) > 0) and (
            abs(df_offroute["lon_origin"].iloc[0]) > 0
        )  # [4]

    def test_tank_analysis(self, car):
        d = car.tank_analysis(10)
        print(d)
        assert (
            (
                d["highway_commentary"]
                == "Current fuel level will take you 92.6 miles on the highway"
            )
            and (
                d["city_commentary"]
                == "Current fuel level will take you 52.6 miles on city roads"
            )
            and (
                d["combined_commentary"]
                == "Current fuel level will take you 72.1 miles on the highway and city roads"
            )
            and (
                d["fuel_analysis"]
                == "Add 40.0 litres of PETROL to fill your tank to capacity"
            )
        )

    def test_get_tank_data(self, car):
        d = car.get_tank_data()
        print(d)
        assert (
            (d["capacity"] == 50.0)
            and (d["highway"] == 9.260705353391595)
            and (d["city"] == 5.2572650343481975)
            and (d["combined"] == 7.214991344210079)
            and (d["model"] == "PEUGEOT 206 GTI 180")
            and (d["fuel"] == "PETROL")
        )

    def test_prepare_savings(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        d = car.get_tank_data()
        r = car.prepare(hover, "BA11 5LB", "BA11 5AP", "Unleaded")
        d = car.prepare_savings(d["capacity"], 40.0, r["df"], r["df_station"])
        print(d)
        assert (
            (d["full_tank"] == 10.0)
            and (d["min"] == 126.7)
            and (d["station_price"] == 132.9)
            and (d["difference"] == 6.2)
            and (d["loss"] == 0.62)
            and (d["predicted_price"] >= 132.9)
            and (d["selected_station_brand"] == "ESSO")
        )

    def test_round_offroute(self, car):
        hover = {
            "points": [
                {
                    "curveNumber": 132,
                    "pointNumber": 5,
                    "pointIndex": 5,
                    "lon": -2.37697983629048,
                    "lat": 51.201507968634,
                    "customdata": "BA11 4NZ",
                    "text": "ESSO, Unleaded: 130.9p, BA11 4NZ",
                }
            ]
        }
        d = car.get_tank_data()
        data = car.prepare(hover, "BA11 5LB", "BA11 5AP", "Unleaded")
        s = car.prepare_savings(d["capacity"], 40.0, data["df"], data["df_station"])
        df_offroutes = DatabaseModel().read(
            "journey_route_information", f"BA11 5LB-BA11 5AP"
        )
        latlon = Map.generate_latlon("BA11 4NZ")
        o = car.round_offroutes(latlon, Utility.to_dataframe(df_offroutes))
        df_offroute = car.filter_coordinates(o["df_offroutes"], o["lon"], o["lat"])
        r = car.round_offroute(df_offroute, d["combined"], s["station_price"])
        print(r)
        assert (
            (r["distance"] == 5.0)
            and (r["duration"] > 1.0)
            and (r["journey_cost"] >= (1.81))
        )


class TestNearestStation(object):
    @pytest.fixture
    def pump(self):
        return NearestStation("EN1 1AA", "Diesel")

    def test_save(self, pump):
        df = pump.save()
        print(df)
        assert df["Brand"].iloc[0] == "TESCO"  # [4]

    def test_get_stations(self, pump):
        result = pump.get_stations()
        print(result)
        assert result["Price"].iloc[0] >= 110  # [4]

    def test_get_station_data(self, pump):
        df = pump.get_station_data("N17 7LY")
        print(df)
        assert df["PostCode"].iloc[0] == "N17 7LY"  # [4]

    def test_generate_brand_analysis(self, pump):
        data = pump.generate_brand_analysis(get_brand_analysis_input)
        print(data)
        assert data["supermarket"] == 5 and data["non_supermarket"] == 5

    def test_generate_metrics(self, pump):
        data = pump.generate_metrics(get_brand_analysis_input, 5, "Brand")
        print(data)
        assert (
            (len(data["df"]) == 8)
            and (data["min"] == 124.64)
            and (data["max"] == 131.9)
        )

    def test_generate_search_analysis(self, pump):
        data = pump.generate_search_analysis(get_brand_analysis_input)
        print(data)
        assert (
            (data["brand_today"] == "GULF")
            and (data["postcode_today"] == "EN3 4EJ")
            and (data["distance_today"] == 1.49)
            and (data["brand_tomorrow"] == "GULF")
            and (data["postcode_tomorrow"] == "EN3 4EJ")
            and (data["distance_tomorrow"] == 1.49)
        )

    def test_generate_station_timeseries(self, pump):
        data = pump.generate_station_timeseries("", get_brand_analysis_input)
        print(data)
        assert (
            (len(data["df"]) >= 22)
            and (isinstance(data["brand"], str))
            and (isinstance(data["station_post_code"], str))
        )

    def test_generate_routes(self, pump):
        stations_list = [
            "N17 7LY",
            "EN9 1JH",
            "EN8 0TA",
            "N18 3HF",
            "N9 7HL",
            "EN3 4EJ",
            "E4 8ST",
            "EN4 8QX",
            "EN4 0JY",
            "EN8 7RS",
        ]
        data = pump.generate_routes(stations_list)
        print(data)
        assert (len(data["df_route"]) > 0) and (data["routes"][-1] is not None)

    def test_generate_map_data(self, pump):
        df = pd.read_excel("Test_NearestPump_map_input.xlsx")
        data = pump.generate_map_data(df)
        print(data)
        assert (
            (isinstance(len(data["df_route"]), int))
            and (len(data["stations"]) == 1)
            and (len(data["routes"]) > 1)
        )


class TestNearestStationDashboardIntegration(object):
    def test_render_map_card2(self):
        data = Utility.to_dataframe(render_map_card2_input)
        station = NearestStation("EN1 1AA", "Unleaded")
        data = station.generate_map_data(data)
        print(data)
        assert len(data) == 4

    def test_createNewOptions(self):
        result = Station.address("EN1 1AA")
        print(result)
        assert result == [
            {
                "label": "EN1 1AA, Enfield, Greater London, England, United Kingdom",
                "value": "EN1 1AA",
            }
        ]

    def test_render_data_table(self):
        post_code = Utility.to_uppercase("EN1 1AA")
        station = NearestStation("EN1 1AA", "Unleaded")
        stations = station.get_stations()
        table = Station("EN1 1AA", "Unleaded").update_table(stations)
        print(table)
        assert len(table) == 2

    def test_render_search_result(self):
        response = NearestStation("EN1 1AA", "Unleaded").get_stations()
        print(response)
        assert len(response) == 10

    def test_render_station_details(self):
        station = NearestStation("EN1 1AA", "Unleaded")
        ts = station.generate_station_timeseries("", render_map_card2_input)
        print(ts)
        assert len(ts["df"]) == 22

    def test_render_summary_cards(self):
        station = NearestStation("EN1 1AA", "Unleaded")
        data = station.generate_search_analysis(render_map_card2_input)
        print(data)
        assert len(data) == 6

    def test_render_pie_chart(self):
        station = NearestStation("EN1 1AA", "Unleaded")
        data = station.generate_brand_analysis(render_map_card2_input)
        print(data)
        assert len(data) == 2

    def test_render_bar_chart(self):
        station = NearestStation("EN1 1AA", "Unleaded")
        data = station.generate_metrics(render_map_card2_input, 5, "Brand")
        print(data)
        assert isinstance(data["min"], (int, float)) and isinstance(
            data["max"], (int, float)
        )


class TestJourneySaverDashboardIntegration(object):
    def test_createNewOptions_origin(self):
        address = Station.address("BA3 2HW")
        print(address)
        assert address == [
            {
                "label": "BA3 2HW, Radstock, Bath And North East Somerset, England, United Kingdom",
                "value": "BA3 2HW",
            }
        ]

    def test_createNewOptions_destination(self):
        address = Station.address("BA8 0SJ")
        print(address)
        assert address == [
            {
                "label": "BA8 0SJ, Templecombe, Somerset, England, United Kingdom",
                "value": "BA8 0SJ",
            }
        ]

    def test_render_final_form_input(self):
        response = Vehicle("AV04YGE").data
        print(response)
        assert response["Response"]["StatusCode"] == "Success"

    def test_render_tank_dial(self):
        capacity = Vehicle("AV04YGE").get_tank_capacity()
        print(capacity)
        assert capacity == 50.0

    def test_render_fuel_type(self):
        fuel = Vehicle("AV04YGE").get_fuel_type()
        print(fuel)
        assert fuel == "PETROL"

    def test_render_car_details(self):
        vehicle = Vehicle("AV04YGE")
        spec = vehicle.get_spec()
        print(spec)
        assert len(spec) == 6

    def test_render_tank_analysis(self):
        analysis = Vehicle("AV04YGE").tank_analysis(10)
        print(analysis)
        assert len(analysis) == 4

    def test_render_journey_result(self):
        station = JourneyStation("BA3 2HW", "Unleaded", "BA8 0SJ")
        df = station.get_journey_data()
        table = Station("BA3 2HW", "Unleaded", "BA8 0SJ").update_table(df)
        print(table)
        assert len(table["df"]) == 12

    def test_update_journey_map(self):
        df = Utility.to_dataframe(render_journey_result_input)
        station = JourneyStation("BA3 2HW", "Unleaded", "BA8 0SJ")
        data = station.generate_map_data(df)
        print(data)
        assert len(data) == 6

    def test_render_journey_analysis(self):
        vehicle = Vehicle("AV04YGE")
        analysis = vehicle.analysis(
            render_journey_analysis_input, "BA3 2HW", "BA8 0SJ", 10, "Unleaded"
        )
        print(analysis)
        assert len(analysis) == 6
