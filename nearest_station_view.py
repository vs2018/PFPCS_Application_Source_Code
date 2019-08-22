# This is the layout web page for the Nearest Dashboard. It contains Dash HTML Components that form the content of the web page.
# To stylise the web page, Dash Bootstrap Components (dbc - see tag [2] below) have been used.
# Dash Bootstrap Components is based on the original Bootstrap (source: https://getbootstrap.com/)
# Dash Bootstrap Components is an interface to enable writing bootstrap using python in Dash web applications.

# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Dash Bootstrap Components library: https://dash-bootstrap-components.opensource.faculty.ai/
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components

# The HTML Components, Dash Core Components and Dash Bootstrap Components have been referenced on a best effort basis
# to help the reader understand how the components have been used to design the web page layout.
# All dbc components in this file have been taken from the following URL's:
# [4] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/card
# [5] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# [6] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/input_group
# [7] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/input
# [8] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/button
# [9] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/form
# [10] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/jumbotron


import dash_core_components as dcc  # [3]
import dash_html_components as html  # [1]
import dash_bootstrap_components as dbc  # [2]

card_details = [
    dbc.CardHeader("Complete the form and click 'Search Fuel Prices'"),  # [4]
    dbc.CardBody(  # [4]
        [
            html.P(  # [1]
                dbc.Row(  # [5]
                    [
                        dbc.Col(  # [5]
                            html.Div(  # [1]
                                dbc.InputGroup(  # [6]
                                    [
                                        dbc.Input(
                                            placeholder="Enter postcode with 'A'",
                                            id="autocompleteInput-nearest",
                                        )  # [7]
                                    ]
                                )
                            ),
                            width=7,
                        ),
                        dbc.Col(
                            html.Div(
                                dbc.InputGroup(  # [6]
                                    [
                                        html.P(
                                            dbc.Button(  # [8]
                                                children="Search Address",
                                                color="btn btn-dark",
                                                id="submit-post-code-button",
                                                n_clicks=0,
                                            ),
                                            className="lead",
                                        )
                                    ]
                                )
                            ),
                            width=5,
                        ),
                    ]
                ),
                className="card-text",
            ),
            html.P(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(  # [3]
                                    id="dropdown-nearest", placeholder="Select Address"
                                )
                            )
                        )
                    ]
                ),
                className="card-text",
            ),
            html.Div(
                dbc.FormGroup(  # [9]
                    [
                        dbc.Label("Select Fuel Grade"),
                        dbc.RadioItems(  # [7]
                            options=[
                                {"label": "Diesel", "value": "Diesel"},
                                {"label": "Premium Diesel", "value": "Premium Diesel"},
                                {"label": "Unleaded", "value": "Unleaded"},
                                {"label": "Super Unleaded", "value": "Super Unleaded"},
                            ],
                            inline=True,
                            id="fuel_type",
                        ),
                    ]
                )
            ),
            html.P(
                dbc.Button(  # [8]
                    children="Search Fuel Prices",
                    color="btn btn-dark",
                    id="submit-button",
                    n_clicks=0,
                    size="lg",
                ),
                className="lead",
            ),
        ]
    ),
]  # [1] [4] [5]

input_card = dbc.FormGroup(
    dbc.Card(card_details, color="dark", outline=True)
)  # [4] [9]

app1_form = dbc.Row(
    [
        dbc.Col(input_card, width=9),
        dbc.Col(html.Div(id="api-result"), html.Div(id="render-knob-app1"), width=3),
    ],
    form=True,
)  # [1] [5] [9]


jumbotron_app1 = html.Div(
    dbc.Jumbotron(
        [
            html.H1("Nearest Station Dashboard", className="display-3"),
            html.P(
                "Search and compare fuel prices by petrol station in a 5 mile radius (Data Source: UK Vehicle Data API)",
                className="lead",
            ),
            html.Hr(className="my-2"),
            app1_form,
            html.Hr(className="my-2"),
        ],
        className="bg-white text-dark px-5 pt-5 pb-0 mb-0",
    )
)  # #[1] [10]

card_content_app1 = [
    dbc.CardHeader(
        html.H5("Map - Petrol Stations and Routes", className="card-title")
    ),  # [4]
    dbc.CardBody(html.Div(id="data-table-analytics")),  # [1]  # [4]
]

