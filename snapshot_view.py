# This is the layout web page for Snapshot Dashboard. It contains Dash HTML Components (see tag [1] below) that form the content of the web page.
# To stylise the web page, Dash Bootstrap Components (dbc - see tag [2] below) have been used.
# Dash Bootstrap Components is based on the original Bootstrap (source: https://getbootstrap.com/)
# Dash Bootstrap Components allows you to write Bootstrap using Python in Dash web applications.

# [1] Dash HTML Component library to write html code, URL: https://dash.plot.ly/dash-html-components
# [2] Dash Bootstrap Components library: https://dash-bootstrap-components.opensource.faculty.ai/
# [3] Dash Core Components library to create user interface components, URL: https://dash.plot.ly/dash-core-components

# See nearest_station_view.py to understand how all the Dash Bootstrap Components (dbc) are referenced. They are not again referenced individually in this file.
# One dbc component of each type has been referenced in this file to give a view of how the components have been used to structure the layout of the web page.
# All dbc components in this file have been taken from the following URL's:
# [4] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/card
# [5] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# [6] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/input
# [7] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/button
# [8] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/form
# [9] Adapted from: https://dash-bootstrap-components.opensource.faculty.ai/l/components/jumbotron
# [10] Source: Author: Philippe, Date: Sep '18, URL: https://community.plot.ly/t/adding-local-image/4896/8

import dash_bootstrap_components as dbc  # [2]
import dash_core_components as dcc  # [3]
import dash_html_components as html  # [1]
from project.snapshot_app.natural_language import NewsArticle, RACNewsletter
from project.infrastructure.gui_component import UIComponent
from app import app

supermarket_nonsupermarket_card = [
    dbc.CardHeader(
        "Average UK Fuel Price Predictions (Data Source: RAC Website)"
    ),  # [4]
    dbc.CardBody(  # [4]
        [
            html.P(  # [1]
                dbc.Row(  # [5]
                    [
                        dbc.Col(
                            dbc.FormGroup(  # [8]
                                [
                                    dbc.Label("Select Prediction Horizon"),
                                    dbc.RadioItems(  # [6]
                                        options=[
                                            {"label": "Next Month", "value": "1"},
                                            {"label": "3 Months", "value": "3"},
                                            {"label": "6 Months", "value": "6"},
                                        ],
                                        inline=True,
                                        id="prediction_range_supermarket",
                                    ),
                                ]
                            )
                        )
                    ]
                ),
                className="card-text",
            ),
            html.P(
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(  # [3]
                                id="supermarket-dropdown",
                                options=[
                                    {
                                        "label": "Supermarket Unleaded",
                                        "value": "supermarket-unleaded",
                                    },
                                    {
                                        "label": "Supermarket Diesel",
                                        "value": "supermarket-diesel",
                                    },
                                    {"label": "Unleaded", "value": "unleaded"},
                                    {"label": "Diesel", "value": "diesel"},
                                ],
                                value="",
                                placeholder="Select Fuel Type",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(  # [7]
                                id="submit-button-supermarket",
                                n_clicks=0,
                                children="Predict",
                            )
                        ),
                    ]
                ),
                className="card-text",
            ),
            html.Div(id="supermarket-output"),
        ]
    ),
]

region_card = [
    dbc.CardHeader("UK Regional Average Price Predictor"),
    dbc.CardBody(
        [
            html.P(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.FormGroup(
                                [
                                    dbc.Label("Select Prediction Horizon"),
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Next Month", "value": "1"},
                                            {"label": "3 Months", "value": "3"},
                                            {"label": "6 Months", "value": "6"},
                                        ],
                                        inline=True,
                                        id="prediction_range_region",
                                        value="1",
                                    ),
                                ]
                            )
                        )
                    ]
                ),
                className="card-text",
            ),
        ]
    ),
]
##########RAC Data#####################
newsletter = RACNewsletter("https://media.rac.co.uk/tag/rac-fuel-watch/pressreleases")
predictions = newsletter.generate_prediction()
movement = UIComponent().rac(predictions)
#######################################################

