#############################
#
# LIBRERIAS
#
#############################
import dash
from dash import Dash, dcc, html, Input, Output, callback
from utils import simple_equation

dash.register_page(__name__, path="/", name="simple_equation")

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
                                html.H3("Initial value"),
                                dcc.Input(type="number", value=0.5, id="val_ini"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Initial Time"),
                                dcc.Input(type="number", value=0, id="time_ini1"),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("Final Time"),
                                dcc.Input(type="number", value=2, id="time_fin1"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    className="div_flex",
                    children=[
                        html.Div(
                            [
                                html.H3("a rate"),
                                dcc.Input(
                                    max=10, step=0.1, type="number", value=5, id="a"
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H3("b rate"),
                                dcc.Input(
                                    max=10, step=0.1, type="number", value=1, id="b"
                                ),
                            ]
                        ),
                    ],
                ),
                html.H3("Mesh for the vector field"),
                dcc.Slider(
                    min=1,
                    max=30,
                    step=1,
                    value=10,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id="mesh1",
                ),
                html.H3("Vector size"),
                dcc.Slider(min=0.02, max=0.1, step=0.005, value=0.03, id="size_vec1"),
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
                html.H2("Simple ODE graph"),
                dcc.Loading(
                    type="default",
                    children=html.Div(
                        className="centered-figure", children=dcc.Graph(id="figure_1")
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
    Output("figure_1", "figure"),
    Input("val_ini", "value"),
    Input("a", "value"),
    Input("b", "value"),
    Input("time_ini1", "value"),
    Input("time_fin1", "value"),
    Input("mesh1", "value"),
    Input("size_vec1", "value"),
    Input("toggle_vector_field", "value"),
)
def ode1_graph_simple_equation(y0, a, b, t_0, t_f, mesh1, size_vec1, toggle_field):
    show_field = (
        "show_field" in toggle_field
    )  # Verifica si el campo vectorial está activado
    fig1 = simple_equation(y0, a, b, t_0, t_f, mesh1, size_vec1, show_field)
    return fig1
