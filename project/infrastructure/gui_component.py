# [1] Plotly library - Graph Object to create interactive graphs, URL: https://plot.ly/python/reference/
# [2] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components
# [3] Dash DataTable library to create an interactive table, URL: https://dash.plot.ly/datatable
# [4] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [5] Dash Bootstrap Components library to write bootstrap components, URL: https://dash-bootstrap-components.opensource.faculty.ai/
# [6] Dash DAQ component to create an interactive fuel tank meter, URL: https://dash.plot.ly/dash-daq
# [7] Mapbox access token to create an interactive map (scattermapbox), URL: https://www.mapbox.com/
# [8] Adapted from: https://plot.ly/python/bar-charts/
# [9] Adapted from: https://plot.ly/python/scattermapbox/
# [10] Adapted from: Author: Guillaume, Date: Jun 25 '18 at 20:03, URL: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# [11] Adapted from: https://plot.ly/python/creating-and-updating-figures/
# [12] Adapted from: https://dash.plot.ly/dash-core-components/graph
# [13] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/card
# [14] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/badge
# [15] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/button
# [16] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/form
# [17] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/input
# [18] Adapted from: https://dash.plot.ly/interactive-graphing
# [19] Adapted from: https://plot.ly/python/pie-charts/
# [20] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# [21] Adapted from: https://plot.ly/python/line-and-scatter/
# [22] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/alert
# [23] Adapted from: Author: Gaurav, Date: Apr 30 '18 at 17:07, URL: https://stackoverflow.com/questions/15741759/find-maximum-value-of-a-column-and-return-the-corresponding-row-values-using-pan
# [24] Adapted from: https://dash.plot.ly/datatable/interactivity

import plotly.graph_objs as go  # [1]
import dash_core_components as dcc  # [2]
import dash_table  # [3]
import dash_html_components as html  # [4]
import dash_bootstrap_components as dbc  # [5]
import dash_daq as daq  # [6]

mapbox_access_token = "pk.eyJ1IjoidnMyMDE5IiwiYSI6ImNqd29ydWh5cDFkajQ0NG9sc3FwbGtyY2IifQ.H9Y11sNtzZ1bOAzgu_mnVA"  # [7]


