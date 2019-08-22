##############IMPORTS IN FUEL MODEL CLASS  FILE#######################from fuel_prediction_algorithm import *
from training_data import text_training_data
import requests

# from datetime import datetime, timedelta, date
import datetime
import pandas as pd
import json
from sqlalchemy import create_engine, exc
import plotly.graph_objs as go
from mapbox import Directions
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


from fuel_prediction_algorithm_class import *

from fuel_prediction_processor_class import *

from fuel_maps_api_class import *

from fuel_model_class import *
import tweepy
from tweepy.streaming import StreamListener
from rac_links import *
from requests.exceptions import RequestException
from contextlib import closing
from requests import get
from bs4 import BeautifulSoup
from textblob.classifiers import NaiveBayesClassifier
from sklearn.preprocessing import MinMaxScaler

###################################################################
from fuel_prediction_algorithm import *

from fuel_prediction_processor import *

from fuel_maps_api import *


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

import json
import ibm_cloud_sdk_core
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
    SentimentOptions,
)

########################
from matplotlib import pyplot as plt

# import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

##################

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

# from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


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

from ibm_watson import DiscoveryV1
import dash_daq as daq
from wordcloud import WordCloud

from app import app

# from apps import app1, app2
from fuel_app_style import *
import dash_bootstrap_components as dbc
import dash_html_components as html
from textblob.classifiers import NaiveBayesClassifier
import os
from rac_links import *
from master_class_file import *

####################################################################


mapbox_access_token = "pk.eyJ1IjoidnMyMDE5IiwiYSI6ImNqd29ydWh5cDFkajQ0NG9sc3FwbGtyY2IifQ.H9Y11sNtzZ1bOAzgu_mnVA"
############################################################################################################################################################
class DateHelper:
    @staticmethod
    def get_today_date():
        today = datetime.date.today()
        return str(today)


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
        if "DirectionsOffRoute" in table:
            table = "DirectionsOffRoute"
        df.to_sql(table, con=self.connection, if_exists="append", index=False)

    def read(self, table):
        return pd.read_sql(f"select * from {table}", self.connection)

    def drop(self, table):
        connection = self.connection.raw_connection()
        cursor = connection.cursor()
        command = f"DROP TABLE IF EXISTS {table};"
        cursor.execute(command)
        connection.commit()
        cursor.close()


