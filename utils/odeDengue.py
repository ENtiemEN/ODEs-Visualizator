import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.integrate import odeint
from plotly.subplots import make_subplots


############ MODELO PARA R0 (Numero reproductivo básico)


# Modelo de transmisión del dengue
def dengue_system(y, t, beta, psi, sigma, delta, mu, theta):
    p, q = y
    dpdt = mu * (1 - p) - beta * psi * sigma * p * q / (delta + sigma)
    dqdt = beta * psi * sigma * p * q / (delta + sigma) - (theta + mu) * q
    return [dpdt, dqdt]


def enfermedad_dengue(beta, psi, sigma, delta, mu, theta, p0, q0, t_end, cant, scale):
    """
    Graficar el campo vectorial y la solución del modelo de dengue.

    Parámetros:
    ----------
    beta, psi, sigma, delta, mu, theta: Parámetros del modelo de transmisión.
    p0: Población inicial susceptible.
    q0: Población inicial infectada.
    t_end: Tiempo final para la simulación.
    cant: Número de particiones para el campo vectorial.
    scale: Factor de escala para los vectores en el campo.
    """
    # Crear malla para el campo vectorial
    ax, bx = 0, 1
    ay, by = 0, 1
    p_values = np.linspace(ax, bx, cant)
    q_values = np.linspace(ay, by, cant)
    P, Q = np.meshgrid(p_values, q_values)

    # Definir el campo vectorial (derivadas de p y q)
    dpdt = mu * (1 - P) - beta * psi * sigma * P * Q / (delta + sigma)
    dqdt = beta * psi * sigma * P * Q / (delta + sigma) - (theta + mu) * Q

    # Crear subgráficas para el campo vectorial y la solución temporal de p y q
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Campo Vectorial con Solución Particular", "Solución Numérica"),
    )

    # Añadir el campo vectorial a la primera subgráfica
    fig.add_trace(
        ff.create_quiver(
            P, Q, dpdt, dqdt, scale=scale, line=dict(color="black", width=1)
        ).data[0],
        row=1,
        col=1,
    )

    # Puntos de equilibrio
    R0 = beta * psi * sigma / ((delta + sigma) * (theta + mu))
    eq1 = [1, 0]
    eq2 = [1 / R0, mu * (R0 - 1) / (R0 * (mu + theta))]

    # Añadir los puntos de equilibrio
    fig.add_trace(
        go.Scatter(
            x=[eq1[0], eq2[0]],
            y=[eq1[1], eq2[1]],
            mode="markers+text",
            marker=dict(symbol="star", color="red", size=10),
            text=[
                f"E1 = ({eq1[0]:.2f}, {eq1[1]:.2f})",
                f"E2 = ({eq2[0]:.2f}, {eq2[1]:.2f})",
            ],
            textposition="top center",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Resolver el sistema usando odeint
    t_eval = np.linspace(0, t_end, 500)
    sol = odeint(
        dengue_system, [p0, q0], t_eval, args=(beta, psi, sigma, delta, mu, theta)
    )

    # Solución particular
    p = sol[:, 0]
    q = sol[:, 1]

    # Añadir la trayectoria de la solución particular al primer subplot
    fig.add_trace(
        go.Scatter(
            x=p,
            y=q,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name=f"Trayectoria Particular (p0={p0:.2f}, q0={q0:.2f})",
        ),
        row=1,
        col=1,
    )

    # Añadir la solución numérica al segundo subplot
    fig.add_trace(
        go.Scatter(
            x=t_eval,
            y=p,
            mode="lines",
            line=dict(color="blue", width=2),
            name="Población Susceptible (p)",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t_eval,
            y=q,
            mode="lines",
            line=dict(color="red", width=2),
            name="Población Infectada (q)",
        ),
        row=2,
        col=1,
    )

    # Etiquetas y formato
    fig.update_layout(
        title={
            "text": f"Modelo de Dengue: Campo Vectorial y Solución Particular (R0 = {R0:.2f})",
            "x": 0.5,
        },
        width=800,
        height=800,
        showlegend=True,
        template="plotly_white",
    )

    # Ajustar los ejes
    fig.update_xaxes(title_text="Población Susceptible (p)", row=1, col=1)
    fig.update_yaxes(title_text="Población Infectada (q)", row=1, col=1)

    fig.update_xaxes(title_text="Tiempo (t)", row=2, col=1)
    fig.update_yaxes(title_text="Población", row=2, col=1)

    return fig


###########     MODELO PARA H (umbral de población)


# Definición del sistema de ecuaciones diferenciales
def mosquito_population(y, t, delta, epsilon, sigma, phi, rho, nu, K):
    x, y, z = y
    dxdt = delta * z - epsilon * x
    dydt = sigma * z - epsilon * y
    dzdt = phi * rho * y * (1 - z / K) - (delta + sigma + nu) * z
    return [dxdt, dydt, dzdt]


def poblacion_mosquito(
    delta, epsilon, sigma, phi, rho, nu, K, x0, y0, z0, t_end, cant, scale
):
    """
    Modelo de población de mosquitos (machos, hembras, inmaduros).

    Parámetros:
    - delta: Tasa de desarrollo inmaduro a macho adulto.
    - epsilon: Tasa de mortalidad de mosquitos adultos.
    - sigma: Tasa de desarrollo inmaduro a hembra adulta.
    - phi: Probabilidad de cruce entre hembras y machos.
    - rho: Número promedio de huevos fecundados por hembra.
    - nu: Tasa de muerte de mosquito en estado inmaduro (0.1 inicialmente)
    - K: Número de huevos inmaduros en todos los criaderos (1000 inicialmente)
    - x0, y0, z0: Condiciones iniciales (machos, hembras, inmaduros).
    - t_end: Tiempo total de simulación.
    - cant: Cantidad de puntos en el intervalo temporal.
    - scale: Escala del campo vectorial.

    Retorna:
    - fig: Gráfica de Plotly con la evolución temporal y el campo vectorial.
    """

    # Solución numérica del sistema
    t_eval = np.linspace(0, t_end, cant)
    sol = odeint(
        mosquito_population,
        [x0, y0, z0],
        t_eval,
        args=(delta, epsilon, sigma, phi, rho, nu, K),
    )
    X = sol[:, 0]  # Mosquitos machos
    Y = sol[:, 1]  # Mosquitos hembras
    Z = sol[:, 2]  # Mosquitos inmaduros

    # Campo vectorial
    z = np.linspace(0, 1.6 * K, 100)
    y = np.linspace(0, 1.5 * K, 100)
    zg, yg = np.meshgrid(z, y)
    dz = phi * rho * yg * (1 - zg / K) - (delta + sigma + nu) * zg
    dy = sigma * zg - epsilon * yg

    # Crear subgráficas con Plotly
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Campo Vectorial y Trayectoria", "Evolución Temporal"),
        specs=[[{"type": "scatter"}], [{"type": "xy"}]],
    )

    # Campo vectorial y trayectoria
    fig.add_trace(
        ff.create_quiver(
            zg, yg, dz, dy, scale=scale, line=dict(color="gray", width=1)
        ).data[0],
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=Z, y=Y, mode="lines", line=dict(color="green"), name="Trayectoria"
        ),
        row=1,
        col=1,
    )

    # Puntos de equilibrio
    q2_z = (
        K
        * ((sigma * phi * rho) / (epsilon * (delta + sigma + nu)) - 1)
        / ((sigma * phi * rho) / (epsilon * (delta + sigma + nu)))
    )
    q2_y = (
        (sigma * K / epsilon)
        * ((sigma * phi * rho) / (epsilon * (delta + sigma + nu)) - 1)
        / ((sigma * phi * rho) / (epsilon * (delta + sigma + nu)))
    )
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(symbol="star", size=10, color="red"),
            name="Equilibrio 1",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[q2_z],
            y=[q2_y],
            mode="markers",
            marker=dict(symbol="star", size=10, color="red"),
            name=f"Equilibrio 2 ({q2_z:.1f}, {q2_y:.1f})",
        ),
        row=1,
        col=1,
    )

    # Evolución temporal
    fig.add_trace(
        go.Scatter(
            x=t_eval, y=X, mode="lines", line=dict(color="blue"), name="Machos (x)"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t_eval, y=Y, mode="lines", line=dict(color="red"), name="Hembras (y)"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t_eval, y=Z, mode="lines", line=dict(color="green"), name="Inmaduros (z)"
        ),
        row=2,
        col=1,
    )

    # Configuración de diseño
    fig.update_layout(
        title={"text": "Modelo de Población de Mosquitos", "x": 0.5},
        width=800,
        height=800,
        showlegend=True,
        template="plotly_white",
    )
    fig.update_xaxes(title_text="Mosquitos Inmaduros (z)", row=1, col=1)
    fig.update_yaxes(title_text="Mosquitos Hembras (y)", row=1, col=1)
    fig.update_xaxes(title_text="Tiempo (t)", row=2, col=1)
    fig.update_yaxes(title_text="Población", row=2, col=1)

    return fig
