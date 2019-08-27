# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Adapted from: Dash State, URL: https://dash.plot.ly/state
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components
# [4] Adapted from: Author:chriddyp, Date:Aug '17, URL:https://community.plot.ly/t/show-hide-radio-and-form-elements-in-a-menu/5227
# [5] Adapted from: https://dash.plot.ly/dash-core-components/button
# [6] Adapted from: Author:alishobeiri, Date:Aug '17, URL:https://community.plot.ly/t/how-to-integrate-google-maps-address-autocompletion-in-dash/5515/2
# [7] Adapted from: https://community.plot.ly/t/prepopulate-a-hidden-div/9120/3
# [8] Source: Dash Multi-page app layout, URL:https://dash.plot.ly/urls
# [9] Adapted from: Dash callbacks, URL: https://dash.plot.ly/getting-started-part-2
# [10] Adapted from: https://dash.plot.ly/sharing-data-between-callbacks
# [11] Adapted from: Dash DataTable, URL: https://dash.plot.ly/datatable/interactivity
# [12] Adapted from: Interactive Visualisations, URL: https://dash.plot.ly/interactive-graphing
# [13] Source: https://dash-bootstrap-components.opensource.faculty.ai/l/components
# [14] Adapted from: https://plot.ly/python/pie-charts/
# [15] Adapted from: https://plot.ly/python/bar-charts/

from app import app
from dash.dependencies import Input, Output, State  # [2]
import dash_html_components as html  # [1]
import dash_core_components as dcc  # [3]


from project.infrastructure.gui_component import UIComponent
from project.station_dashboards.station import Station, NearestStation
from nearest_station_view import (
    jumbotron_app1,
    layout_first_quarter,
    layout_second_quarter,
    layout_third_quarter,
    # layout_fourth_quarter,
    jumbotron_result_app1,
    jumbotron_result2_app1,
    jumbotron_layout_app1,
)
from navbar import navbar
from project.infrastructure.utility import Utility

layout = html.Div([navbar, jumbotron_app1, html.Div(id="layout")])  # [1] [2] [8]


