#############################
#
# LIBRERIAS
#
#############################
import dash
from dash import Dash, dcc, html, Input, Output, callback
from utils import lotka_volterra, lotka_volterra_system

dash.register_page(__name__, path="/ODE3", name="Lotka-Volterra")

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
                                html.H3("Initial Prey Population"),
                                dcc.Input(type="number", value=50, id="prey_pob_ini"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial Predator Population"),
                                dcc.Input(
                                    type="number", value=20, id="predator_pob_ini"
                                ),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    className="div_flex",
                    children=[
                        html.Div(
                            [
                                html.H3("Final Time"),
                                dcc.Input(type="number", value=50, id="time_fin3"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Prey Growth Rate"),
                                dcc.Input(
                                    max=1,
                                    step=0.01,
                                    type="number",
                                    value=0.4,
                                    id="alpha",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Predation Rate"),
                                dcc.Input(
                                    max=1,
                                    step=0.01,
                                    type="number",
                                    value=0.02,
                                    id="beta",
                                ),
                            ]
                        ),
                    ],
                ),
                html.H3("Predator Growth Rate"),
                dcc.Input(
                    max=1,
                    step=0.01,
                    type="number",
                    value=0.01,
                    id="delta",
                ),
                html.H3("Predator Death Rate"),
                dcc.Input(
                    max=1,
                    step=0.01,
                    type="number",
                    value=0.1,
                    id="gamma",
                ),
                html.H3("Mesh for the Vector Field"),
                dcc.Slider(
                    min=1,
                    max=40,
                    step=1,
                    value=20,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id="mesh3",
                ),
                html.H3("Vector Size"),
                dcc.Slider(min=0.1, max=1, step=0.1, value=0.3, id="size_vec3"),
                dcc.Markdown(
                    r"""
                    ### Lotka-Volterra Equations:
                    $$ 
                    \begin{aligned}
                    \frac{dx}{dt} &= \alpha x - \beta xy \\
                    \frac{dy}{dt} &= \delta xy - \gamma y 
                    \end{aligned} 
                    $$
                    """,
                    mathjax=True,  # Enables LaTeX rendering
                    style={
                        "margin-top": "30px",
                        "font-size": "24px",
                    },  # Increases the font size
                ),
            ],
        ),
        html.Div(
            className="div_graphic",
            children=[
                html.H2("Lotka-Volterra Equations"),
                dcc.Loading(type="default", children=dcc.Graph(id="figure_3")),
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
    Output("figure_3", "figure"),
    Input("alpha", "value"),
    Input("beta", "value"),
    Input("delta", "value"),
    Input("gamma", "value"),
    Input("prey_pob_ini", "value"),
    Input("predator_pob_ini", "value"),
    Input("time_fin3", "value"),
    Input("mesh3", "value"),
    Input("size_vec3", "value"),
)
def ode_3_graph_lotka_volterra(
    alpha,
    beta,
    delta,
    gamma,
    prey_pob_ini,
    predator_pob_ini,
    time_fin3,
    mesh3,
    size_vec3,
):
    fig3 = lotka_volterra(
        alpha,
        beta,
        delta,
        gamma,
        prey_pob_ini,
        predator_pob_ini,
        time_fin3,
        mesh3,
        size_vec3,
    )
    return fig3
