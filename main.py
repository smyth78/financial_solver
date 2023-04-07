import json

import pandas as pd
from sympy import Symbol
from sigfig import round

from dash import dcc, ctx
from dash import html
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc

from server import app
import layouts, constants, alerts
import helper_functions as hf


header = dbc.Container(
    [
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("About", href="/about"))
            ],
        )
    ]
)

app.layout = html.Div(
    [
        dbc.NavbarSimple([header], className="mb-5", id='nav-bar',
                         brand="Savings Calculator",
                         brand_href="/",
                         color="dark",
                         dark=True,
                         ),
        dbc.Container(html.Div(id='alert-1')),
        dbc.Container(id='page-content'),
        # create the session store
        dcc.Store(id='session', storage_type='session'),
    ]
)

@app.callback(
    [Output('page-content', 'children'),
     Output('session', 'data'),
     Output('alert-1', 'children'),
     Output({'type': 'input', 'index': ALL}, 'value')],
    [Input({'type': 'fire', 'index': ALL}, 'n_clicks'),
     Input({'type': 'toggle-view', 'index': ALL}, 'value'),
     Input({'type': 'clear-box', 'index': ALL}, 'n_clicks')],
    [State('session', 'data'),
     State({'type': 'input', 'index': ALL}, 'value'),
     State({'type': 'toggle-view', 'index': ALL}, 'value')],)
def create_initial_layout(fire, toggle_change, clear, stored_data, inputs, toggle_state):
    trig_id = ctx.triggered_id
    alert = None
    base_lo = None
    is_working = True if 'working' in toggle_state or toggle_state == [] else False

    # set initial values
    if trig_id is None:
        # define initial values of input boxes
        wi, wp, wn, wr, final_w_bal = '20,000', '300', '20', '7', ''
        base_lo = layouts.base_layout(is_working, wi, wp, wn, wr, final_w_bal, None)

    # if any CB triggered
    else:
        [wi, wp, wn, wr, final_w_bal] = hf.convert_fstrings_to_floats(inputs)

        if trig_id['type'] == 'clear-box':
            index_of_none = [i for i, v in enumerate(clear) if v is not None][0]
            inputs[index_of_none] = ''
            base_lo = layouts.base_layout(is_working, wi, wp, wn, wr, final_w_bal, None)

        elif trig_id['type'] == 'toggle-view':
            if 'working' in toggle_change:
                base_lo = layouts.base_layout(is_working, wi, wp, wn, wr, final_w_bal, None)
                [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings(
                    [wi, wp, wn, wr, final_w_bal])
                inputs = [final_w_bal, wp, wn, wr, wi]
            else:
                base_lo = layouts.base_layout(is_working, final_w_bal, wp, wn, wr, '', None)
                [final_w_bal, wp, wn, wr, wi] = hf.convert_floats_to_ints_to_fstrings(
                    [final_w_bal, wp, wn, wr, None])
                inputs = [final_w_bal, wp, wn, wr, wi]

        elif trig_id['type'] == 'fire':
            # check to make sure only 1 empty box
            if sum(x == '' for x in inputs) != 1:
                alert = alerts.only_1_empty
                wi, wp, wn, wr, final_w_bal = inputs
                base_lo = layouts.base_layout(is_working, wi, wp, wn, wr, final_w_bal, None)
            # find SINGLE empty box...
            else:
                index_of_none = [i for i in range(len(inputs)) if inputs[i] == ''][0]
                highlight_box = None

                # choose first financial eqn for f, i and p and v2 for r and n
                # first option i
                if index_of_none == 0:
                    solved_i = hf.solve_working_equation(Symbol('i'), wp, wn, wr, final_w_bal, is_working)
                    [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings([solved_i, wp, wn, wr, final_w_bal])
                    highlight_box = 0

                # this one for p
                elif index_of_none == 1:
                    solved_p = hf.solve_working_equation(wi, Symbol('p'), wn, wr, final_w_bal, is_working)
                    [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings(
                        [wi, solved_p, wn, wr, final_w_bal])
                    highlight_box = 1

                # this one for n
                elif index_of_none == 2:
                    solved_n = hf.solve_working_equation_v2(wi, wp, Symbol('n'), wr, final_w_bal)
                    [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings(
                        [wi, wp, solved_n, wr, final_w_bal])
                    highlight_box = 2

                # use second formula for r
                # this one for r
                elif index_of_none == 3:
                    solved_r = hf.solve_working_equation_v2(wi, wp, wn,  Symbol('r'), final_w_bal)
                    [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings(
                        [wi, wp, wn, solved_r, final_w_bal])
                    highlight_box = 3

                # this one for f
                elif index_of_none == 4:
                    solved_f = hf.solve_working_equation(wi, wp, wn, wr, Symbol('f'), is_working)
                    [wi, wp, wn, wr, final_w_bal] = hf.convert_floats_to_ints_to_fstrings(
                        [wi, wp, wn, wr, solved_f])
                    highlight_box = 4

                base_lo = layouts.base_layout(is_working, wi, wp, wn, wr, final_w_bal, highlight_box)
                # need to add the sovled val to input list....
                inputs = [wi, wp, wn, wr, final_w_bal]
    return base_lo, None, alert, inputs

if __name__ == '__main__':
    app.run_server(debug=True)