rac_card = [
    dbc.CardHeader(
        "Prediction based on monthly RAC newsletters (Data Source: RAC Website)"
    ),
    dbc.CardBody(
        [
            html.H5(
                dbc.Row(
                    [
                        dbc.Col(
                            "Next Months PFPCS Fuel Price Movement Prediction: ",
                            width=8,
                        ),
                        dbc.Col(movement["overall"], width=4),
                    ]
                )
            ),
            html.Hr(className="my-4"),
            html.P(
                "Disclaimer: RAC Outlooks are scraped from the RAC website",
                className="card-title",
            ),
            html.P(
                dbc.Row(
                    [
                        dbc.Col("RAC Unleaded Outlook: "),
                        dbc.Col(movement["unleaded"], width=6),
                    ]
                )
            ),
            html.P(
                dbc.Row(
                    [
                        dbc.Col("RAC Diesel Outlook: "),
                        dbc.Col(movement["diesel"], width=6),
                    ]
                )
            ),
            html.P(
                dbc.Row(
                    [
                        dbc.Col("RAC Super Unleaded Outlook: "),
                        dbc.Col(movement["super_unleaded"], width=6),
                    ]
                )
            ),
            html.P(
                dbc.Row(
                    [dbc.Col("RAC LPG Outlook: "), dbc.Col(movement["lpg"], width=6)]
                )
            ),
        ]
    ),
]

try:
    prediction = NewsArticle("fuel price uk").generate_prediction()
    discovery_component = UIComponent().discovery(prediction)
    discovery_body = [
        html.P(
            f"The PFPCS prediction is based on news articles dating back to {discovery_component['oldest']}",
            className="card-title",
        ),
        html.H5(
            dbc.Row(
                [
                    dbc.Col(f"Tomorrows PFPCS Movement Fuel Price Prediction:"),
                    dbc.Col(discovery_component["movement"], width=4),
                ]
            )
        ),
        html.Hr(className="my-4"),
        html.Div(
            html.Img(src=app.get_asset_url("wordcloud.png"), alt="wordcloud")
        ),  # [10]
    ]
except:
    discovery_body = ["Error"]


news_card = [
    dbc.CardHeader(
        "Prediction based on UK fuel price news articles (Data Source: IBM Discovery API)"
    ),
    dbc.CardBody(discovery_body),
]


twitter_handle_card = [
    dbc.CardHeader("Twitter Sentiment of UK Fuel Retailers (Data Source: Twitter API)"),
    dbc.CardBody(
        [
            html.P("Select Twitter handle(s)", className="card-title"),
            html.Div(
                [
                    dcc.Dropdown( #[3]
                        id="timeline-dropdown",
                        options=[
                            {"label": "BP", "value": "BP_Press"},
                            {"label": "Shell", "value": "Shell"},
                            {"label": "Total", "value": "TOTALinUK"},
                            {"label": "Esso", "value": "Esso_GB"},
                            {"label": "Sainsburys", "value": "SainsburysNews"},
                            {"label": "Tesco", "value": "tesconews"},
                            {"label": "Morrisons", "value": "MorrisonsNews"},
                            {"label": "Asda", "value": "asda"},
                        ],
                        value=["BP_Press", "Shell"],
                        multi=True,
                    ),
                    dcc.Graph(id="live-update-graph2"), #[3]
                ]
            ),
        ]
    ),
]


row_1 = dbc.Row(
    [
        dbc.Col(
            dbc.Card(supermarket_nonsupermarket_card, color="dark", outline=True),
            className="mb-4",
        ),
        dbc.Col(dbc.Card(twitter_handle_card, color="dark", outline=True)),
    ],
    className="bg-white text-dark mb-4",
)

row_2 = dbc.Row(
    [
        dbc.Col(dbc.Card(rac_card, color="dark", outline=True), className="mb-4"),
        dbc.Col(dbc.Card(news_card, color="dark", outline=True)),
    ],
    className="bg-white text-dark mb-4",
)
row_3 = dbc.Row(
    [dbc.Col(dbc.Card(twitter_handle_card, color="dark", outline=True))],
    className="bg-white text-dark mb-4",
)

cards = html.Div([row_2, row_1])

jumbotron_homepage = dbc.Jumbotron(  # [9]
    [
        html.H1("Predictive Fuel Price Comparison Service", className="display-3"),
        html.P(
            "The PFPCS application helps car owners save money on fuel",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "The Snapshot dashboard provides a fuel price movement prediction for tomorrow and next month, and average UK predictions for 1/3/6 months\n"
        ),
        cards,
    ],
    className="bg-white text-dark",
)
