# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Adapted from: Dash State, URL: https://dash.plot.ly/state
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components
# [4] Adapted from: Author:chriddyp, Date:Aug '17, URL:https://community.plot.ly/t/show-hide-radio-and-form-elements-in-a-menu/5227
# [5] Adapted from: https://dash.plot.ly/dash-core-components/button
# [6] Adapted from: Author:alishobeiri, Date:Aug '17, URL:https://community.plot.ly/t/how-to-integrate-google-maps-address-autocompletion-in-dash/5515/2
# [7] Adapted from: Author: kritho, Date: Mar '18, URL: https://community.plot.ly/t/prepopulate-a-hidden-div/9120/3
# [8] Source: Dash Multi-page app layout, URL:https://dash.plot.ly/urls
# [9] Adapted from: Dash callbacks, URL: https://dash.plot.ly/getting-started-part-2
# [10] Adapted from: https://dash.plot.ly/sharing-data-between-callbacks
# [11] Adapted from: Dash DataTable, URL: https://dash.plot.ly/datatable/interactivity
# [12] Adapted from: Interactive Visualisations, URL: https://dash.plot.ly/interactive-graphing


import dash_html_components as html  # [1]
from dash.dependencies import Input, Output, State  # [2]
from app import app
import dash_core_components as dcc  # [3]
from project.station_dashboards.station import Station, JourneyStation
from project.station_dashboards.vehicle import Vehicle
from journey_saver_view import *
from navbar import navbar
from project.infrastructure.utility import Utility
from project.infrastructure.gui_component import UIComponent

layout = html.Div(
    [
        html.Button(
            id="submit-button", n_clicks=0, children="Submit", style={"display": "none"}
        ),  # [1] [2] [4] [5] [7] [10]
        navbar,
        jumbotron_app2,
        html.Div(id="journey-layout"),  # [1] [2]
    ]
)  # [1] [2] [8]


@app.callback(
    Output("dropdown-origin", "options"),
    [Input("submit-origin-button", "n_clicks")],
    [State("autocompleteInput-origin", "value")],
)  # [2] [6] [9] [10]
def createNewOptions_origin(n_clicks, value):
    address = Station.address(value)
    return address


@app.callback(
    Output("autocompleteInput-origin", "value"), [Input("dropdown-origin", "value")]
)  # [2] [6] [9] [10]
def resetInput_origin(value):
    return value


@app.callback(
    Output("dropdown-destination", "options"),
    [Input("submit-destination-button", "n_clicks")],
    [State("autocompleteInput-destination", "value")],
)  # [2]  [6] [9] [10]
def createNewOptions_destination(n_clicks, value):
    address = Station.address(value)
    return address


@app.callback(
    Output("autocompleteInput-destination", "value"),
    [Input("dropdown-destination", "value")],
)  # [2]  [6] [9] [10]
def resetInput_destination(value):
    return value


