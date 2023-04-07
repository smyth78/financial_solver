from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc

def base_layout(is_working, wi, wp, wn, wr, fwb, solv_indx):
    layout = html.Div(
        [
            dbc.Row([
                dbc.Col(dbc.RadioItems(
                    options=[
                        {"label": "Working", "value": 'working'},
                        {"label": "Retired", "value": 'retired'},
                    ],
                    value='working' if is_working else 'retired',
                    id={'type': "toggle-view", 'index': 0},
                    inline=True,
                ), )
            ], className="mb-3 py-2"),
            dbc.Row([dcc.Markdown('''Change initial values, always leave one box empty...''')], className='pt-1'),
            working_layout(wi, wp, wn, wr, fwb, solv_indx, is_working),
            dbc.Row(dbc.Col(dbc.Button("Fire", color="success", className="me-1", id={'type': 'fire', 'index': 0}), width=3))
        ]
    )
    return layout

def get_input_box_class_name(is_solved):
    return 'mb-3 border border-danger' if is_solved else 'mb-3'

def working_layout(wi, wp, wn, wr, fwb, solved_indx, is_working):
    layout = html.Div(dbc.Row([
        dbc.Col([html.Div(dcc.Markdown('''Initial balance''') if is_working else dcc.Markdown('''Retirement pot'''),
                          className=''),
                 html.Div(dcc.Markdown('''Monthly deposit''') if is_working else dcc.Markdown('''Monthly withdrawal'''),
                          className='pt-1'),
                 html.Div(dcc.Markdown('''Years to work''') if is_working else dcc.Markdown('''Years retired'''),
                          className=''),
                 html.Div(dcc.Markdown('''Interest rate'''), className='pt-2'),
                 html.Div(dcc.Markdown('''Final balance'''), className='pt-3'),
                 ], width=4),
        dbc.Col([html.Div(dcc.Markdown('''$'''), className='pt-1'),
                 html.Div(dcc.Markdown('''$'''), className='pt-3'),
                 html.Div(dcc.Markdown('''yrs'''), className='pt-2'),
                 html.Div(dcc.Markdown('''%'''), className='pt-3'),
                 html.Div(dcc.Markdown('''$'''), className='pt-3')], width=1),
        dbc.Col([
            dbc.Input(placeholder="Initial balance..." if is_working else 'Retirement pot...',
                      type='text',
                      size="md",
                      className=get_input_box_class_name(True if solved_indx == 0 else False),
                      value=wi,
                      id={'type': 'input', 'index': 0}),
            dbc.Input(placeholder="Monthly deposit..." if is_working else 'Monthly withdrawal...',
                      type='text',
                      size="md",
                      className=get_input_box_class_name(True if solved_indx == 1 else False),
                      value=wp,
                      id={'type': 'input', 'index': 1}),
            dbc.Input(placeholder="Years...",
                      size="md",
                      type='text',
                      className=get_input_box_class_name(True if solved_indx == 2 else False),
                      value=wn,
                      id={'type': 'input', 'index': 2}),
            dbc.Input(placeholder="Interest...",
                      size="md",
                      type='text',
                      className=get_input_box_class_name(True if solved_indx == 3 else False),
                      value=wr,
                      id={'type': 'input', 'index': 3}),
            dbc.Input(placeholder="Final balance...",
                      size="md",
                      type='text',
                      className=get_input_box_class_name(True if solved_indx == 4 else False),
                      id={'type': 'input', 'index': 4},
                      value=fwb),
                     ], width=5),
        dbc.Col([dbc.Button("X", color="danger", id={'type': 'clear-box', 'index': 0}),
                 dbc.Button("X", color="danger", className="mt-3", id={'type': 'clear-box', 'index': 1}),
                 dbc.Button("X", color="danger", className="mt-3", id={'type': 'clear-box', 'index': 2}),
                 dbc.Button("X", color="danger", className="mt-3", id={'type': 'clear-box', 'index': 3}),
                 dbc.Button("X", color="danger", className="mt-3    ", id={'type': 'clear-box', 'index': 4})], width=2),
    ]))
    return layout