class FileHelper:
    @staticmethod
    def save(api, data):
        date = DateHelper.get_today_date()
        with open(f"{api}-{date}.json", "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

    @staticmethod
    def save_no_date(name, data):
        with open(f"{name}.json", "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

    @staticmethod
    def open(api):
        date = DateHelper.get_today_date()
        with open(f"{api}-{date}.json", "r") as handle:
            return json.load(handle)

    @staticmethod
    def open_no_date(name):
        with open(f"{name}.json", "r") as handle:
            return json.load(handle)

    @staticmethod
    def read(file):
        arr = []
        with open(file, "r") as f:
            x = f.readlines()
        for ls in x:
            d = json.loads(ls)
            arr.append(d)
        return arr


class DataFrameHelper:
    @staticmethod
    def to_dataframe(obj):
        return pd.DataFrame(obj)

    @staticmethod
    def drop_duplicate(df, columns):
        return df.drop_duplicates(subset=columns)

    @staticmethod
    def sort_columns(df, cols):
        return df.sort_values(cols)


class UIComponentLogic:
    @classmethod
    def to_uppercase(cls, post_code):
        if post_code != None:
            return post_code.upper()
        return None


class UIComponent:
    @classmethod
    def render_twitter_trace(cls, handle, y_ax):
        return go.Bar(x=[handle], y=[y_ax], name=handle)

    @classmethod
    def render_routes(cls, df_route, route_information, i):
        return go.Scattermapbox(
            lat=[df_route["Lat"].iloc[i], df_route["Lat"].iloc[i + 1]],
            lon=[df_route["Lng"].iloc[i], df_route["Lng"].iloc[i + 1]],
            mode="lines",
            text=route_information,
        )

    @classmethod
    def render_journey_route(cls, df_route, route_information, i):
        return go.Scattermapbox(
            lat=[df_route["Lat"].iloc[i], df_route["Lat"].iloc[i + 1]],
            lon=[df_route["Lng"].iloc[i], df_route["Lng"].iloc[i + 1]],
            mode="lines",
            text=route_information,
            marker={"size": 10, "color": "black"},
        )

    @classmethod
    def render_stations(cls, df):
        return [
            go.Scattermapbox(
                lat=df["Lat"],
                lon=df["Lon"],
                mode="markers",
                marker={"size": 10},
                text=df["Information"],
                customdata=df["Post Code"],
                hoverinfo="text",
                name="Results",
            )
        ]

    @classmethod
    def render_station_route(cls, df):
        return go.Scattermapbox(
            lat=[df["lat_origin"].iloc[k], df["lat_destination"].iloc[k]],
            lon=[df["lon_origin"].iloc[k], df["lon_destination"].iloc[k]],
            mode="lines",
            text=df["route_information"].iloc[k],
            marker={"size": 3},
        )

    @classmethod
    def render_off_route(cls, closest_coordinate, route_information, k):
        return go.Scattermapbox(
            lat=[closest_coordinate[k][1], closest_coordinate[k + 1][1]],
            lon=[closest_coordinate[k][0], closest_coordinate[k + 1][0]],
            mode="lines",
            text=route_information,
            marker={"size": 3},
        )

    @classmethod
    def render_origin(cls, search_lat, search_lon, post_code):
        return [
            go.Scattermapbox(
                lat=[search_lat],
                lon=[search_lon],
                mode="markers",
                marker={"size": 16, "color": "black"},
                text=post_code,
                hoverinfo="text",
                name="Results",
            )
        ]

    @classmethod
    def render_nearest_map(cls, df_route, search_code, stations, routes):
        layout = cls.render_layout(df_route)
        return go.Figure(data=search_code + stations + routes, layout=layout)

    @classmethod
    def render_journey_map(
        cls, df_route, origin_plot, destination_plot, routes, off_routes, stations
    ):
        layout = cls.render_layout(df_route)
        fig = go.Figure(
            data=origin_plot + destination_plot + routes + off_routes + stations,
            layout=layout,
        )
        return dcc.Graph(
            id="data-table-analytics2",
            figure=fig,
            hoverData={"points": [{"customdata": ""}]},
        )

    @classmethod
    def render_layout(cls, df_route):
        return go.Layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode="closest",
            showlegend=False,
            mapbox={
                "accesstoken": mapbox_access_token,
                "bearing": 0,
                "center": {
                    "lat": df_route["Lat"].iloc[0],
                    "lon": df_route["Lng"].iloc[0],
                },
                "pitch": 30,
                "zoom": 10,
                "style": "mapbox://styles/mapbox/light-v9",
            },
        )

    @classmethod
    def discovery(cls, data):
        movement = cls.badge(data[0])
        return movement, data[2], data[3]

    @classmethod
    def badge(cls, data):
        if "down" in data:
            movement = dbc.Badge(data, color="success")
        elif "No change" in data:
            movement = dbc.Badge(data, color="primary")
        else:
            movement = dbc.Badge(data, color="danger")
        return movement

    @classmethod
    def rac(cls, data):
        overall = cls.badge(data[0])
        unleaded = cls.badge(data[2])
        diesel = cls.badge(data[3])
        super_unleaded = cls.badge(data[4])
        lpg = cls.badge(data[5])
        return overall, unleaded, diesel, super_unleaded, lpg

    @classmethod
    def search_price_button(cls):
        return dbc.Button(
            children="Search Fuel Prices",
            color="primary",
            id="submit-button",
            n_clicks=0,
            size="lg",
        )

    @classmethod
    def fuel_knob(cls, capacity):
        return dbc.FormGroup(
            [
                dbc.Label("Select Current Fuel Level"),
                daq.Knob(
                    label="Fuel Tank Meter",
                    id="knob",
                    max=capacity,
                    scale={"start": 0, "labelInterval": 5, "interval": 1},
                    value="10",
                ),
            ]
        )

    @classmethod
    def fuel_radio_items(cls, options_list):
        return dbc.FormGroup(
            [
                dbc.Label("Select Fuel Grade"),
                dbc.RadioItems(
                    options=options_list, inline=True, id="fuel_type", value="Unleaded"
                ),
            ]
        )

    @classmethod
    def car_card(cls, registration, model, fuel, tank, highway, city, combined):
        card_content = [
            dbc.CardHeader(f"Car Details for {registration}"),
            dbc.CardBody(
                [
                    html.H5(f"{model}", className="card-title"),
                    html.P(f"Fuel: {fuel}", className="card-text"),
                    html.P(f"Tank Capacity: {tank}", className="card-text"),
                    html.P(f"Highway Mileage (MPG): {highway}", className="card-text"),
                    html.P(f"Urban Mileage (MPG): {city}", className="card-text"),
                    html.P(
                        f"Combined Mileage (MPG): {combined}", className="card-text"
                    ),
                ]
            ),
        ]
        return dbc.Card(card_content, color="dark", inverse=True)

    @classmethod
    def nearest_pump_bar(cls, trace1, trace2, min, max):
        return {
            "data": [trace1, trace2],
            "layout": go.Layout(
                title=f"Graph",
                colorway=["#EF963B", "#EF533B"],
                hovermode="closest",
                xaxis={
                    "title": "Post Code",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"size": 9, "color": "black"},
                },
                yaxis={
                    "title": "Price (pence)",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"color": "black"},
                    "range": [min - 5, max + 5],
                },
            ),
        }

    @classmethod
    def bar_trace(cls, df, x, y):
        return go.Bar(x=df[x], y=df[y], name=y)

    @classmethod
    def nearest_pie(cls, supermarket, non_supermarket):
        return {
            "data": [
                go.Pie(
                    labels=["Supermarket", "Non-Supermarket"],
                    values=[supermarket, non_supermarket],
                    marker={"colors": ["#FEBFB3", "#96D38C"]},
                    textinfo="label",
                )
            ],
            "layout": go.Layout(),
        }

    @classmethod
    def card_detail(cls, title, body):
        return [
            dbc.CardHeader(html.H5(title, className="card-title")),
            dbc.CardBody([html.P(body, className="card-text")]),
        ]

    @classmethod
    def map_card(cls, title, map):
        card_content = [
            dbc.CardHeader(html.H5(title, className="card-title")),
            dbc.CardBody(map),
        ]
        return [dbc.Card(card_content, color="dark", outline=True, className="mx-0")]

    @classmethod
    def cards_layout(cls, n_rows, n_cols, colors, data):
        result = []
        data_counter = 0
        for row in range(n_rows):
            row_data = []
            for col in range(n_cols):
                card = dbc.Col(
                    dbc.Card(data[data_counter], color=colors[row], inverse=True)
                )
                data_counter += 1
                row_data.append(card)
            result.append(dbc.Row(row_data, className="mb-4"))
        return result

    @classmethod
    def station_scatter_line(cls, df, brand, post_code):
        return {
            "data": [go.Scatter(x=df.index, y=df["Prediction"], mode="lines+markers")],
            "layout": {
                "title": f"Fuel Price for {brand} at {post_code}",
                "height": 225,
                # 'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
                "margin": {"l": 40, "b": 30, "r": 20, "t": 30},
                "annotations": [
                    {
                        "x": 0,
                        "y": 0.85,
                        "xanchor": "left",
                        "yanchor": "bottom",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "align": "left",
                        "bgcolor": "rgba(255, 255, 255, 0.5)",
                        "text": "",
                    }
                ],
                "yaxis": {"type": "linear"},
                "xaxis": {"showgrid": False},
            },
        }

    @classmethod
    def incorrect_input_alert(cls):
        return dbc.Alert("Post Code and/or Fuel Type not entered", color="warning")

    @classmethod
    def incorrect_journey_input_alert(cls):
        return dbc.Alert(
            "Origin Post Code and/or Finish Post Code and/or Fuel Grade and/or Fuel Level not entered",
            color="warning",
        )

    @classmethod
    def incorrect_registration_alert(cls):
        return dbc.Alert("Registration needs to contain an 'A'", color="warning")

    @classmethod
    def invalid_post_code(cls):
        return dbc.Alert(
            "Invalid Post Code. The Post Code needs to include the letter A",
            color="danger",
        )

    @classmethod
    def success(cls):
        return dbc.Alert(
            "Success - API data found for this origin and destination", color="danger"
        )

    @classmethod
    def failure(cls):
        return dbc.Alert(
            "Failure - API data not found for this origin and destination",
            color="danger",
        )

    @classmethod
    def no_results(cls, post_code, fuel_type):
        return dbc.Alert(
            f"There are no pumps in the {post_code} area that supply {fuel_type}",
            color="danger",
        )

    @classmethod
    def no_data(cls, post_code, fuel_type):
        return dbc.Alert(
            f"We do not hold data for fuel pumps in the {post_code} area",
            color="danger",
        )

    @classmethod
    def search_alerts(cls, df, post_code):
        range_today = df["Price"].max() - df["Price"].min()
        range_tomorrow = (
            df["1-Day Price Prediction"].max() - df["1-Day Price Prediction"].min()
        )
        alert = html.Div(
            [
                dbc.Alert(
                    f"Success, we have found you fuel prices for {df['PostCode'].count()} pumps in {post_code}",
                    color="primary",
                ),
                html.Hr(),
                dbc.Button(
                    "Summary Statistics", id="alert-toggle-fade", className="mr-1"
                ),
                html.Hr(),
                dbc.Alert(
                    [
                        html.P(
                            f"Today's Minimum Price: {round(df['Price'].min(),1)} pence"
                        ),
                        html.P(
                            f"Tomorrow's Minimum Price: {round(df['1-Day Price Prediction'].min(),1)} pence"
                        ),
                        html.P(f"Today's Price Range: {round(range_today,1)} pence"),
                        html.P(
                            f"Tomorrow's Price Range: {round(range_tomorrow,1)} pence"
                        ),
                    ],
                    id="alert-fade",
                    dismissable=True,
                    is_open=True,
                ),
            ]
        )
        return alert

    @classmethod
    def data_table_card(cls, df1, df):
        table = dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i, "deletable": False} for i in df1.columns],
            data=df.to_dict("records"),
            style_table={
                "maxHeight": "500px",
                "overflowY": "scroll",
                "overflowX": "scroll",
                "border": "thin lightgrey solid",
            },
            style_cell={
                "whiteSpace": "no-wrap",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "maxWidth": 8,
                "textAlign": "left",
                "padding": "5px",
            },
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
                # 'border': '1px solid blue'
            },
            css=[
                {
                    "selector": ".dash-cell div.dash-cell-value",
                    "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
                }
            ],
            style_as_list_view=True,
            editable=True,
            filtering=True,
            sorting=True,
            sorting_type="multi",
            row_selectable="multi",
            row_deletable=True,
            selected_rows=[],
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)",
                    "if": {"column_id": "Price"},
                    "backgroundColor": "#3D9970",
                    "color": "white",
                }
            ],
        )
        card_content = [
            dbc.CardHeader(html.H5("Fuel Price Table", className="card-title")),
            dbc.CardBody(table),
        ]
        return [dbc.Card(card_content, color="dark", outline=True)]

    @classmethod
    def scatter_line(cls, df, title):
        plot = go.Scatter(x=df.index, y=df["Prediction"], mode="lines+markers")
        graph = dcc.Graph(
            figure={
                "data": [plot],
                "layout": go.Layout(
                    title=f"Fuel Price Prediction: {title}",
                    yaxis={"title": "Price (pence)", "type": "linear"},
                    xaxis={
                        "title": "Date",
                        "tickangle": 45,
                        "showgrid": False,
                        "tickformat": "%b %Y",
                    },
                ),
            }
        )
        return graph

    @classmethod
    def bar_chart(cls, traces):
        fig2 = {
            "data": traces,
            "layout": go.Layout(
                title="tweets",
                colorway=["#EF963B", "#EF533B"],
                hovermode="closest",
                xaxis={
                    "title": "Twitter Handles",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"size": 9, "color": "black"},
                },
                yaxis={
                    "title": "Mean Sentiment Score of 25 latest tweets",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"color": "black"},
                },
            ),
        }
        return fig2


