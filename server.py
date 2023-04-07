import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    prevent_initial_callbacks=False,
    compress=True,
)
app.config.suppress_callback_exceptions = True
app.title = 'savings_calc'

server = app.server


