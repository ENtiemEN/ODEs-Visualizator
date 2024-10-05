# Libraries
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.integrate import odeint
from plotly.subplots import make_subplots

# Functions


def simple_equation(
    y0: float,
    a: float,
    b: float,
    t0: float,
    t: float,
    cant: float,
    scale: float,
    show_field,
):
    """
    Parameters:
    ---------------
    y0: initial y (poblation, etc)
    a: first parameter
    b: second parameter
    t0: initial time
    t: final time
    cant: partitions on the temporal and spatial axis
    scale: vector size of the vector field
    """

    # y and t range
    y_values = np.linspace(y0, a / b + 0.2, cant)
    t_values = np.linspace(t0, t, cant)

    # Create a mesh of points (y,t)
    T, Y = np.meshgrid(t_values, y_values)

    # ODE definition
    dy_dt = a * Y - b * Y**2

    # ODE's Exact solution
    function = (a * y0 * np.exp(a * t_values)) / (
        b * y0 * np.exp(a * t_values) - (-a + b * y0) * np.exp(a * t0)
    )

    fig1 = go.Figure()

    if show_field:
        # Vectorial Field: dy_dt (vertical component)
        U = np.ones_like(T)  # component in t (horizontal)
        V = dy_dt  # component at y (vertical)

        # Create the vector field w/ Plotly
        fig1 = ff.create_quiver(
            T, Y, U, V, scale=scale, line=dict(color="black", width=1), showlegend=False
        )

    # Create the function
    fig1.add_trace(
        go.Scatter(
            x=t_values,
            y=function,
            # mode = 'markers+lines',
            line=dict(color="blue"),
            name="Simple Equation",
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=[0, t],
            y=[a / b, a / b],
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="limit value",
        )
    )

    # graphic labels
    fig1.update_layout(
        title={
            "text": "Vector Field of dy/dt=ay-by^2",
            "x": 0.5,
            "y": 0.98,
            "xanchor": "center",
        },
        xaxis_title="Time (t)",
        yaxis_title="Value (y)",
        width=800,
        template="plotly_white",
        margin=dict(l=10, r=10, t=65, b=0),
        legend=dict(orientation="h", y=1.08),
    )

    # Axis
    fig1.update_xaxes(
        mirror=True, showline=True, linecolor="green", gridcolor="gray", showgrid=False
    )
    fig1.update_yaxes(
        mirror=True, showline=True, linecolor="green", gridcolor="gray", showgrid=False
    )

    return fig1


def ecuacion_logistica(
    K: float,
    P0: float,
    r: float,
    t0: float,
    t: float,
    cant: float,
    scale: float,
    show_field,
):
    """
    Retorna una gráfica de la ecuacion logistica con su campo vectorial.

    Parámetros:
    -------
    - K: Capacidad de carga.
    - P0: Poblacion Inicial.
    - r: Tasa de crecimineto poblacional.
    - t0: Tiempo inicial.
    - t: Tiempo final.
    - cant: Las particiones para el eje temporal y espacial.
    - scale: Tamaño del vector del campo vectorial.
    """

    # Rango de P y t
    P_values = np.linspace(0, K + 5, cant)
    t_values = np.linspace(0, t, cant)

    # Crear una malla de puntos (P, t)
    T, P = np.meshgrid(t_values, P_values)

    # Definir la EDO
    dP_dt = r * P * (1 - P / K)

    # Solucion exacta de la Ecuación Logística
    funcion = (
        K
        * P0
        * np.exp(r * t_values)
        / (P0 * np.exp(r * t_values) + (K - P0) * np.exp(r * t0))
    )

    fig2 = go.Figure()

    if show_field:
        # Campo vectorial: dP/dt (componente vertical)
        U = np.ones_like(T)  # Componente en t (horizontal)
        V = dP_dt  # Componente en P (vertical)

        # Crear el campo de vectores con Plotly
        fig2 = ff.create_quiver(
            T, P, U, V, scale=scale, line=dict(color="black", width=1), showlegend=False
        )

    # Crear la función logística
    fig2.add_trace(
        go.Scatter(
            x=t_values,
            y=funcion,
            # mode = 'markers+lines',
            line=dict(color="blue"),
            name="Ecuación Logística",
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=[0, t],
            y=[K, K],
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Capacidad de carga",
        )
    )

    # Etiquetas para la gráfica
    fig2.update_layout(
        title={
            "text": "Campo de vectores de dP/dt = rP(1 - P/k)",
            "x": 0.5,
            "y": 0.92,
            "xanchor": "center",
        },
        xaxis_title="Tiempo (t)",
        yaxis_title="Población (P)",
        width=800,
        template="plotly_white",
        margin=dict(l=10, r=10, t=90, b=0),
        legend=dict(orientation="h", y=1.1),
    )

    # contorno a la grafica
    fig2.update_xaxes(
        mirror=True, showline=True, linecolor="green", gridcolor="gray", showgrid=False
    )
    fig2.update_yaxes(
        mirror=True, showline=True, linecolor="green", gridcolor="gray", showgrid=False
    )

    return fig2