class Vehicle:
    def __init__(self, reg):
        self.registration = reg
        self.data = self.save()

    # def get_data(self):
    #     return self.data
    # tested
    def get_spec(self):
        tank = self.data["Response"]["DataItems"]["TechnicalDetails"]["Dimensions"][
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
        # print(model,fuel,tank,highway,city,combined,"Vehicle get_spec output")
        return model, fuel, tank, highway, city, combined

    # tested
    def save(self):
        try:
            data = FileHelper.open_no_date(f"vehicle-{self.registration}")
        except Exception as e:
            # print(e)
            result = requests.get(
                f"https://uk1.ukvehicledata.co.uk/api/datapackage/VehicleData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_VRM={self.registration}"
            )
            data = result.json()
            FileHelper.save_no_date(f"vehicle-{self.registration}", data)
        # print(data,"Vehicle save output")
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
    def mpg(self, mpg):
        # print(mpg / 4.54609,"Vehicle mpg output")
        return mpg / 4.54609

    # tested
    def analysis_dataframes(self, hoverData, origin, destination, fuel_type):
        # print(hoverData,origin,destination,fuel_type,"Vehicle analysis_dataframes input")
        station_post_code = hoverData["points"][0]["customdata"]
        today = DateHelper.get_today_date()
        station = Station(origin, fuel_type, destination)
        df = station.get_journey_data()
        df_station = df[
            (df["PostCode"] == station_post_code)
            & (df["Date"] == today)
            & (df["FuelType"] == fuel_type)
        ]
        # df_station = df[df['PostCode'] == station_post_code]
        df_directions = station.get_directions()
        df_places = station.get_places(df_directions)
        post_codes = Station.get_unique_stations(df_places)
        # #print(df,df_station,df_directions,station_post_code,"vishalanalysis")
        # print(df,df_station,df_directions,station_post_code,"Vehicle analysis_dataframes output")
        return df, df_station, df_directions, station_post_code

    # tested
    def analysis(self, hoverData, origin, destination, tank, fuel_type):
        # print(hoverData, origin,destination,tank,fuel_type,"Vehicle analysis input")
        capacity, highway, city, combined, model, fuel = self.get_tank_data()
        df_r, df, route, station = self.analysis_dataframes(
            hoverData, origin, destination, fuel_type
        )
        # print(route['Distance-Value'],"df route analysis")
        # #print(df_r,df,route,station,"#1")

        full, min, price, difference, loss, prediction, brand = self.savings_inputs(
            capacity, float(tank), df_r, df
        )
        # #print(full,min,price,difference,loss,prediction,brand,"#2")
        saving, selected_s = self.saving_analysis(
            prediction, price, full, brand, station, fuel_type
        )
        # #print(saving,selected_s,"#3")

        cheapest_l, cheapest_b, annual = self.comparison_inputs(
            route, city, min, price, df_r
        )
        # #print(cheapest_l,cheapest_b,annual,"#4")

        difference, losses, comparison = self.comparison_analysis(
            difference, min, fuel_type, cheapest_b, cheapest_l, loss, annual, brand
        )
        # #print(difference,losses,comparison,"#5")

        distance, duration, journey = self.distance_inputs(
            origin, destination, station, combined, price
        )
        # #print(distance,duration,journey,"#6")

        distance = self.distance_analysis(brand, station, distance, duration, journey)
        # #print(distance,"#6")

        # print(distance,selected_s,difference,losses,comparison,saving,"Vehicle analysis output")
        return distance, selected_s, difference, losses, comparison, saving

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
            analysis_3 = f"If you make this journey tomorrow, you will save £{round(predicted_saving,2)} to fill up your tank compared to filling it up today at this station"
        else:
            predicted_saving = predicted_price - station_price
            predicted_saving = (predicted_saving * full_tank) / 100
            analysis_3 = f"If you make this journey tomorrow, you will lose £{round(predicted_saving,2)} to fill up your tank compared to filling it up today at this station"
        selected_station = f"£{round(((station_price * full_tank)/100),2)} to fill up {fuel_type} fuel at {selected_station_brand} located at {station_post_code}"
        # print(analysis_3,selected_station,"Vehicle saving_analysis output")
        return analysis_3, selected_station

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
            analysis_difference = f"{difference} p more expensive than the minimum price which is {min} of {fuel_type} in your search which is {cheapest_brand} located at {cheapest_location}"
            analysis_loss = f"Loss of £{loss}"
        else:
            analysis_difference = f"{cheapest_brand} at {cheapest_location} is the cheapest station in your search"
            analysis_loss = f"No loss"

        analysis_4 = f"On a daily commute (5 days a week), you could save up to £{annual_loss} per year if you fill at {cheapest_brand} located at {cheapest_location} rather than this station"
        # print(analysis_difference,analysis_loss,analysis_4,"Vehicle comparison_analysis output")
        return analysis_difference, analysis_loss, analysis_4

    # tested
    def comparison_inputs(self, df_route, city, min, station_price, df_raw):
        # print(df_route,city,min,station_price,df_raw,"Vehicle comparison_inputs inputs")
        # print(city,min,station_price,df_route,df_raw,"comparison inputs")
        journey_distance = df_route["Distance-Value"].iloc[0] / 1000
        # print(journey_distance,"journey distance")
        min_annual_cost = (((journey_distance * 260) / city) * min) / 100
        station_annual_cost = (((journey_distance * 260) / city) * station_price) / 100
        annual_loss = round((station_annual_cost - min_annual_cost), 2)
        sorted_df = df_raw.sort_values("Price")
        cheapest_brand = sorted_df["Brand"].iloc[0]
        cheapest_location = sorted_df["PostCode"].iloc[0]
        # print(cheapest_location,cheapest_brand,annual_loss,"Vehicle comparison_inputs outputs")
        return cheapest_location, cheapest_brand, annual_loss

    # tested
    def round_offroutes(self, latlon, df_offroutes):
        # print(latlon,df_offroutes,"Vehicle round_offroutes inputs")
        latlon[0] = round(latlon[0], 2)
        latlon[1] = round(latlon[1], 2)
        decimals = 2
        df_offroutes["lat_destination"] = df_offroutes["lat_destination"].apply(
            lambda x: round(x, decimals)
        )
        df_offroutes["lat_origin"] = df_offroutes["lat_origin"].apply(
            lambda x: round(x, decimals)
        )
        df_offroutes["lon_destination"] = df_offroutes["lon_destination"].apply(
            lambda x: round(x, decimals)
        )
        df_offroutes["lon_origin"] = df_offroutes["lon_origin"].apply(
            lambda x: round(x, decimals)
        )
        # print(df_offroutes,latlon[0],latlon[1],"Vehicle round_offroutes output")
        return df_offroutes, latlon[0], latlon[1]

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
        distance = df_offroute["route_information"].iloc[0]
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
        return distance, duration, journey_cost

    # tested
    def filter_coordinates(self, df_offroutes, latlon_0, latlon_1):
        # print(df_offroutes,latlon_0,latlon_1,"Vehicle filter_coordinates inputs")
        df_offroute = df_offroutes[
            (df_offroutes["lat_destination"] == latlon_1)
            & (df_offroutes["lon_destination"] == latlon_0)
        ]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_origin"] == latlon_1)
                & (df_offroutes["lon_origin"] == latlon_0)
            ]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_origin"] == latlon_1)
                & (df_offroutes["lon_destination"] == latlon_0)
            ]
        if len(df_offroute) < 1:
            df_offroute = df_offroutes[
                (df_offroutes["lat_destination"] == latlon_1)
                & (df_offroutes["lon_origin"] == latlon_0)
            ]
        # print(df_offroute,"Vehicle filter_coordinates outputs")
        return df_offroute

    # tested
    def distance_inputs(
        self, origin, destination, station_post_code, combined, station_price
    ):
        # print(origin,destination,station_post_code,combined,station_price,"Vehicle distance_inputs inputs")
        df_offroutes = DatabaseModel().read("DirectionsOffRoute")
        # #print(df_offroutes,'databasereadvishaloffroutes')
        df_offroutes = df_offroutes[
            (df_offroutes["origin"] == origin)
            & (df_offroutes["destination"] == destination)
        ]
        # #print(df_offroutes,'databasereadvishaloffroutesfiltered')
        latlon = MapboxDirections.generate_latlon(station_post_code)
        df_offroutes, latlon[0], latlon[1] = self.round_offroutes(latlon, df_offroutes)
        df_offroute = self.filter_coordinates(df_offroutes, latlon[0], latlon[1])
        # #print(df_offroute,"distanceinputsvishal")
        # #print(df_offroute,"filtereddistanceinputsvishal")
        # if df_offroute.empty:
        #     df_offroutes,latlon[0],latlon[1] = self.split_offroutes(latlon,df_offroutes)
        #     df_offroute = self.filter_coordinates(df_offroutes,latlon[0],latlon[1])
        distance, duration, journey_cost = self.round_offroute(
            df_offroute, combined, station_price
        )
        # print(distance,duration,journey_cost,"Vehicle distance_inputs inputs")
        return distance, duration, journey_cost

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
        return f"{selected_station_brand} at {station_post_code} is off route by {distance} km. It will take you {duration*2} mins to make this excursion and cost you £{journey_cost} to drive to and back from the station."

    # tested
    def savings_inputs(self, capacity, tank, df_raw, df):
        # print(capacity,tank,df_raw,df,"Vehicle savings_inputs inputs")
        full_tank = capacity - tank
        min = round(df_raw["Price"].min(), 2)
        max = df_raw["Price"].max()
        station_price = df["Price"].iloc[0]
        difference = round((station_price - min), 2)
        loss = round(((full_tank * difference) / 100), 2)
        if loss < 0:
            save_loss = "save"
        else:
            save_loss = "lose"
        predicted_price = df["1-Day Price Prediction"].iloc[0]
        selected_station_brand = df["Brand"].iloc[0]
        # print(full_tank,min,station_price,difference,loss,predicted_price,selected_station_brand,"Vehicle savings_inputs outputs")
        return (
            full_tank,
            min,
            station_price,
            difference,
            loss,
            predicted_price,
            selected_station_brand,
        )

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
        highway = self.mpg(highway)
        city = self.mpg(city)
        combined = self.mpg(combined)
        # print(capacity,highway,city,combined,model,fuel,"Vehicle get_tank_data outputs")
        return capacity, highway, city, combined, model, fuel

    # tested
    def tank_analysis(self, tank):
        # print(tank,"Vehicle tank_analysis inputs")
        capacity, highway, city, combined, model, fuel = self.get_tank_data()
        tank = float(tank)
        # #print(tank,highway,"tank_analysis")
        highway_commentary = f"Driving on the highway, your current fuel in the tank will take you {round((tank * highway),1)} miles. "
        city_commentary = f"Driving in the city, your current fuel in the tank will take you {round((tank * city),1)} miles. "
        combined_commentary = f"Driving in both city and highway, your current fuel in the tank will take you {round((combined * tank),1)} miles. "
        if (capacity - tank) > 0:
            fuel_analysis = f"To top up your fule tank to its full capacity, you can put in {round((capacity - tank),1)} litres of {fuel}. "
        else:
            fuel_analysis = f"Your tank is currently full"
        # print(highway_commentary,city_commentary, combined_commentary,fuel_analysis,"Vehicle tank_analysis outputs")
        return highway_commentary, city_commentary, combined_commentary, fuel_analysis