card_content_bar = [
    dbc.CardHeader(
        html.H5(
            "Petrol Station Analysis - Current and Predicted Price",
            className="card-title",
        )  # [1]
    ),  # [4]
    dbc.CardBody(
        [
            html.Div(dbc.Label("Select Metric")),  # [9]
            html.Div(
                dbc.RadioItems(  # [7]
                    options=[
                        {"label": "Brand", "value": "Brand"},
                        {"label": "Distance", "value": "Distance"},
                        {"label": "Post Code", "value": "Post Code"},
                    ],
                    inline=True,
                    id="radio-metrics",
                    value="Brand",
                )
            ),  # [1]
            html.Div(dbc.Label("Select Distance Radius")),  # [1] [9]
            html.Div(
                dcc.Slider(
                    id="slider-metrics",
                    min=0,
                    max=5,
                    marks={
                        0: "0 mi",
                        0.5: "0.5 mi",
                        1.0: "1.0 mi",
                        1.5: "1.5 mi",
                        2.0: "2.0 mi",
                        2.5: "2.5 mi",
                        3.0: "3.0 mi",
                        3.5: "3.5 mi",
                        4.0: "4.0 mi",
                        4.5: "4.5 mi",
                        5: "5.0 mi",
                    },
                    value=5,
                ),  # [3]
                className="mb-4",
            ),  # [1]
            html.Div(id="brand-prices"),  # [1]
        ]
    ),  # [4]
]

card_content_line = [
    dbc.CardHeader(
        html.H5(
            "Fuel Price Movement - Historical and Predicted Price",
            className="card-title",
        )  # [1]
    ),  # [4]
    dbc.CardBody(html.P(id="station-details")),  # [4]
]

card_content_pie = [
    dbc.CardHeader(
        html.H5("Petrol Station Company Type", className="card-title")
    ),  # [4]
    dbc.CardBody(id="app1-pie-chart"),  # [4]
]

jumbotron_result_app1 = dbc.Jumbotron(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="data-table"), width=7),  # [1] [5]
                        dbc.Col(
                            dcc.Loading(
                                id="loading-cards",
                                children=[html.Div(html.Div(id="summary_cards"))],
                                type="default",
                            ),  # [3]
                            width=5,
                        ),  # [5]
                    ]
                )  # [5]
            ],
            fluid=True,
            className="my-0",
        )  # [5]
    ],
    fluid=True,
    className="px-4 pt-5 pb-1 mb-0 bg-white text-dark",
)  # [10]

jumbotron_result2_app1 = dbc.Jumbotron(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                id="loading-map",
                                children=[
                                    html.Div(
                                        dbc.Card(
                                            card_content_app1,
                                            color="dark",
                                            outline=True,
                                        )  # [4]
                                    )  # [1]
                                ],
                                type="default",
                            ),  # [3]
                            width=6,
                        ),  # [5]
                        dbc.Col(
                            html.Div(
                                dbc.Card(
                                    card_content_line, color="dark", outline=True
                                )  # [4]
                            ),  # [1]
                            width=6,
                        ),  # [5]
                    ]
                )
            ],
            fluid=True,
            className="my-0",
        )  # [5]
    ],
    fluid=True,
    className="px-4 pt-5 pb-1 mb-0 bg-white text-dark",
)  # [10]


jumbotron_layout_app1 = dbc.Jumbotron(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                dbc.Card(
                                    card_content_bar, color="dark", outline=True
                                )  # [4]
                            ),  # [1]
                            width=7,
                        ),  # [5]
                        dbc.Col(
                            html.Div(
                                dbc.Card(
                                    card_content_pie, color="dark", outline=True
                                )  # [4]
                            ),  # [1]
                            width=5,
                        ),  # [5]
                    ]
                )
            ],
            fluid=True,
            className="my-0",
        )  # [5]
    ],
    fluid=True,
    className="px-4 pt-5 pb-1 mb-0 bg-white text-dark",
)  # [10]

jumbotron_bottom = dbc.Jumbotron(
    fluid=True, className="my-0 bg-white text-dark"
)  # [10]

layout_first_quarter = dbc.Jumbotron(
    [html.Div(id="jumbotron_result_app1")],  # [1]
    fluid=True,
    className="my-0 py-0 bg-white text-dark",
)  # [10]

layout_second_quarter = dbc.Jumbotron(
    [html.Div(id="jumbotron_result2_app1")],  # [1]
    fluid=True,
    className="my-0 py-0 bg-white text-dark",
)  # [10]


layout_third_quarter = dbc.Jumbotron(
    [html.Div(id="jumbotron_layout_app1")],  # [1]
    fluid=True,
    className="py-0 my-0 py-0 bg-white text-dark",
)  # [10]
