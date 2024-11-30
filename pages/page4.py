#############################
#
# LIBRERIAS
#
#############################
import dash
from dash import Dash, dcc, html, Input, Output, callback
from utils import SIR_conditioned, SIR_conditioned_system

dash.register_page(__name__, path="/Epidemiological", name="Epidemiological-models")

#############################
#
# Layout HTML
#
#############################

layout = html.Div(
    className="Pages",
    children=[
        html.Div(
            className="div_parameters",
            children=[
                html.H2("Parameters"),
                html.Div(
                    className="div_flex",
                    children=[
                        html.Div(
                            [
                                html.H3("Infection rate"),
                                dcc.Input(
                                    max=1,
                                    step=0.0001,
                                    type="number",
                                    value=0.0005,
                                    id="infection_rate",
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.H3("Recovery rate"),
                                dcc.Input(
                                    max=1,
                                    step=0.005,
                                    type="number",
                                    value=0.1,
                                    id="recovery_rate",
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.H3("Change Point"),
                                dcc.Input(type="number", value=15, id="change_point"),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="div_flex",
                    children=[
                        html.Div(
                            [
                                html.H3("Initial Suceptibles"),
                                dcc.Input(
                                    type="number", value=1999, id="suceptibles_ini"
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial infected"),
                                dcc.Input(
                                    type="number",
                                    value=1,
                                    id="infected_ini",
                                    disabled=True,
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial recovered"),
                                dcc.Input(
                                    type="number",
                                    value=0,
                                    id="recovered_ini",
                                    disabled=True,
                                ),
                            ]
                        ),
                    ],
                ),
                html.H3("Final time"),
                dcc.Input(type="number", value=100, id="time_fin4"),
            ],
        ),
        html.Div(
            className="div_graphic",
            children=[
                html.H2(r"Change of β, γ from a point"),
                dcc.Loading(
                    type="default",
                    children=html.Div(
                        className="centered-figure", children=dcc.Graph(id="figure_4")
                    ),
                ),
            ],
        ),
    ],
)


#############################
#
# Callback
#
#############################


@callback(
    Output("figure_4", "figure"),
    Input("infection_rate", "value"),
    Input("recovery_rate", "value"),
    Input("change_point", "value"),
    Input("suceptibles_ini", "value"),
    Input("infected_ini", "value"),
    Input("recovered_ini", "value"),
    Input("time_fin4", "value"),
)
def conditioned_system_epidemiological(
    infection_rate,
    recovery_rate,
    change_point,
    suceptibles_ini,
    infected_ini,
    recovered_ini,
    time_fin4,
):
    fig4 = SIR_conditioned(
        infection_rate,
        recovery_rate,
        change_point,
        suceptibles_ini,
        infected_ini,
        recovered_ini,
        time_fin4,
    )
    return fig4