class Station:
    def __init__(self, origin, fuel_type, destination=None):
        self.origin = UIComponentLogic().to_uppercase(origin)
        self.destination = UIComponentLogic().to_uppercase(destination)
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
        # self.data = self.save()

    # tested
    @staticmethod
    def address(value):
        # print(value,"Station address input")
        try:
            mapbox = MapboxDirections(value)
            addresses = mapbox.get_address()
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
        # print(result,"Station address output")
        return result

    # tested
    def call_api(self):
        try:
            data = FileHelper.open(self.origin)
        except Exception as e:
            # print(e)
            result = requests.get(
                f"https://uk1.ukvehicledata.co.uk/api/datapackage/FuelPriceData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_postcode={self.origin}"
            )
            data = result.json()
            FileHelper.save(self.origin, data)
        # print(data,"Station call_api output")
        return data

    # tested
    def get_stations(self):
        try:
            df = DatabaseModel().read("stations")
            today = DateHelper.get_today_date()
            df = df[
                (df["SearchPostCode"] == self.origin)
                & (df["Date"] == today)
                & (df["FuelType"] == self.fuel_type)
            ]
            if len(df) < 1:
                raise ValueError
        except (ValueError, exc.SQLAlchemyError) as e:
            # print(e)
            df = NearestPump(self.origin, self.fuel_type).save()
        # print(df,"Station get_stations output")
        return df

    # tested
    def get_directions(self):
        try:
            df = DatabaseModel().read("DirectionsAPI")
            df = df[
                (df["Origin"] == self.origin) & (df["Destination"] == self.destination)
            ]
            if len(df) < 1:
                raise ValueError
        except (ValueError, exc.SQLAlchemyError) as e:
            # print(e)
            mapbox = MapboxDirections(self.origin, self.destination)
            df = mapbox.save()
        # print(df,"Station get_directions output")
        return df

    # tested
    def get_places(self, df_directions):
        try:
            df = DatabaseModel().read("GoogleMapsPlacesNearby")
            df = df[
                (df["Origin"] == self.origin) & (df["Destination"] == self.destination)
            ]
            if len(df) < 1:
                raise ValueError
        except (ValueError, exc.SQLAlchemyError) as e:
            # print(e)
            places = GoogleMapsPlaces(self.origin, self.destination, df_directions)
            df = places.save()
        # print(df,"Station get_places output")
        return df

    # tested
    def get_journey_data(self):
        df_directions = self.get_directions()
        # print(df_directions,"get_journey_data_vishal")
        df_places = self.get_places(df_directions)
        post_codes = Station.get_unique_stations(df_places)
        today = DateHelper.get_today_date()
        try:
            df = DatabaseModel().read("stations")
            df = df[
                (df["SearchPostCode"].isin(post_codes))
                & (df["FuelType"] == self.fuel_type)
                & (df["Date"] == today)
            ]
            if len(df) < 1:
                raise ValueError
        except (ValueError, exc.SQLAlchemyError) as e:
            # print(e)
            df = Journey(self.origin, self.fuel_type, self.destination).save(post_codes)
        # print(df,"Station get_journey_data output")
        return df

    # tested
    @staticmethod
    def get_unique_stations(df):
        # print(df,"Station get_unique_stations input")
        df.to_excel("Test_Station_get_unique_stations_df.xlsx")
        unique_postcodes = df["Station-PostCode"].drop_duplicates().values.tolist()
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
        # print(postcodes,"Station get_unique_stations output")
        return postcodes

    # tested
    def get_data(self, df):
        # print(df,"Station get_data input")
        df.to_excel("Test_Station_get_data_df.xlsx")
        df = DataFrameHelper.drop_duplicate(df, ["PostCode"])
        df["TimeRecorded"] = df["TimeRecorded"].str.split().str[0]
        df.rename(
            {
                "PostCode": "Post Code",
                "DistanceFromSearchPostcode": "Distance",
                "1-Day Price Prediction": "Prediction",
                "TimeRecorded": "DateR",
                "1-Day Prediction Confidence": "Error",
            },
            axis=1,
            inplace=True,
        )
        cols = ["Distance", "Price", "Prediction", "Error"]
        df[cols] = df[cols].round(2)
        df1 = df[["Brand", "Post Code", "Price", "Prediction", "DateR", "Error"]]
        # print(df1,df,"Station get_data output")
        return df1, df

    # tested
    def update_data(self, latlon, date, data, d, prediction, p):
        # print(latlon,date,data,d,prediction,p,"Station update_data input")
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
        # print(self.data,"Station update_data output")

    # tested
    def reset_data(self):
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
        # print(self.data,"Station reset_data output")

    # tested
    def get_station_data(self, station):
        # print(station,"Station get_station_data input")
        df = DatabaseModel().read("stations")
        today = DateHelper.get_today_date()
        # print(df[(df['PostCode'] == station) & (df['Date'] == today) & (df['FuelType'] == self.fuel_type)],"Station get_station_data output")
        return df[
            (df["PostCode"] == station)
            & (df["Date"] == today)
            & (df["FuelType"] == self.fuel_type)
        ]

    # tested
    def get_route_data(self, destination):
        # print(destination,"Station get_route_data input")
        df = DatabaseModel().read("DirectionsAPI")
        # print(df[(df['Origin'] == self.origin) & (df['Destination'] == destination)],"Station get_route_data output")
        return df[(df["Origin"] == self.origin) & (df["Destination"] == destination)]

    # tested
    def predict(self, data, date):
        # print(data,date,"Station predict input")
        for d in data["Response"]["DataItems"]["FuelStationDetails"]["FuelStationList"]:
            for p in d["FuelPriceList"]:
                if p["FuelType"] == self.fuel_type:
                    try:
                        latlon = MapboxDirections.generate_latlon(d["Postcode"])
                    except IndexError:
                        latlon = MapboxDirections.generate_latlon(
                            data["Request"]["DataKeys"]["Postcode"]
                        )
                    try:
                        processor = Processor(
                            d["Brand"],
                            d["Town"],
                            d["County"],
                            d["Postcode"],
                            self.fuel_type,
                            p["LatestRecordedPrice"]["InPence"],
                            data["Request"]["DataKeys"]["Postcode"],
                        )
                        prediction = processor.save()
                        self.update_data(latlon, date, data, d, prediction, p)
                        # print(data,date,"Station predict output")
                    except UnboundLocalError as e:
                        continue


