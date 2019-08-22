# This is the layout web page for Journey Saver Dashboard. It contains Dash HTML Components that form the content of the web page.
# To stylise the web page, Dash Bootstrap Components (dbc - see tag [2] below) have been used.
# Dash Bootstrap Components is based on the original Bootstrap (source: https://getbootstrap.com/)
# Dash Bootstrap Components is an interface to enable writing bootstrap using python in Dash web applications.

# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Dash Bootstrap Components library: https://dash-bootstrap-components.opensource.faculty.ai/
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components

# See nearest_station_view.py to understand how all the Dash Bootstrap Components (dbc) are referenced. They are not again referenced individually in this file.
# One dbc component of each type has been referenced in this file to give a view of how the components have been used to structure the layout of the web page.
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

form_input = [
    dbc.CardHeader(
        "Complete the form to get fuel prices at petrol stations along your journey"
    ),  # [4]
    dbc.CardBody(
        [
            html.Div(id="fuel_type", className="card-text"),  # [1]
            html.P(id="tank-knob", className="card-text"),  # [1]
            html.P(id="post-code-inputs", className="card-text"),  # [1]
            html.P(id="search-price-button", className="card-text"),  # [1]
        ]
    ),  # [4]
]

inline_radioitems = dbc.FormGroup(
    dbc.Card(form_input, color="dark", outline=True)
)  # [9] [4]

car_details = dbc.Row(  # [5]
    [
        dbc.Col(  # [5]
            dbc.FormGroup(  # [9]
                [
                    html.P(  # [1]
                        "Enter Car Registration (must contain an 'A'), e.g: AV04YGE"
                    ),
                    dbc.Input(  # [7]
                        placeholder="Enter Car Registration",
                        type="text",
                        bs_size="lg",
                        className="mb-3",
                        id="registration",
                        value="",
                    ),
                    html.P(  # [1]
                        dbc.Button(  # [8]
                            children="Submit Registration",
                            color="primary",
                            id="submit-button-registration",
                            n_clicks=0,
                            size="lg",
                        ),
                        className="lead",
                    ),
                    html.Div(id="input-form-final"),  # [1]
                ]
            ),
            width=9,
        ),
        dbc.Col(html.Div(id="render-car"), width=3),  # [5] [1]
    ]
)

jumbotron_app2 = dbc.Jumbotron(  # [10]
    [
        html.H1("Journey Saver Dashboard", className="display-3"),
        html.P(
            "Enter car registration number and journey details to get personalised fuel price insights (Data Source: UK Vehicle Data API)",
            className="lead",
        ),
        html.Hr(className="my-2"),
        car_details,
        html.Div(id="journey-search-alert"),
        html.Div(id="tank-analysis"),
    ],
    className="bg-white text-dark px-5 mb-0",
)

jumbotron_result = dbc.Jumbotron(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                id="loading-journey-map",
                                children=[html.Div(id="map-card")],
                                type="default",
                            ),
                            width=5,
                        ),
                        dbc.Col(
                            dcc.Loading(
                                id="loading-journey-table",
                                children=[html.Div(id="table-card")],
                                type="default",
                            ),
                            width=7,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                id="loading-journey-analysis",
                                children=[html.Div(id="analysis-card")],
                                type="default",
                            ),
                            width=12,
                        )
                    ],
                    className="bg-white text-dark mt-4",
                ),
            ],
            fluid=True,
            className="bg-white text-dark my-0",
        )
    ],
    className="bg-white text-dark my-0",
)

post_code_inputs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    dbc.Button(  # [8]
                                        children="Origin",
                                        color="btn btn-dark",
                                        id="submit-origin-button",
                                        n_clicks=0,
                                    )
                                ),
                                dbc.Input(
                                    placeholder="Enter postcode with 'A'",
                                    id="autocompleteInput-origin",
                                    value="",
                                ),
                            ]
                        )
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-origin",
                            placeholder="Click 'Origin' button to select origin address",
                        )
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dbc.InputGroup(  # [6]
                            [
                                html.P(
                                    dbc.Button(
                                        children="Destination",
                                        color="btn btn-dark",
                                        id="submit-destination-button",
                                        n_clicks=0,
                                    ),
                                    className="lead",
                                ),
                                dbc.Input(
                                    placeholder="Enter postcode with 'A'",
                                    id="autocompleteInput-destination",
                                    value="",
                                ),
                            ]
                        )
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-destination",
                            placeholder="Click 'Destination' button to select destination address",
                        )
                    )
                ),
            ]
        ),
    ]
)