# HOMEWORK --------- Función  prueba
"""
    1) Averiguar alguna ecuación de algún modelo, desarrollarlo con Sympy
    2) Mejorar la apariencia visual de la página
    3) Agregar un botón que me permita activar o desactivar el campo de vectores
Sugerencias --> Ecuación depredador presa
"""


def lotka_volterra_system(z, t, alpha, beta, delta, gamma):
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]


def lotka_volterra(
    alpha: float,
    beta: float,
    delta: float,
    gamma: float,
    x0: float,
    y0: float,
    t_end: float,
    cant: float,
    scale: float,
):
    """
    Plot the vector field and the solution of the predator-prey Lotka-Volterra model.

    Parameters:
    ----------
    alpha: Growth rate of prey.
    beta: Predation rate.
    delta: Growth rate of predators due to predation.
    gamma: Death rate of predators.
    x0: Initial population of prey.
    y0: Initial population of predators.
    t_end: End time.
    cant: Number of partitions for the vector field.
    scale: Size of the vectors.
    """

    # Create a mesh grid
    x_values = np.linspace(0, 1.5 * x0, cant)
    y_values = np.linspace(0, 1.8 * y0, cant)
    X, Y = np.meshgrid(x_values, y_values)

    # Define the vector field of the Lotka-Volterra equations
    dX_dt = alpha * X - beta * X * Y
    dY_dt = delta * X * Y - gamma * Y

    # Vector field
    U = dX_dt
    V = dY_dt

    # Solve the equations using scipy.odeint
    t_values = np.linspace(0, t_end, 1000)  # Time for the numerical solution
    z0 = [x0, y0]  # Initial conditions
    sol = odeint(lotka_volterra_system, z0, t_values, args=(alpha, beta, delta, gamma))
    prey = sol[:, 0]  # Prey population
    predators = sol[:, 1]  # Predator population

    # Create subplots with two rows
    fig3 = make_subplots(
        rows=2, cols=1, subplot_titles=("Vector Field", "Numerical Solution")
    )

    # Add the vector field to the first row subplot
    fig3.add_trace(
        ff.create_quiver(
            X, Y, U, V, scale=scale, line=dict(color="black", width=1)
        ).data[0],
        row=1,
        col=1,
    )

    # Add the numerical solutions (prey and predators) to the second row subplot
    fig3.add_trace(
        go.Scatter(
            x=t_values, y=prey, mode="lines", line=dict(color="blue"), name="Prey"
        ),
        row=2,
        col=1,
    )

    fig3.add_trace(
        go.Scatter(
            x=t_values,
            y=predators,
            mode="lines",
            line=dict(color="red"),
            name="Predators",
        ),
        row=2,
        col=1,
    )

    # Graph labels
    fig3.update_layout(
        title={
            "text": "Lotka-Volterra Model: Vector Field and Numerical Solution",
            "x": 0.5,
        },
        width=800,
        height=800,
        showlegend=False,
        template="plotly_white",
    )

    # Adjust axes of both subplots
    fig3.update_xaxes(title_text="Prey population (x)", row=1, col=1)
    fig3.update_yaxes(title_text="Predator population (y)", row=1, col=1)

    fig3.update_xaxes(title_text="Time", row=2, col=1)
    fig3.update_yaxes(title_text="Population", row=2, col=1)

    return fig3