class UIComponent:
    @classmethod
    def render_twitter_trace(cls, handle, y_ax):  # [8]
        return go.Bar(x=[handle], y=[y_ax], name=handle)

    @classmethod
    def render_routes(cls, df_route, route_information, i):  # [9]
        return go.Scattermapbox(
            lat=[df_route["Lat"].iloc[i], df_route["Lat"].iloc[i + 1]],  # [10]
            lon=[df_route["Lng"].iloc[i], df_route["Lng"].iloc[i + 1]],  # [10]
            mode="lines",
            text=route_information,
        )

    @classmethod
    def render_journey_route(cls, df_route, route_information, i):  # [9]
        return go.Scattermapbox(
            lat=[df_route["Lat"].iloc[i], df_route["Lat"].iloc[i + 1]],  # [10]
            lon=[df_route["Lng"].iloc[i], df_route["Lng"].iloc[i + 1]],  # [10]
            mode="lines",
            text=route_information,
            marker={"size": 10, "color": "black"},
        )

    @classmethod
    def render_stations(cls, df):  # [9]
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
    def render_station_route(cls, df):  # [9]
        return go.Scattermapbox(
            lat=[df["lat_origin"].iloc[k], df["lat_destination"].iloc[k]],  # [10]
            lon=[df["lon_origin"].iloc[k], df["lon_destination"].iloc[k]],  # [10]
            mode="lines",
            text=df["route_information"].iloc[k],  # [10]
            marker={"size": 3},
        )

    @classmethod
    def render_off_route(cls, closest_coordinate, route_information, k):  # [9]
        return go.Scattermapbox(
            lat=[closest_coordinate[k][1], closest_coordinate[k + 1][1]],  # [10]
            lon=[closest_coordinate[k][0], closest_coordinate[k + 1][0]],  # [10]
            mode="lines",
            text=route_information,
            marker={"size": 3},
        )

    @classmethod
    def render_origin(cls, search_lat, search_lon, post_code):  # [9]
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
        fig = go.Figure(data=search_code + stations + routes, layout=layout)  # [11]
        graph = dcc.Graph(
            id="data-table-analytics",
            figure=fig,
            hoverData={"points": [{"customdata": ""}]},
        )  # [12]
        return graph

    @classmethod
    def render_journey_map(
        cls, df_route, origin_plot, destination_plot, routes, off_routes, stations
    ):
        layout = cls.render_layout(df_route)
        fig = go.Figure(
            data=origin_plot + destination_plot + routes + off_routes + stations,
            layout=layout,
        )  # [11]
        graph = dcc.Graph(
            id="data-table-analytics2",
            figure=fig,
            hoverData={"points": [{"customdata": ""}]},
        )  # [12]
        card_content = [
            dbc.CardHeader(
                html.H5(
                    "Map - Journey Route (Black Line) and Routes to each Petrol Station",
                    className="card-title",
                )
            ),
            dbc.CardBody(graph),
        ]  # [13]
        return [dbc.Card(card_content, color="dark", outline=True)]  # [13]

    @classmethod
    def render_layout(cls, df_route):  # [9]
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
    def discovery(cls, data):  # [14]
        movement = cls.badge(data["movement"])
        return {
            "movement": movement,
            "oldest": data["oldest"],
            "latest": data["latest"],
        }

    @classmethod
    def badge(cls, data):  # [14]
        if "down" in data:
            movement = dbc.Badge(data, color="success")
        elif "No change" in data:
            movement = dbc.Badge(data, color="primary")
        else:
            movement = dbc.Badge(data, color="danger")
        return movement

    @classmethod
    def rac(cls, data):  # [14]
        overall = cls.badge(data["movement"])
        unleaded = cls.badge(data["petrol"])
        diesel = cls.badge(data["diesel"])
        super_unleaded = cls.badge(data["super_unleaded"])
        lpg = cls.badge(data["lpg"])
        return {
            "overall": overall,
            "unleaded": unleaded,
            "diesel": diesel,
            "super_unleaded": super_unleaded,
            "lpg": lpg,
        }

    @classmethod
    def search_price_button(cls):  # [15]
        return dbc.Button(
            children="Search Fuel Prices",
            color="primary",
            id="submit-button",
            n_clicks=0,
            size="lg",
        )

    @classmethod
    def fuel_knob(cls, capacity):  # [16]
        return dbc.FormGroup(
            [
                dbc.Label("Select Current Fuel Level"),
                daq.Knob(
                    label="Fuel Tank Meter (Litres)",
                    id="knob",
                    max=capacity,
                    scale={"start": 0, "labelInterval": 5, "interval": 1},
                    value="10",
                ),  # [6]
            ]
        )

    @classmethod
    def fuel_radio_items(cls, options_list):  # [16]
        return dbc.FormGroup(
            [
                dbc.Label("Select Fuel Grade"),
                dbc.RadioItems(
                    options=options_list, inline=True, id="fuel_type", value="Unleaded"
                ),  # [17]
            ]
        )

    @classmethod
    def car_card(
        cls, registration, model, fuel, tank, highway, city, combined
    ):  # [13] [4]
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
    def nearest_pump_bar(cls, trace1, trace2, min, max):  # [18]
        return dcc.Graph(
            figure={
                "data": [trace1, trace2],
                "layout": go.Layout(
                    title=f"Petrol Stations",
                    colorway=["#EF963B", "#EF533B"],
                    hovermode="closest",
                    xaxis={
                        "title": "Selected Metric",
                        "titlefont": {"color": "black", "size": 14},
                        "tickfont": {"size": 9, "color": "black"},
                    },
                    yaxis={
                        "title": "Price (pence)",
                        "titlefont": {"color": "black", "size": 14},
                        "tickfont": {"color": "black"},
                        "range": [min - 5, max + 5],
                    },
                ),  # [11]
            }
        )

    @classmethod
    def bar_trace(cls, df, x, y):  # [8]
        return go.Bar(x=df[x], y=df[y], name=y)

    @classmethod
    def nearest_pie(cls, supermarket, non_supermarket):  # [18]
        return dcc.Graph(
            figure={
                "data": [
                    go.Pie(
                        labels=["Supermarket", "Non-Supermarket"],
                        values=[supermarket, non_supermarket],
                        marker={"colors": ["#FEBFB3", "#96D38C"]},
                        textinfo="label",
                    )  # [19]
                ],
                "layout": go.Layout(),
            }
        )

    @classmethod
    def card_detail(cls, title, body):  # [13]
        return [
            dbc.CardHeader(html.H5(title, className="card-title")),
            dbc.CardBody([html.P(body, className="card-text")]),
        ]

    @classmethod
    def map_card(cls, title, map):  # [13]
        card_content = [
            dbc.CardHeader(html.H5(title, className="card-title")),
            dbc.CardBody(map),
        ]
        return [dbc.Card(card_content, color="dark", outline=True, className="mx-0")]

    @classmethod
    def cards_layout(cls, n_rows, n_cols, colors, data):  # [20]
        result = []
        data_counter = 0
        for row in range(n_rows):
            row_data = []
            for col in range(n_cols):

                card = dbc.Col(
                    dbc.Card(
                        data[data_counter], color=colors[row], inverse=True
                    )  # [13]
                )
                data_counter += 1
                row_data.append(card)
            result.append(dbc.Row(row_data, className="mb-4"))
        return result

    @classmethod
    def station_scatter_line(cls, df, brand, post_code):  # [18]
        return dcc.Graph(
            figure={
                "data": [
                    go.Scatter(
                        x=df.index, y=df["Prediction"], mode="lines+markers"
                    )  # [21]
                ],
                "layout": {
                    "title": f"Fuel Price for {brand} at {post_code}",
                    "height": 225,
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
                    "yaxis": {"title": "Price (pence)", "type": "linear"},
                    "xaxis": {"title": "Date (2019)", "showgrid": False},
                },
            }
        )

    @classmethod
    def incorrect_inputs_alert(cls):  # [22]
        return dbc.Alert("Fuel Type and Post Code not entered", color="warning")

    @classmethod
    def incorrect_post_code_alert(cls):  # [22]
        return dbc.Alert("Post Code not entered", color="warning")

    @classmethod
    def incorrect_origin_alert(cls):  # [22]
        return dbc.Alert("Origin not entered", color="warning")

    @classmethod
    def incorrect_destination_alert(cls):  # [22]
        return dbc.Alert("Destination not entered", color="warning")

    @classmethod
    def incorrect_fuel_type_alert(cls):  # [22]
        return dbc.Alert("Fuel Type not selected", color="warning")

    @classmethod
    def incorrect_journey_input_alert(cls):  # [22]
        return dbc.Alert(
            "Origin and Destination post code not entered", color="warning"
        )

    @classmethod
    def incorrect_registration_alert(cls):  # [22]
        return dbc.Alert(
            "Invalid registration number. It needs to contain an 'A'", color="warning"
        )

    @classmethod
    def invalid_post_code(cls):  # [22]
        return dbc.Alert(
            "Invalid Post Code. The Post Code needs to include the letter A",
            color="danger",
        )

    @classmethod
    def invalid_origin(cls):  # [22]
        return dbc.Alert(
            "Invalid Origin post code. The post code needs to include the letter A",
            color="danger",
        )

    @classmethod
    def invalid_destination(cls):  # [22]
        return dbc.Alert(
            "Invalid Destination post code. The post code needs to include the letter A",
            color="danger",
        )

    @classmethod
    def success(cls):  # [22]
        return dbc.Alert(
            "Success - API data found for this origin and destination", color="danger"
        )

    @classmethod
    def failure(cls):  # [22]
        return dbc.Alert(
            "Failure - API data not found for this origin and destination",
            color="danger",
        )

    @classmethod
    def no_results(cls, post_code, fuel_type):  # [22]
        return dbc.Alert(
            f"There are no stations in the {post_code} area that supply {fuel_type}",
            color="danger",
        )

    @classmethod
    def no_journey_results(cls, origin, destination):  # [22]
        return dbc.Alert(
            f"There are no stations on this journe route with origin {origin} and {destination}",
            color="danger",
        )

    @classmethod
    def no_data(cls, post_code, fuel_type):  # [22]
        return dbc.Alert(
            f"We do not hold data for fuel stations in the {post_code} area",
            color="danger",
        )

    @classmethod
    def no_journey_data(cls, origin, destination):  # [22]
        return dbc.Alert(
            f"We do not hold data for fuel stations on this journey with origin {origin} and destiantion {destination}",
            color="danger",
        )

    @classmethod
    def search_journey_alerts(cls, df, origin, destination):  # [22]
        return (
            dbc.Alert(
                f"Success: {len(df)} petrol stations found along your journey route with origin {origin} and destination {destination}",
                color="primary",
            ),
        )

    @classmethod
    def search_alerts(cls, df, post_code):  # [4]
        range_today = df["Price"].max() - df["Price"].min()  # [23]
        range_tomorrow = (
            df["1-Day Price Prediction"].max() - df["1-Day Price Prediction"].min()
        )  # [23]
        alert = html.Div(
            [
                dbc.Alert(
                    f"Success: {df['PostCode'].count()} petrol stations found in {post_code}",
                    color="primary",
                ),  # [22]
                html.Hr(),
                dbc.Button(
                    "Summary Statistics", id="alert-toggle-fade", className="mr-1"
                ),
                html.Hr(),
                dbc.Alert(
                    [
                        html.P(f"Today's Min Price: {round(df['Price'].min(),1)}p"),
                        html.P(
                            f"Tomorrow's Min Price: {round(df['1-Day Price Prediction'].min(),1)}p"
                        ),
                        html.P(f"Today's Price Range: {round(range_today,1)}p"),
                        html.P(f"Tomorrow's Price Range: {round(range_tomorrow,1)}p"),
                    ],
                    id="alert-fade",
                    dismissable=True,
                    is_open=True,
                ),  # [22]
            ]
        )
        return alert

    @classmethod
    def data_table_card(cls, df1, df):  # [24]
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
                "textAlign": "center",
                "padding": "5px",
            },
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
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
            dbc.CardHeader(
                html.H5(
                    "Petrol Station Fuel Prices - Current and Tomorrow's Predicted Prices",
                    className="card-title",
                )
            ),
            dbc.CardBody(table),
        ]  # [13]
        return [dbc.Card(card_content, color="dark", outline=True)]  # [13]

    @classmethod
    def scatter_line(cls, df, title):  # [18]
        plot = go.Scatter(x=df.index, y=df["Prediction"], mode="lines+markers")  # [21]
        graph = dcc.Graph(  # [12]
            figure={
                "data": [plot],
                "layout": go.Layout(
                    title=f"Fuel Price Movement: {title}",
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
    def bar_chart(cls, traces):  # [18]
        fig2 = {
            "data": traces,
            "layout": go.Layout(
                title="Twitter Timeline - Average Sentiment of Latest 5 Tweets",
                colorway=["#EF963B", "#EF533B"],
                hovermode="closest",
                xaxis={
                    "title": "Twitter Handles",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"size": 9, "color": "black"},
                },
                yaxis={
                    "title": "Average Sentiment Score",
                    "titlefont": {"color": "black", "size": 14},
                    "tickfont": {"color": "black"},
                },
            ),
        }
        return fig2
