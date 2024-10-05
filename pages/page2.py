#############################
#
# LIBRERIAS
#
#############################
import dash
from dash import Dash, dcc, html, Input, Output, callback
from utils import ecuacion_logistica

dash.register_page(__name__, path="/ODE2", name="Logistic-Equation")

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
                                html.H3("Initial Poblation"),
                                dcc.Input(type="number", value=10, id="pob_ini"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial Time"),
                                dcc.Input(type="number", value=10, id="time_ini"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Final Time"),
                                dcc.Input(type="number", value=50, id="time_fin"),
                            ]
                        ),
                    ],
                ),
                html.H3("Growth Rate"),
                dcc.Input(max=5, step=0.1, type="number", value=0.15, id="r"),
                html.H3("Load Capacity"),
                dcc.Input(type="number", value=150, id="K"),
                html.H3("Mesh for the vector field"),
                dcc.Slider(
                    min=1,
                    max=40,
                    step=1,
                    value=15,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id="mesh",
                ),
                html.H3("Vector Size"),
                dcc.Slider(min=0.1, max=2, step=0.1, value=1, id="size_vec"),
                html.H3("Mostrar campo vectorial"),
                dcc.Checklist(
                    options=[{"label": " Activar", "value": "show_field"}],
                    value=["show_field"],  # Valor inicial, campo vectorial activo
                    id="toggle_vector_field",
                    inline=True,
                ),
            ],
        ),
        html.Div(
            className="div_graphic",
            children=[
                html.H2("ODE Logistic Equation"),
                dcc.Loading(type="default", children=dcc.Graph(id="figure_2")),
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
    Output("figure_2", "figure"),
    Input("pob_ini", "value"),
    Input("time_ini", "value"),
    Input("time_fin", "value"),
    Input("r", "value"),
    Input("K", "value"),
    Input("mesh", "value"),
    Input("size_vec", "value"),
    Input("toggle_vector_field", "value"),
)
def ode2_graph_logistic_equation(P0, t_i, t_f, r, K, mesh, size_vec, toggle_field):
    show_field = "show_field" in toggle_field
    fig = ecuacion_logistica(K, P0, r, t_i, t_f, mesh, size_vec, show_field)
    return fig
