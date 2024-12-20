from dash import Dash, html, dcc
import dash

# Inicializamos la app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

# Definir el layout de la app
app.layout = html.Div(
    children=[
        # Primer Div: Header
        html.Div(
            className="header",
            children=[
                html.Img(className="sm_logo", src="assets/img/logo.jpg"),
                html.H1(
                    "Mathematical Models Graphic Interface",
                    className="main_title",
                ),
            ],
        ),
        # Segundo Div: Navegación
        html.Div(
            className="navigation_container",
            children=[
                dcc.Link(
                    html.Button("Simple Model ODE", className="buton ode_1"), href="/"
                ),
                dcc.Link(
                    html.Button("Logistic Equation ODE", className="buton ode_2"),
                    href="/ODE2",
                ),
                dcc.Link(
                    html.Button("Lotka-Volterra Equations", className="buton ode_3"),
                    href="/ODE3",
                ),
                dcc.Link(
                    html.Button(
                        "SIR Basic",
                        className="buton epiModels",
                    ),
                    href="/Epidemiological",
                ),
                dcc.Link(
                    html.Button(
                        "Dengue Model",
                        className="buton dengue",
                    ),
                    href="/Dengue",
                ),
            ],
        ),
        # Contenedor de las páginas
        dash.page_container,
        # Div: Footer (Pie de página que estará al final de la página)
        html.Div(
            className="footer",
            children=[
                html.P(
                    "Julca Delgado Enrique - 22140111",
                    className="footer_text",
                ),
            ],
        ),
    ]
)

# Corremos la app en el puerto 1254
if __name__ == "__main__":
    app.run(debug=True, port="1254")
