#############################
#
# LIBRERIAS
#
#############################
import dash
from dash import dcc, html, Input, Output, callback
from utils.odeDengue import enfermedad_dengue, poblacion_mosquito

dash.register_page(__name__, path="/Dengue", name="Dengue Model")

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
                html.H2("Model Parameters"),
                html.Div(
                    className="div_flex",
                    children=[
                        html.Div(
                            [
                                html.H3("Transmission Rate (β)"),
                                dcc.Input(
                                    type="number", step=0.1, value=0.8, id="beta_dengue"
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Transmission Efficiency (ψ)"),
                                dcc.Input(
                                    type="number", step=0.1, value=0.7, id="psi_dengue"
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Recovery Rate (σ)"),
                                dcc.Input(
                                    type="number",
                                    step=0.1,
                                    value=0.2,
                                    id="sigma_dengue",
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
                                html.H3("Natural Death Rate (δ)"),
                                dcc.Input(
                                    type="number",
                                    step=0.01,
                                    value=0.2,
                                    id="delta_dengue",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Birth Rate (µ)"),
                                dcc.Input(
                                    type="number",
                                    step=0.001,
                                    value=0.0042,
                                    id="mu_dengue",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Recovery Rate of Infected (θ)"),
                                dcc.Input(
                                    type="number",
                                    step=0.01,
                                    value=1 / 7,
                                    id="theta_dengue",
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
                                html.H3("Initial Susceptible (p₀)"),
                                dcc.Input(type="number", value=0.9, id="p0_dengue"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial Infected (q₀)"),
                                dcc.Input(type="number", value=0.05, id="q0_dengue"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Final Time"),
                                dcc.Input(type="number", value=100, id="t_end_dengue"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                html.H3("Vector Field Mesh"),
                                dcc.Slider(
                                    min=10,
                                    max=50,
                                    step=5,
                                    value=20,
                                    id="mesh_dengue",
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                html.H3("Vector Size"),
                                dcc.Slider(
                                    min=0.1,
                                    max=2,
                                    step=0.1,
                                    value=1,
                                    id="size_vec_dengue",
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            className="div_graphic",
            children=[
                html.H2("Dengue Transmission Model - Disease Dynamics"),
                dcc.Loading(
                    type="default",
                    children=html.Div(
                        className="centered-figure",
                        children=dcc.Graph(id="figure_disease"),
                    ),
                ),
            ],
        ),
        html.Div(
            className="div_graphic",
            children=[
                html.H2("Dengue Transmission Model - Mosquito Population Dynamics"),
                dcc.Loading(
                    type="default",
                    children=html.Div(
                        className="centered-figure",
                        children=dcc.Graph(id="figure_population"),
                    ),
                ),
            ],
        ),
    ],
)

#############################
#
# Callbacks
#
#############################


@callback(
    [Output("figure_disease", "figure"), Output("figure_population", "figure")],
    [
        Input("beta_dengue", "value"),
        Input("psi_dengue", "value"),
        Input("sigma_dengue", "value"),
        Input("delta_dengue", "value"),
        Input("mu_dengue", "value"),
        Input("theta_dengue", "value"),
        Input("p0_dengue", "value"),
        Input("q0_dengue", "value"),
        Input("t_end_dengue", "value"),
        Input("mesh_dengue", "value"),
        Input("size_vec_dengue", "value"),
    ],
)
def update_dengue_graphs(
    beta, psi, sigma, delta, mu, theta, p0, q0, t_end, mesh, size_vec
):
    # Gráfica del modelo de la enfermedad
    figure_disease = enfermedad_dengue(
        beta, psi, sigma, delta, mu, theta, p0, q0, t_end, mesh, size_vec
    )

    # Gráfica del modelo de población de mosquitos
    figure_population = poblacion_mosquito(
        delta, 0.1, sigma, 0.8, 2, 0.1, 1000, 0.1, 0.05, 200, t_end, mesh, size_vec
    )

    return figure_disease, figure_population