@app.callback(
    Output("input-form-final", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_final_form_input(n_clicks, registration):
    if n_clicks > 0:

        if "A" not in registration:
            return UIComponent().incorrect_registration_alert()
        response = Vehicle(registration).data
        if response["Response"]["StatusCode"] == "Success":
            return inline_radioitems


@app.callback(
    Output("post-code-inputs", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_post_code_inputs(n_clicks, registration):

    return post_code_inputs


@app.callback(
    Output("tank-knob", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_tank_dial(n_clicks, registration):
    capacity = Vehicle(registration).get_tank_capacity()
    return UIComponent().fuel_knob(capacity)


@app.callback(
    Output("fuel_type", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_fuel_type(n_clicks, registration):
    fuel = Vehicle(registration).get_fuel_type()
    if fuel == "DIESEL" or fuel == "Diesel":
        return UIComponent().fuel_radio_items(
            [
                {"label": "Diesel", "value": "Diesel"},
                {"label": "Premium Diesel", "value": "Premium Diesel"},
            ]
        )

    else:
        return UIComponent().fuel_radio_items(
            [
                {"label": "Unleaded", "value": "Unleaded"},
                {"label": "Super Unleaded", "value": "Super Unleaded"},
            ]
        )


@app.callback(
    Output("render-car", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_car_details(n_clicks, registration):
    if n_clicks > 0:
        try:
            vehicle = Vehicle(registration)
            spec = vehicle.get_spec()
            return UIComponent().car_card(
                registration,
                spec["model"],
                spec["fuel"],
                spec["capacity"],
                spec["highway"],
                spec["city"],
                spec["combined"],
            )
        except TypeError:
            return ""


@app.callback(
    Output("search-price-button", "children"),
    [Input("submit-button-registration", "n_clicks")],
    [State("registration", "value")],
)  # [2] [9] [10]
def render_search_price_button(n_clicks, registration):
    return UIComponent().search_price_button()


@app.callback(
    [Output("tank-analysis", "children"), Output("journey-layout", "children")],
    [Input("submit-button", "n_clicks")],
    [State("registration", "value"), State("knob", "value")],
)  # [2] [9] [10]
def render_tank_analysis(n_clicks, registration, tank):
    if n_clicks > 0:
        analysis = Vehicle(registration).tank_analysis(tank)
        highway = UIComponent().card_detail(
            "Highway Mileage", analysis["highway_commentary"]
        )
        city = UIComponent().card_detail("City Mileage", analysis["city_commentary"])
        combined = UIComponent().card_detail(
            "Combined Mileage", analysis["combined_commentary"]
        )
        analysis = UIComponent().card_detail("Fuel Tank", analysis["fuel_analysis"])
        data = [highway, city, combined, analysis]

        return UIComponent().cards_layout(1, 4, ["dark"], data), jumbotron_result
    return "", ""


@app.callback(
    [Output("journey-search-alert", "children"), Output("table-card", "children")],
    [Input("submit-button", "n_clicks"), Input("tank-analysis", "children")],
    [
        State("autocompleteInput-origin", "value"),
        State("autocompleteInput-destination", "value"),
        State("fuel_type", "value"),
        State("registration", "value"),
        State("knob", "value"),
    ],
)  # [2] [9] [10]
def render_journey_result(
    n_clicks, analysis, origin, destination, fuel_type, registration, tank
):
    if n_clicks > 0 and (analysis != ""):
        if (origin == "") and (destination == ""):
            return UIComponent().incorrect_journey_input_alert(), ""
        if origin == "":
            return UIComponent().incorrect_origin_alert(), ""
        if destination == "":
            return UIComponent().incorrect_destination_alert(), ""
        if ("A" not in origin) or (len(origin) > 8):
            return UIComponent().invalid_origin(), ""
        if ("A" not in destination) or (len(destination) > 8):
            return UIComponent().invalid_destination(), ""
        try:
            station = JourneyStation(origin, fuel_type, destination)
            df = station.get_journey_data()
            table = Station(origin, fuel_type, destination).update_table(df)
        except (KeyError, TypeError, IndexError) as e:
            return UIComponent().no_journey_data(origin, destination), ""
        if len(table) < 1:
            return UIComponent().no_journey_results(origin, destination), ""
        return (
            UIComponent().search_journey_alerts(table["df1"], origin, destination),
            UIComponent().data_table_card(table["df1"], table["df"]),
        )
    return "", ""


@app.callback(
    Output("map-card", "children"),
    [
        Input("table", "derived_virtual_data"),
        Input("autocompleteInput-origin", "value"),
        Input("autocompleteInput-destination", "value"),
        Input("table", "derived_virtual_selected_rows"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11]
def update_journey_map(
    rows, origin, destination, derived_virtual_selected_rows, fuel_type
):

    df = Utility.to_dataframe(rows)
    station = JourneyStation(origin, fuel_type, destination)
    data = station.generate_map_data(df)
    return UIComponent().render_journey_map(
        data["stations_list"],
        data["origin_coordinate"],
        data["destination_coordinate"],
        data["routes"],
        data["off_routes"],
        data["stations"],
    )


@app.callback(
    Output("analysis-card", "children"),
    [
        Input("data-table-analytics2", "clickData"),
        Input("autocompleteInput-origin", "value"),
        Input("autocompleteInput-destination", "value"),
        Input("registration", "value"),
        Input("knob", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [12]
def render_journey_analysis(
    hoverData, origin, destination, registration, tank, fuel_type
):
    if hoverData["points"][0]["customdata"] == "":
        return ""
    vehicle = Vehicle(registration)
    analysis = vehicle.analysis(hoverData, origin, destination, tank, fuel_type)

    distance = UIComponent().card_detail(
        "Fuel cost to drive to petrol station", analysis["distance"]
    )
    cost = UIComponent().card_detail("Cost to fill up tank", analysis["cost"])
    difference = UIComponent().card_detail(
        "Fuel Price Comparison", analysis["difference"]
    )
    loss = UIComponent().card_detail(
        "Money lost by buying fuel at this petrol station", analysis["loss"]
    )
    saving = UIComponent().card_detail("Annual Saving", analysis["saving"])
    day = UIComponent().card_detail("Savings by buying fuel tomorrow", analysis["day"])

    data = [distance, difference, loss, day, saving, cost]

    return UIComponent().cards_layout(2, 3, ["primary", "secondary", "info"], data)
