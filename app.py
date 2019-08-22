# [1] Source: Dash Multi-page App Layout, URL: https://dash.plot.ly/urls
# [2] Dash Bootstrap Components library to write bootstrap components, URL: https://dash-bootstrap-components.opensource.faculty.ai/
# [3] Source: Author:shaytangolova, Date:Feb 3, URL:https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/23


import dash  # [1]
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # [1] [2]

server = app.server  # [1]
app.config.suppress_callback_exceptions = True  # [1]
app.css.append_css({"external_url": "assets/style.css"})  # [3]
