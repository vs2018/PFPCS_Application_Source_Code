# [1] Dash Bootstrap Components library to write bootstrap components, URL: https://dash-bootstrap-components.opensource.faculty.ai/
# [2] Source: https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar

import dash_bootstrap_components as dbc  # [1]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Snapshot", href="/")),
        dbc.NavItem(dbc.NavLink("Nearest Station", href="/nearest-station")),
        dbc.NavItem(dbc.NavLink("Journey Saver", href="/journey-saver")),
    ],
    brand="PFPCS",
    brand_href="/",
    color="dark",
    dark=True,
)  # [2]