class Journey(Station):
    def __init__(self, origin, fuel_type, destination):
        super().__init__(origin, fuel_type, destination)
        self.route_data = {
            "origin": [],
            "destination": [],
            "lat_origin": [],
            "lat_destination": [],
            "lon_origin": [],
            "lon_destination": [],
            "route_information": [],
        }

    # tested

    def reset_route_data(self):
        self.route_data = {
            "origin": [],
            "destination": [],
            "lat_origin": [],
            "lat_destination": [],
            "lon_origin": [],
            "lon_destination": [],
            "route_information": [],
        }

    # tested

    def save_route(self, closest_coordinate, route_information, k):
        # print(closest_coordinate,route_information,k,"Journey save_route input")
        self.route_data["origin"].append(self.origin)
        self.route_data["destination"].append(self.destination)
        self.route_data["lat_origin"].append(closest_coordinate[k][1])
        self.route_data["lat_destination"].append(closest_coordinate[k + 1][1])
        self.route_data["lon_origin"].append(closest_coordinate[k][0])
        self.route_data["lon_destination"].append(closest_coordinate[k + 1][0])
        self.route_data["route_information"].append(route_information)
        # print(self.route_data,"Journey save_route output")

    # tested

    def get_offroute_data(self, df, df_route, i):
        # print(df,df_route,i,"Journey get_offroute_data input")
        df.to_excel("Test_Journey_get_offroute_data_df.xlsx")
        df_route.to_excel("Test_Journey_get_offroute_data_df_route.xlsx")
        station_lat, station_lon = df["Lat"].iloc[i], df["Lon"].iloc[i]
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
                # print(origin_dict, destination_dict,"calling directions off routes vishal")
                response = MapboxConnection().directions.directions(
                    [origin_dict, destination_dict], "mapbox/driving-traffic"
                )
                driving_route = response.geojson()
                # print(driving_route,"driving_route vishal")
                route_responses.append(driving_route)
                distance_value = driving_route["features"][0]["properties"]["distance"]
                distances.append([distance_value, j])
            except KeyError as e:
                # print(e,"error with downloading direction")
                continue
        # print(distances,route_responses,"Journey get_offroute_data input output")
        return distances, route_responses

    # tested

    def save_station_routes(self, df, df_route):
        # print(df,df_route,"Journey save_station_routes input")
        df.to_excel("Test_Journey_save_station_routes_df.xlsx")
        df_route.to_excel("Test_Journey_save_station_routes_df_route.xlsx")
        off_routes = []
        off_routes_data = []
        for i in range(len(df)):
            distances, route_responses = self.get_offroute_data(df, df_route, i)
            # print(distances,route_responses,"result of get_offroute_data_vishal")
            distances.sort(key=lambda x: x[0])
            closest_coordinate_response = route_responses[distances[0][1]]
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
                + " km, Duration: "
                + str(int(duration_info))
                + " mins"
            )
            data = []
            for k in range(len(closest_coordinate) - 1):
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
                self.save_route(closest_coordinate, route_information, k)
            off_routes_data.append(data)
        FileHelper.save_no_date(
            f"routes-{self.origin}-{self.destination}", off_routes_data
        )
        df = DataFrameHelper.to_dataframe(self.route_data)
        DatabaseModel().save(df, "DirectionsOffRoute")
        self.reset_route_data()
        # print(off_routes,"Journey save_station_routes output")
        return off_routes

    # tested

    def get_station_routes(self, df):
        data = FileHelper.open_no_date(f"routes-{self.origin}-{self.destination}")
        off_routes = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                off_routes.append(
                    UIComponent().render_off_route(
                        data[i][j]["closest_coordinate"],
                        data[i][j]["route_information"],
                        data[i][j]["k"],
                    )
                )
        return off_routes

    # tested

    def map_routes(self, df_route, df):
        # print(df_route,df,"Journey map_routes input")
        df.to_excel("Test_Journey_map_routes_df.xlsx")
        df_route.to_excel("Test_Journey_map_routes_df_route.xlsx")
        routes = []
        route_information = (
            "Distance: "
            + str(int(df_route["Distance-Text"].iloc[0]))
            + " km, Duration: "
            + str(int(df_route["Duration-Text"].iloc[0]))
            + " mins"
        )
        for i in range(len(df_route) - 1):
            routes.append(
                UIComponent().render_journey_route(df_route, route_information, i)
            )
        try:
            off_routes = self.get_station_routes(df)
            if len(off_routes) < 1:
                raise ValueError
        except (ValueError, exc.SQLAlchemyError, FileNotFoundError, IndexError) as e:
            off_routes = self.save_station_routes(df, df_route)
        # print(off_routes,routes,"Journey map_routes output")
        return off_routes, routes

    # tested

    def map(self, df):
        # print(df,"Journey map input")
        df.to_excel("Test_Journey_map_df.xlsx")
        stations_list = super().get_route_data(self.destination)
        off_routes, routes = self.map_routes(stations_list, df)
        df["Information"] = (
            df["Brand"]
            + ", "
            + df["FuelType"]
            + ": "
            + df["Price"].map(str)
            + "p, "
            + df["Post Code"]
        )
        latlon_origin = MapboxDirections.generate_latlon(self.origin)
        latlon_destination = MapboxDirections.generate_latlon(self.destination)
        stations = UIComponent().render_stations(df)
        origin_coordinate = UIComponent().render_origin(
            latlon_origin[1], latlon_origin[0], stations_list["Start-Address"].iloc[0]
        )
        destination_coordinate = UIComponent().render_origin(
            latlon_destination[1],
            latlon_destination[0],
            stations_list["End-Address"].iloc[0],
        )
        # print(stations_list,origin_coordinate,destination_coordinate,routes,off_routes,stations,"mapvishal")
        # print(stations_list,origin_coordinate,destination_coordinate,routes,off_routes,stations,"Journey map output")
        return (
            stations_list,
            origin_coordinate,
            destination_coordinate,
            routes,
            off_routes,
            stations,
        )

    # tested

    def call_api(self, post_codes):
        # print(post_codes,"Journey call_api input")
        batch_data = []
        for post_code in post_codes:
            try:
                data = FileHelper.open(post_code)
                # print(data,"inside call_api journey")
            except FileNotFoundError as e:
                # print(e,"exception raised in call_api journey")
                result = requests.get(
                    f"https://uk1.ukvehicledata.co.uk/api/datapackage/FuelPriceData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_postcode={post_code}"
                )
                data = result.json()
                FileHelper.save(post_code, data)
            try:
                data["Response"]["DataItems"]["FuelStationDetails"]["FuelStationList"][
                    0
                ]
                batch_data.append(data)
            except KeyError as e:
                # print(e)
                pass
        # print(batch_data,"Journey call_api output")
        return batch_data

    # tested

    def save(self, post_codes):
        # print(post_codes,"Journey save input")
        post_codes = self.remove_invalid_post_code(post_codes)
        batch_data = self.call_api(post_codes)
        date = DateHelper.get_today_date()
        for data in batch_data:
            super().predict(data, date)
        df = DataFrameHelper.to_dataframe(self.data)
        super().reset_data()
        if len(df) > 0:
            DatabaseModel().save(df, "stations")
        # print(df,"Journey save output")
        return df

    # tested
    def remove_invalid_post_code(self, post_codes):
        # print(post_codes,"Journey remove_invalid_post_code input")
        for post_code in post_codes:
            if "A" not in post_code:
                post_codes.remove(post_code)
        # print(post_codes,"Journey remove_invalid_post_code output")
        return post_codes


class NearestPump(Station):
    def __init__(self, post_code, fuel_type):
        super().__init__(post_code, fuel_type)
        # self.post_code = post_code
        # self.fuel_type = fuel_type
        # self.data = self.save()

    # tested
    def get_brand_analysis(self, data):
        # print(data,"NearestPump get_brand_analysis input")
        df = DataFrameHelper.to_dataframe(data)
        df = DataFrameHelper.drop_duplicate(df, ["Post Code"])
        total = len(df)
        supermarket = 0
        non_supermarket = 0
        for i in range(len(df)):
            for station in ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]:
                if station in df["Brand"].iloc[i]:
                    supermarket += 1
        non_supermarket = total - supermarket
        # print(supermarket,non_supermarket,"NearestPump get_brand_analysis output")
        return supermarket, non_supermarket

    # tested
    def get_metrics(self, data, slider, radio):
        # print(data,slider,radio,"NearestPump get_metrics input")
        df = DataFrameHelper.to_dataframe(data)
        df = df[df["Distance"] <= slider]
        price_min, price_max = df["Price"].min(), df["Price"].max()
        prediction_min, prediction_max = df["Prediction"].min(), df["Prediction"].max()
        if prediction_max > price_max:
            max = prediction_max
        else:
            max = price_max
        if prediction_min < price_min:
            min = prediction_min
        else:
            min = price_min
        if (radio == "Brand") or (radio == "Post Code"):
            df = DataFrameHelper.sort_columns(df, ["Price", "Prediction"])
        else:
            df = DataFrameHelper.sort_columns(df, ["Distance", "Price", "Prediction"])
        df = df.loc[~df[radio].duplicated(keep="first")]
        # print(df,min,max,"NearestPump get_metrics output")
        return df, min, max

    # tested
    def get_data_analysis(self, rows):
        # print(rows,"NearestPump get_data_analysis input")
        df = DataFrameHelper.to_dataframe(rows)
        brand_today = df[df["Price"] == df["Price"].min()]["Brand"].iloc[0]
        postcode_today = df[df["Price"] == df["Price"].min()]["Post Code"].iloc[0]
        distance_today = df[df["Price"] == df["Price"].min()]["Distance"].iloc[0]
        brand_tomorrow = df[df["Prediction"] == df["Prediction"].min()]["Brand"].iloc[0]
        postcode_tomorrow = df[df["Prediction"] == df["Prediction"].min()][
            "Post Code"
        ].iloc[0]
        distance_tomorrow = df[df["Prediction"] == df["Prediction"].min()][
            "Distance"
        ].iloc[0]
        # print(brand_today,postcode_today,distance_today,brand_tomorrow,postcode_tomorrow,distance_tomorrow,"NearestPump get_data_analysis output")
        return (
            brand_today,
            postcode_today,
            distance_today,
            brand_tomorrow,
            postcode_tomorrow,
            distance_tomorrow,
        )

    # tested
    def get_station_prices(self, hoverData, rows):
        # print(hoverData,rows,"NearestPump get_station_prices input")
        df = DataFrameHelper.to_dataframe(rows)
        try:
            station_post_code = hoverData["points"][0]["customdata"]
        except (KeyError, TypeError, IndexError):
            station_post_code = df[df["Price"] == df["Price"].min()]["Post Code"].iloc[
                0
            ]
        # if hoverData['points'][0]['customdata'] == "" or (hoverData['points'][0]['customdata'] == None):
        #     station_post_code = df[df['Price'] == df['Price'].min()]['Post Code'].iloc[0]
        # else:
        #     station_post_code = hoverData['points'][0]['customdata']
        df = super().get_station_data(station_post_code)
        # df = DataFrameHelper.fetch_postcode_filtered_dataframe(station_post_code, self.fuel_type)
        brand = df.iloc[0]["Brand"]
        prediction = Processor(
            df.iloc[0]["Brand"],
            df.iloc[0]["Town"],
            df.iloc[0]["County"],
            df.iloc[0]["PostCode"],
            df.iloc[0]["FuelType"],
            df.iloc[0]["Price"],
            df.iloc[0]["SearchPostCode"],
        )
        prediction = prediction.save()
        df1, predicted_df = prediction["df"], prediction["prediction"]
        df1.set_index("Date", inplace=True)
        df1.rename(columns={"Price": "Prediction"}, inplace=True)
        df = pd.concat([df1, predicted_df])
        # print(df,brand,station_post_code,"NearestPump get_station_prices output")
        return df, brand, station_post_code

    # tested
    def map_routes(self, stations_list):
        # print(stations_list,"NearestPump map_routes input")
        routes = []
        for idx, station in enumerate(stations_list):
            try:
                df_route = super().get_route_data(station)
                # df_route = DataFrameHelper.fetch_journey_filtered_dataframe(self.origin, station)
                if len(df_route) < 1:
                    raise ValueError
            except (ValueError, exc.SQLAlchemyError) as e:
                # print(e, "MADE MAPBOX DIRECTIONS API CALL")
                try:
                    mapbox = MapboxDirections(self.origin, station)
                    df_route = mapbox.save()
                except IndexError as e:
                    # print(e)
                    mapbox = MapboxDirections(self.origin, stations_list[idx - 1])
                    df_route = mapbox.save()
            route_information = (
                "Distance: "
                + str(int(df_route["Distance-Text"].iloc[0]))
                + " km, Duration: "
                + str(int(df_route["Duration-Text"].iloc[0]))
                + " mins"
            )
            for i in range(len(df_route) - 1):
                routes.append(
                    UIComponent().render_routes(df_route, route_information, i)
                )
        # print(routes,df_route,"NearestPump map_routes output")
        return routes, df_route

    # tested
    def map(self, df):
        # print(df,"NearestPump map input")
        df.to_excel("Test_NearestPump_map_input.xlsx")
        stations_list = (
            df[df["SearchPostCode"] == self.origin]["Post Code"].unique().tolist()
        )
        routes, df_route = self.map_routes(stations_list)
        latlon = MapboxDirections.generate_latlon(self.origin)
        search_lat = latlon[1]
        search_lon = latlon[0]
        df["Information"] = (
            df["Brand"]
            + ", "
            + df["FuelType"]
            + ": "
            + df["Price"].map(str)
            + "p, "
            + df["Post Code"]
        )
        stations = UIComponent().render_stations(df)
        origin_coordinate = UIComponent().render_origin(
            search_lat, search_lon, self.origin
        )
        # print(df_route,origin_coordinate,stations,routes,"NearestPump map output")
        return df_route, origin_coordinate, stations, routes

    # tested
    def save(self):
        data = super().call_api()
        date = DateHelper.get_today_date()
        super().predict(data, date)
        df = DataFrameHelper.to_dataframe(self.data)
        super().reset_data()
        if len(df) > 0:
            DatabaseModel().save(df, "stations")
        # print(df,"NearestPump save output")
        return df