@app.callback(
    Output("data-table-analytics", "children"),
    [
        Input("table", "derived_virtual_data"),
        Input("table", "derived_virtual_selected_rows"),
        Input("autocompleteInput-nearest", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11]
def render_map_card2(rows, derived_virtual_selected_rows, post_code, fuel_type):
    data = Utility.to_dataframe(rows)
    station = NearestStation(post_code, fuel_type)

    data = station.generate_map_data(data)
    print(data, "render_map_card processing output")
    return UIComponent().render_nearest_map(
        data["df_route"], data["origin_coordinate"], data["stations"], data["routes"]
    )


@app.callback(
    Output("dropdown-nearest", "options"),
    [Input("submit-post-code-button", "n_clicks")],
    [State("autocompleteInput-nearest", "value")],
)  # [2] [6] [9] [10]
def createNewOptions(n_clicks, value):
    return Station.address(value)


@app.callback(
    Output("autocompleteInput-nearest", "value"), [Input("dropdown-nearest", "value")]
)  # [2] [6] [9] [10]
def resetInput(value):
    return value


@app.callback(
    Output("data-table", "children"),
    [
        Input("submit-button", "n_clicks"),
        Input("autocompleteInput-nearest", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10]
def render_data_table(n_clicks, post_code, fuel_type):
    post_code = Utility.to_uppercase(post_code)
    station = NearestStation(post_code, fuel_type)
    stations = station.get_stations()
    table = Station(post_code, fuel_type).update_table(stations)
    return UIComponent().data_table_card(table["df1"], table["df"])


@app.callback(
    [Output("api-result", "children"), Output("layout", "children")],
    [Input("submit-button", "n_clicks")],
    [State("autocompleteInput-nearest", "value"), State("fuel_type", "value")],
)  # [2] [9] [10]
def render_search_result(n_clicks, post_code, fuel_type):
    if n_clicks > 0:
        if (post_code is None) and (fuel_type is None):
            return UIComponent().incorrect_inputs_alert(), ""
        if post_code is None:
            return UIComponent().incorrect_post_code_alert(), ""
        if fuel_type is None:
            return UIComponent().incorrect_fuel_type_alert(), ""
        if (post_code is not None) and (fuel_type is not None):
            if ("A" not in post_code) or (len(post_code) > 8):
                return UIComponent().invalid_post_code(), ""
            try:
                response = NearestStation(post_code, fuel_type).get_stations()
            except (KeyError, TypeError) as e:
                return UIComponent().no_data(post_code, fuel_type), ""
            if len(response) < 1:
                return UIComponent().no_results(post_code, fuel_type), ""
            components = [
                layout_first_quarter,
                layout_second_quarter,
                layout_third_quarter,
            ]
            return UIComponent().search_alerts(response, post_code), components
    return "", ""


@app.callback(
    Output("jumbotron_result_app1", "children"),
    [
        Input("submit-button", "n_clicks"),
        Input("fuel_type", "value"),
        Input("autocompleteInput-nearest", "value"),
    ],
)  # [2] [9] [10]
def update_figure_result(n_clicks, fuel_type, post_code):
    if n_clicks > 0:
        return jumbotron_result_app1


@app.callback(
    Output("jumbotron_result2_app1", "children"),
    [
        Input("submit-button", "n_clicks"),
        Input("fuel_type", "value"),
        Input("autocompleteInput-nearest", "value"),
    ],
)  # [2] [9] [10]
def update_figure_result2(n_clicks, fuel_type, post_code):
    if n_clicks > 0:
        return jumbotron_result2_app1


@app.callback(
    Output("jumbotron_layout_app1", "children"),
    [
        Input("submit-button", "n_clicks"),
        Input("fuel_type", "value"),
        Input("autocompleteInput-nearest", "value"),
    ],
)  # [2] [9] [10]
def update_figure_layout(n_clicks, fuel_type, post_code):
    if n_clicks > 0:
        return jumbotron_layout_app1


@app.callback(
    Output("alert-fade", "is_open"),
    [Input("alert-toggle-fade", "n_clicks")],
    [State("alert-fade", "is_open")],
)  # [13]
def toggle_alert(n, is_open):  # [13]
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("station-details", "children"),
    [
        Input("data-table-analytics", "clickData"),
        Input("autocompleteInput-nearest", "value"),
        Input("table", "derived_virtual_data"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11] [12]
def render_station_details(hoverData, post_code, rows, fuel_type):
    station = NearestStation(post_code, fuel_type)
    ts = station.generate_station_timeseries(hoverData, rows)
    return UIComponent().station_scatter_line(
        ts["df"], ts["brand"], ts["station_post_code"]
    )


@app.callback(
    Output("summary_cards", "children"),
    [
        Input("table", "derived_virtual_data"),
        Input("table", "derived_virtual_selected_rows"),
        Input("autocompleteInput-nearest", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11]
def render_summary_cards(rows, derived_virtual_selected_rows, post_code, fuel_type):
    station = NearestStation(post_code, fuel_type)
    data = station.generate_search_analysis(rows)
    brand_today = UIComponent().card_detail(
        "Cheapest Petrol Station - Today", data["brand_today"]
    )
    brand_tomorrow = UIComponent().card_detail(
        "Cheapest Petrol Station - Tomorrow", data["brand_tomorrow"]
    )
    postcode_today = UIComponent().card_detail(
        "Cheapest Petrol Station Postcode - Today", data["postcode_today"]
    )
    postcode_tomorrow = UIComponent().card_detail(
        "Cheapest Petrol Station Postcode - Tomorrow", data["postcode_tomorrow"]
    )
    distance_today = UIComponent().card_detail(
        "Cheapest Petrol Station Distance (miles)- Today", data["distance_today"]
    )
    distance_tomorrow = UIComponent().card_detail(
        "Cheapest Petrol Station Distance (miles)- Tomorrow", data["distance_tomorrow"]
    )
    data = [
        brand_today,
        brand_tomorrow,
        postcode_today,
        postcode_tomorrow,
        distance_today,
        distance_tomorrow,
    ]
    return UIComponent().cards_layout(3, 2, ["primary", "secondary", "info"], data)


@app.callback(
    Output("app1-pie-chart", "children"),
    [
        Input("table", "derived_virtual_data"),
        Input("table", "derived_virtual_selected_rows"),
        Input("autocompleteInput-nearest", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11] [14]
def render_pie_chart(rows, derived_virtual_selected_rows, post_code, fuel_type):
    station = NearestStation(post_code, fuel_type)
    data = station.generate_brand_analysis(rows)
    return UIComponent().nearest_pie(data["supermarket"], data["non_supermarket"])


@app.callback(
    Output("brand-prices", "children"),
    [
        Input("table", "derived_virtual_data"),
        Input("table", "derived_virtual_selected_rows"),
        Input("radio-metrics", "value"),
        Input("slider-metrics", "value"),
        Input("autocompleteInput-nearest", "value"),
        Input("fuel_type", "value"),
    ],
)  # [2] [9] [10] [11] [15]
def render_bar_chart(
    rows, derived_virtual_selected_rows, radio, slider, post_code, fuel_type
):
    station = NearestStation(post_code, fuel_type)
    data = station.generate_metrics(rows, slider, radio)
    trace1 = UIComponent().bar_trace(data["df"], radio, "Price")
    trace2 = UIComponent().bar_trace(data["df"], radio, "Prediction")
    return UIComponent().nearest_pump_bar(trace1, trace2, data["min"], data["max"])
