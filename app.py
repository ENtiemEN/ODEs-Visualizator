from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div(
    children=[
        # Primer Div
        html.Div(
            className="header",
            children=[
                html.Img(className="sm_logo", src="assets/img/logo.jpg"),
                html.H1(
                    "ODE's Graphic Interface - Enrique Julca", className="main_title"
                ),
            ],
        ),
        # Segundo Div
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
                    href="ODE3",
                ),
            ],
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True, port="1254")