#######################################################INDEX CLASSES#################################
class TextClassificationEngine:
    def __init__(self):
        self.classifier = self.fit()
        # print(self.classifier,"TextClassificationEngine init")

    # tested
    def fit(self):
        cl = NaiveBayesClassifier(text_training_data)
        return cl

    # tested
    def prediction_engine(self, data):
        # print(data,"prediction_engine input textclassifier")
        re = self.classifier.prob_classify(data)
        overall = re.max()
        pos = round(re.prob("pos"), 2)
        neg = round(re.prob("neg"), 2)
        # print(overall, pos, neg,"prediction_engine output textclassifier")
        return overall, pos, neg


class NeuralNetworkEngine:
    # tested
    def __init__(self, epoch, df, horizon, feature, frequency):
        self.epoch = epoch
        self.df = df
        self.horizon = horizon
        self.feature = feature
        self.frequency = frequency
        # print(epoch, df, horizon, feature, frequency,"NeuralNetworkEngine instance variables")

    # tested
    def scale(self):
        length = len(self.df) - self.horizon
        train = self.df.iloc[:length]
        test = self.df.iloc[length:]
        # print(train,test,length,"inputs to scale")
        scaler = MinMaxScaler()
        scaler.fit(train)
        scaled_train = scaler.transform(train)
        scaled_test = scaler.transform(test)
        # print(type(scaler),type(test),type(scaled_train),type(scaled_test),"neural network scale output")
        return scaler, test, scaled_train, scaled_test

    # tested
    def fit(self, scaled_train, scaled_test, n_input, n_features):
        # print(scaled_train,scaled_test,n_input,n_features,"fit input")
        generator = TimeseriesGenerator(
            scaled_train, scaled_train, length=n_input, batch_size=1
        )
        model = Sequential()
        model.add(LSTM(100, activation="relu", input_shape=(n_input, n_features)))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        model.fit_generator(generator, epochs=self.epoch)
        # print(model,"neural network fit output")
        return model

    # def transform(self,scaler,test_predictions):
    #     #print(scaler,test_predictions,"transform input")
    #     data = scaler.inverse_transform(test_predictions)
    #     if self.frequency == "D":
    #         today = datetime.datetime.today()
    #         date_horizon = today - timedelta(days=self.horizon)
    #     elif self.frequency == "M":
    #         date_horizon = date.today() + relativedelta(months=-(self.horizon-1))
    #     idx = pd.date_range(str(date_horizon), periods=self.horizon*2, freq=self.frequency)
    #     cols = [self.feature]
    #     df = pd.DataFrame(data, idx, cols)
    #     #print(df,"transform output")
    #     return df

    # tested
    def transform(self):
        scaler, test, scaled_train, scaled_test = self.scale()
        n_input = self.horizon
        n_features = 1
        model = self.fit(scaled_train, scaled_test, n_input, n_features)
        first_eval_batch = scaled_train[-self.horizon :]
        first_eval_batch = first_eval_batch.reshape((1, n_input, n_features))
        model.predict(first_eval_batch)
        test_predictions = []
        first_eval_batch = scaled_train[-n_input:]
        current_batch = first_eval_batch.reshape((1, n_input, n_features))
        np.append(current_batch[:, 1:, :], [[[99]]], axis=1)
        test_predictions = []
        first_eval_batch = scaled_train[-n_input:]
        current_batch = first_eval_batch.reshape((1, n_input, n_features))
        for i in range(len(test) + self.horizon):
            current_pred = model.predict(current_batch)[0]
            test_predictions.append(current_pred)
            current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
        # print(scaler,test_predictions,"neural network transform output")
        return scaler, test_predictions

    # tested
    def prediction_engine(self):
        scaler, test_predictions = self.transform()
        # print(scaler,test_predictions,"transform input")
        data = scaler.inverse_transform(test_predictions)
        if self.frequency == "D":
            today = datetime.datetime.today()
            date_horizon = today - timedelta(days=self.horizon)
        elif self.frequency == "M":
            date_horizon = date.today() + relativedelta(months=-(self.horizon - 1))
        idx = pd.date_range(
            str(date_horizon), periods=self.horizon * 2, freq=self.frequency
        )
        cols = [self.feature]
        df = pd.DataFrame(data, idx, cols)
        # print(df,"neural network prediction engine output")
        return df


class AggregatePriceModel:
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

    def first_day(self, entry):
        if len(entry):
            # print(entry[0],"first day output")
            return entry[0]

    # tested
    def extract(self):
        if self.region:
            df = pd.read_excel(self.fuel_type, index_col="Date", parse_dates=True)
            df.index.freq = "M"
            df = df[[self.region]].copy()
        elif "supermarket" in self.fuel_type:
            df = pd.read_excel(
                "supermarket-comparison.xlsx", index_col="Date", parse_dates=True
            )
            df = df.resample(rule="1D").interpolate()
            df = df[[f"{self.fuel_type}"]].copy()
        else:
            df = pd.read_excel("daily-updated.xlsx", index_col="Date", parse_dates=True)
            df = df.resample(rule="MS").apply(self.first_day)
            df = df[[self.fuel_type, f"{self.fuel_type}-wholesale"]].copy()
        # print(df,"AggregatePriceModel extract output")
        return df

    # tested
    def predict(self):
        df = self.extract()
        latest_price_df = df.iloc[[-1]]
        if self.region:
            df.to_excel("Test_neural_network_region.xlsx")
            model = NeuralNetworkEngine(5, df, self.horizon, self.region, "M")
            forecast = model.prediction_engine()
            forecast.rename(columns={self.region: "Prediction"}, inplace=True)
            latest_price_df.rename(columns={self.region: "Prediction"}, inplace=True)
        elif "supermarket" in self.fuel_type:
            model = NeuralNetworkEngine(1, df, self.horizon, "Price", "D")
            forecast = model.prediction_engine()
            latest_price_df.rename(
                columns={f"{self.fuel_type}": "Prediction"}, inplace=True
            )
            forecast.rename(columns={"Price": "Prediction"}, inplace=True)
        else:
            model = SarimaEngine(self.fuel_type, self.horizon, df)
            forecast = model.prediction_engine()
            latest_price_df = df[df.index == "2019-06-01"]
            latest_price_df.rename(columns={self.fuel_type: "Prediction"}, inplace=True)
        merged_df = pd.concat([latest_price_df, forecast.iloc[[-1]]])
        # print(merged_df,"AggregatePriceModel predict output")
        return merged_df


