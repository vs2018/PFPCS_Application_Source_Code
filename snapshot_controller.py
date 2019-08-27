# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Adapted from: Dash State, URL: https://dash.plot.ly/state
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components
# [4] Adapted from: Dash callbacks, URL: https://dash.plot.ly/getting-started-part-2
# [5] Adapted from: "Dash Sharing State Between Callbacks",URL:https://dash.plot.ly/sharing-data-between-callbacks
# [6] Source: Dash Multi-page app layout, URL:https://dash.plot.ly/urls
# [7] Source: https://community.plot.ly/t/announcing-dash-dev-tools/22481


from app import app

import journey_saver_controller
import nearest_station_controller
from navbar import navbar
from snapshot_view import jumbotron_homepage
from project.snapshot_dashboard.average_price import AveragePrice
from project.infrastructure.gui_component import UIComponent
from project.snapshot_dashboard.sentiment import Sentiment

import dash_core_components as dcc  # [3]
import dash_html_components as html  # [1]
from dash.dependencies import Input, Output, State  # [2]


@app.callback(
    Output("live-update-graph2", "figure"), [Input("timeline-dropdown", "value")]
)  # [2] [4] [5]
def render_twitter_bar_chart(handles):
    sentiment_engine = Sentiment(handles)
    sentiment_dataframe = sentiment_engine.process_sentiment()
    timeline_chart = UIComponent().bar_chart(sentiment_dataframe)
    return timeline_chart


@app.callback(
    Output("supermarket-output", "children"),
    [Input("submit-button-supermarket", "n_clicks")],
    [
        State("supermarket-dropdown", "value"),
        State("prediction_range_supermarket", "value"),
    ],
)  # [2] [4] [5]
def render_uk_averages(n_clicks, fuel_type, horizon):
    if n_clicks > 0:
        model = AveragePrice(fuel_type, horizon)
        df = model.get_prediction()
        return UIComponent().scatter_line(df, fuel_type)


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)  # [6]

layout_index = html.Div([navbar, jumbotron_homepage])  # [6]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])  # [6]
def display_page(pathname):  # [6]
    if pathname == "/nearest-station": # [6]
        return nearest_station_controller.layout # [6]
    elif pathname == "/journey-saver": # [6]
        return journey_saver_controller.layout # [6]
    else:
        return layout_index # [6]


if __name__ == "__main__":  # [6]
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)  # [7]