class WebScraper:
    # tested
    def __init__(self, url):
        self.url = url
        # print(self.url,"WebScraper init")

    # tested
    def get_html(self, url):
        # print(url,"WebScraper get_html input")
        try:
            with closing(get(url, stream=True)) as response:
                result = BeautifulSoup(response.content, "html.parser")
                # print(result,"WebScraper get_html output")
                return result
        except RequestException as e:
            # print(e)
            return None

    # tested
    def scrape_url(self, links):
        # print(links,"scrape_url input")
        try:
            data = FileHelper.open("rac")
        except FileNotFoundError as e:
            # print(e)
            data = []
            for link in links:
                html = self.get_html(link)
                title = html.find_all("h1", class_="newsroom-headline fn")
                # print(title)
                date = html.find_all("span", class_="material-date")
                content = html.find_all("div", class_="newsroom-article")
                content2 = content[0].find_all("div", class_="markdown clearfix")
                content3 = content2[0].find_all("p")
                sentences = []
                for p in content3:
                    page = p.getText()
                    sentences.append(page)
                sentences = " ".join(sentences)
                data.append(
                    {
                        "title": title[0].text.strip(),
                        "date": date[0].getText(),
                        "content": sentences,
                    }
                )
            FileHelper.save("rac", data)
        # print(data,"scrape_url output")
        return data

    # tested
    def scrape_urls(self):
        try:
            links = FileHelper.open("rac-links")
        except FileNotFoundError as e:
            # print(e)
            html = self.get_html(self.url)
            # print(html,self.url,"html in scrape urls")
            result = html.find_all("a", class_="material")
            links = []
            for r in result:
                links.append(r["href"])
            start = "https://media.rac.co.uk"
            full_link = [start + link for link in links]
            links = rac_links + full_link
            FileHelper.save("rac-links", links)
        result = self.scrape_url(links)
        # print(result,"scarpe_urls output vishal")
        return result

    # tested
    def scrape_predictions(self):
        html = self.get_html("https://www.rac.co.uk/drive/advice/fuel-watch/")
        diesel = (
            html.find_all("div", class_="fuel-type-container first odd")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        petrol = (
            html.find_all("div", class_="fuel-type-container even")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        super_unleaded = (
            html.find_all("div", class_="fuel-type-container odd")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        lpg = (
            html.find_all("div", class_="fuel-type-container last even")[0]
            .find_all("div", class_="movement")[0]
            .text.strip()
        )
        # print(diesel, petrol, super_unleaded, lpg,"scrape_prediction output")
        return diesel, petrol, super_unleaded, lpg


class Text:
    def __init__(self, query_input):
        self.query_input = query_input

    # tested
    def badge_input(self, forecast):
        forecast.to_excel("Text_badget_input_test.xlsx")
        # print(forecast,"Text badge_input")
        if forecast.iloc[1][0] > 0:
            colour = "#008000"
            movement = "down"
        elif forecast.iloc[1][0] < 0:
            colour = "#FF0000"
            movement = "up"
        else:
            colour = "#D3D3D3"
            movement = "No change"
        # print(colour,movement,"Text badget_input output")
        return colour, movement

    # tested
    def update_classifications(self, scores):
        # print(scores,"update_classifications input")
        classifications = []
        dates = []
        for score in scores:
            # print(score[0],"score")
            try:
                date = datetime.datetime.strptime(score[0], "%b %d, %Y").strftime(
                    "%Y-%m-%d"
                )
                # print(date,"date")
            except ValueError:
                date = score[0].split("T")[0]
            dates.append(date)
            if score[2] == "pos":
                classification = 1
            else:
                classification = -1
            classifications.append(classification)
        # print(classifications,dates,"update_classifications output")
        return classifications, dates

    # tested
    def load(self, classifications, dates):
        # print(classifications,dates,"Text load input")
        dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
        oldest = min(dates)
        today = DateHelper.get_today_date()
        # print(dates)
        idx = pd.date_range(str(oldest), periods=len(classifications), freq="M")
        cols = ["Classification"]
        df = pd.DataFrame(classifications, dates, cols)
        df.sort_index(inplace=True)
        # print(df,"Text load output")
        return df


class News(Text):
    def __init__(self, query_input):
        # #print(query_input,"instance of news class vishal")
        super().__init__(query_input)

    # def transform(self,scores):
    #     #print(scores,"news transform input")
    #     classifications,dates = super().update_classifications(scores)
    #     df = super().load(classifications,dates)
    #     df = df.resample(rule='1MS').last().interpolate()
    #     #print(df,"news transform output")
    #     return df

    # tested
    def classify(self, data):
        # #print(data,"news classify input")
        scores = []
        for result in data:
            overall, pos, neg = TextClassificationEngine().prediction_engine(
                result["title"][0]
            )
            scores.append((result["date"], result["title"][0], overall, pos, neg))
        classifications, dates = super().update_classifications(scores)
        df = super().load(classifications, dates)
        df = df.resample(rule="1MS").last().interpolate()
        # #print(df,"news classify ouput")
        return df

    # def predict(self,data):
    #     #print(data,"News predict input")
    #     diesel, petrol, super_unleaded, lpg = WebScraper('https://www.rac.co.uk/drive/advice/fuel-watch/').scrape_predictions()
    #     df = self.classify(data)
    #     model = NeuralNetworkEngine(5, df, 1, "Classification", "M")
    #     forecast = model.prediction_engine()
    #     colour,movement = super().badge_input(forecast)
    #     #print([movement, colour, petrol, diesel, super_unleaded, lpg],"News predict output")
    #     return [movement, colour, petrol, diesel, super_unleaded, lpg]

    # tested
    def query(self):
        web_scraper = WebScraper(self.query_input)
        data = web_scraper.scrape_urls()
        # #print(data,"News predict input")
        diesel, petrol, super_unleaded, lpg = WebScraper(
            "https://www.rac.co.uk/drive/advice/fuel-watch/"
        ).scrape_predictions()
        df = self.classify(data)
        model = NeuralNetworkEngine(5, df, 1, "Classification", "M")
        forecast = model.prediction_engine()
        colour, movement = super().badge_input(forecast)
        # #print([movement, colour, petrol, diesel, super_unleaded, lpg],"News predict output")
        return [movement, colour, petrol, diesel, super_unleaded, lpg]
        # return result


class NaturalLanguage:
    def __init__(self):
        self.version = "2018-03-16"
        self.key = "keVXTae0f2m98zTXKzDD2Nh4rAUTtQ81ncjFRlu-R3Cn"
        self.url = (
            "https://gateway-lon.watsonplatform.net/natural-language-understanding/api"
        )
        self.connection = self.connect()

    def connect(self):
        connection = NaturalLanguageUnderstandingV1(
            version=self.version, url=self.url, iam_apikey=self.key
        )
        # print(connection,"natural language connection output")
        return connection


class SarimaEngine:
    def __init__(self, fuel_type, horizon, df):
        self.fuel_type = fuel_type
        self.horizon = int(horizon)
        self.df = df
        # print(fuel_type,horizon,df,"Sarima init variables")

    def fit(self, df1, df, p, d, q):
        # print(df1,df,p,d,q,"Sarima fit input")
        exog_name = self.fuel_type + "-wholesale"
        model = SARIMAX(
            df1[self.fuel_type],
            exog=df1[exog_name],
            order=(p, d, q),
            enforce_invertibility=False,
        )
        results = model.fit()
        exog_forecast = df[len(df1) :][[exog_name]]
        # print(results,exog_forecast,"Sarima fit output")
        return results, exog_forecast

    def extract(self):
        df1 = self.df.dropna()
        sliced_length = len(df1) + self.horizon
        df = self.df[0:sliced_length]
        (p, d, q) = auto_arima(df1[self.fuel_type]).order
        length = len(df1) - self.horizon
        train = df1.iloc[:length]
        test = df1.iloc[length:]
        # print(df1,df,p,d,q,"Sarima extract output")
        return df1, df, p, d, q

    def transform(self):
        df1, df, p, d, q = self.extract()
        results, exog_forecast = self.fit(df1, df, p, d, q)
        fcast = results.predict(
            len(df1), len(df1) + (self.horizon - 1), exog=exog_forecast
        )
        # print(fcast,"Sarima transform output")
        return fcast

    def prediction_engine(self):
        fcast = self.transform()
        date_horizon = date.today()
        idx = pd.date_range(str(date_horizon), periods=self.horizon, freq="M")
        cols = ["Prediction"]
        df = pd.DataFrame(fcast.values, idx, cols)
        # print(df,"sarima prediction engine output")
        return df


class TwitterConnection:
    def __init__(self):
        self.key = "X9rPqN7KFmze7srVvE51FqaJf"
        self.secret = "E0SbuDIgETvJQicBqoQTn9GtVe3jyJKdJEcXFfCfCGw1mrmljl"
        self.token = "724869065894928385-uUY1B7BxAga8zUv3Ni3M3DLITTQI1Sf"
        self.token_secret = "Hfgm9x91y9GVdTSBaSLpulWCoKa1C5YM1YvAR8IdFLXQ0"
        self.connection = self.connect()
        # #print(self.connection,"variable in __init__ in TwitterConnection")

    # tested
    def connect(self):
        oauth_handler = OAuthHandler(self.key, self.secret)
        oauth_handler.set_access_token(self.token, self.token_secret)
        connection = API(oauth_handler)
        # #print(connection,"connect output")
        return connection


class Sentiment:
    def __init__(self, handles):
        # #print(handles,"input to __init__ in Sentiment")
        self.handles = handles
        # #print(self.handles,"instance variable set in __init__ in Sentiment")

    # tested
    def calculate_sentiment(self, tweet):
        # #print(tweet,"calculate_sentiment input")
        try:
            analysis = (
                NaturalLanguage()
                .connection.analyze(
                    text=tweet, features=Features(sentiment=SentimentOptions())
                )
                .get_result()
            )
            analysis = analysis["sentiment"]["document"]["score"]
            if "save" in tweet:
                analysis = abs(analysis)
        except (
            requests.exceptions.RequestException,
            ibm_cloud_sdk_core.api_exception.ApiException,
        ) as e:
            # print(e)
            analysis = 0
        # #print(analysis,"calculate_sentiment output")
        return analysis

    # tested
    def get_user_timeline(self, handle, api):
        # #print(handle,"get_user_timeline input")
        timeline = api.user_timeline(screen_name=handle, count=5)
        # #print(timeline,"get_user_timeline input output")
        return timeline

    # tested
    def tweet_dataframe_constructor(self, tweets):
        # #print(tweets,"tweet_dataframe_constructor input")
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=["tweets"])
        df["sentiment"] = np.array(
            [self.calculate_sentiment(tweet) for tweet in df["tweets"]]
        )
        df["mean"] = df["sentiment"].mean()
        # #print(df,"tweet_dataframe_constructor output")
        return df

    # tested
    def get_sentiment(self, df):
        # #print(df,"get_sentiment input")
        y_ax = df["mean"].iloc[-1]
        if y_ax == 0.0:
            y_ax = 0.01
        # #print(df,"get_sentiment output")
        return y_ax

    # tested
    def process_twitter_sentiments(self):
        api = TwitterConnection().connection
        traces = []
        for handle in self.handles:
            try:
                tweets = self.get_user_timeline(handle, api)
                df = self.tweet_dataframe_constructor(tweets)
                y_ax = self.get_sentiment(df)
                # tweets = api.user_timeline(screen_name=handle, count=5)
                # df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
                # df['sentiment'] = np.array([self.calculate_sentiment(tweet)
                #                              for tweet in df['tweets']])
                # df['mean'] = df['sentiment'].mean()
                # y_ax = df['mean'].iloc[-1]
                # if y_ax == 0.0:
                #     y_ax = 0.01
                trace = UIComponent().render_twitter_trace(handle, y_ax)
                # trace = go.Bar(x=[handle], y=[y_ax], name=handle)
                traces.append(trace)
            except tweepy.TweepError as e:
                # print(e)
                continue
        # #print(traces,"output of process_twitter_sentiments")
        return traces


class DiscoveryConnection:
    def __init__(self):
        self.version = "2018-08-01"
        self.url = "https://gateway-lon.watsonplatform.net/discovery/api"
        self.key = "AlAAjM1RG99-dBY9I1XIU-V3w4p62cKyzllNjRX4W6pQ"
        self.connection = self.connect()
        self.news_collection = self.news_collection()

    # tested
    def connect(self):
        discovery = DiscoveryV1(version=self.version, url=self.url, iam_apikey=self.key)
        # #print(discovery,"connect discovery")
        return discovery

    # tested
    def news_collection(self):
        environments = self.connection.list_environments().get_result()
        news_environment_id = "system"
        collections = self.connection.list_collections(news_environment_id).get_result()
        news_collections = [x for x in collections["collections"]]
        configurations = self.connection.list_configurations(
            environment_id=news_environment_id
        ).get_result()
        # #print(news_collections,"news_collection vishal")
        return news_collections


class Discovery(Text):
    def __init__(self, query_input):
        super().__init__(query_input)
        self.discovery = DiscoveryConnection()

    # tested
    def parse_data(self, data):
        # #print(data,"parse_data vishal")
        sentences = []
        for relation in data["enriched_text"]["relations"]:
            sentences.append(relation["sentence"])
        sentences = list(set(sentences))
        try:
            country = data["country"]
        except KeyError as e:
            # print(e)
            country = "N/A"
        # #print(sentences,country,"parse_data output")
        return sentences, country

    # tested
    def extract(self, data):
        results = []
        for result in data["results"]:
            sentences, country = self.parse_data(result)
            if country == "GB":
                results.append(
                    {
                        "publication_date": result["publication_date"],
                        "country": country,
                        "text": result["text"],
                        "title": result["title"],
                        "url": result["url"],
                        "relations": sentences,
                    }
                )
        # #print(results,"extract output")
        return results

    # tested
    def transform(self, scores):
        # #print(scores,"transform input")
        classifications, dates = super().update_classifications(scores)
        df = super().load(classifications, dates)
        df1 = (
            df.groupby(df.index)
            .apply(lambda df1: df1.resample("D").mean().interpolate())
            .reset_index(level=0, drop=True)
        )
        df1 = df1.resample(rule="1D").interpolate()
        # #print(df1,"transform output")
        return df1

    # tested
    def save_wordcloud(self, wordcloud):
        FileHelper.save("wordcloud", wordcloud)
        os.system(
            "wordcloud_cli --text wordcloud_text --imagefile assets/wordcloud.png"
        )

    # tested
    def filter_text(self, text):
        relevant_words = ["uk", "price", "fuel"]
        relevant_words_caps = ["UK", "Price", "Fuel"]
        relevant_words_bool = all(word in text for word in relevant_words)
        relevant_words_caps_bool = all(word in text for word in relevant_words_caps)
        return relevant_words_bool, relevant_words_caps_bool

    # tested
    def classify(self, data):
        wordcloud = []
        scores = []
        date = DateHelper.get_today_date()
        for result in self.extract(data):
            title, text, date = (
                [result["title"]],
                [result["text"]],
                result["publication_date"],
            )
            relations = list(set(result["relations"]))
            joined_text = ". ".join(title + text + relations)
            overall, pos, neg = TextClassificationEngine().prediction_engine(
                joined_text
            )
            relevant_words_bool, relevant_words_caps_bool = self.filter_text(
                joined_text
            )
            if relevant_words_bool or relevant_words_caps_bool:
                scores.append((date, text[0], overall, pos, neg))
                wordcloud.append(joined_text)
        df = self.transform(scores)
        self.save_wordcloud(wordcloud)
        # #print(df,"classify output vishal")
        return df

    # #tested
    #     def predict(self,data):
    #         df = self.classify(data)
    #         forecast = NeuralNetworkEngine(1, df, 1, "Classification", "D").prediction_engine()
    #         colour,movement = super().badge_input(forecast)
    #         oldest = str(df.index[0]).split(" ")[0]
    #         latest = str(df.index[-1]).split(" ")[0]
    #         #print(movement, colour, oldest, latest,"predict output")
    #         return movement, colour, oldest, latest

    # tested
    def call_api(self):
        try:
            data = FileHelper.open("discovery")
        except FileNotFoundError as e:
            # #print(e,"discovery query exception")
            data = self.discovery.connection.query(
                "system",
                self.discovery.news_collection[-1]["collection_id"],
                natural_language_query=self.query_input,
                passages=True,
                count=50,
                highlight=True,
                deduplicate=True,
            ).get_result()
            FileHelper.save("discovery", data)
        # #print(data,"call api discovery vishal")
        return data

    # tested
    def query(self):
        data = self.call_api()
        # try:
        #     data = FileHelper.open("discovery")
        # except FileNotFoundError as e:
        #     #print(e,"discovery query exception")
        #     data = self.discovery.connection.query(
        #         'system',
        #         self.discovery.news_collection[-1]['collection_id'],
        #         natural_language_query=self.query_input,
        #         passages=True,
        #         count=50,
        #         highlight=True,
        #         deduplicate=True
        #     ).get_result()
        #     FileHelper.save("discovery", data)
        df = self.classify(data)
        forecast = NeuralNetworkEngine(
            1, df, 1, "Classification", "D"
        ).prediction_engine()
        colour, movement = super().badge_input(forecast)
        oldest = str(df.index[0]).split(" ")[0]
        latest = str(df.index[-1]).split(" ")[0]
        # #print(movement, colour, oldest, latest,"query result")
        return movement, colour, oldest, latest
