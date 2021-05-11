import scipy as sci  # Import matplotlib and associated modules for 3D and animations
import numpy as np
import scipy.integrate as integrat
import matplotlib.pyplot as plt
from io import StringIO
import PIL.Image
from matplotlib import animation
from matplotlib.animation import FuncAnimation, PillowWriter

import base64


class ThreeBody:
    # Definición constante de gravitación universal.
    G = 6.67408e-11

    # Creación de figura
    fig = plt.figure(figsize=(15, 15))

    # Trazar las orbitas
    ax = fig.add_subplot(111, projection="3d")

    def __init__(self, m_nd, r_nd, v_nd, t_nd, m, r, v, t):
        self.m_nd = m_nd  # kg #Masa
        self.r_nd = r_nd  # m #Distancia
        self.v_nd = v_nd  # m/s #Velocidad relativa
        self.t_nd = t_nd  # s #Periodo orbital

        # Constantes netas.
        self.K1 = self.G * self.t_nd * self.m_nd / (self.r_nd ** 2 * self.v_nd)
        self.K2 = self.v_nd * self.t_nd / self.r_nd

        # Definir masas
        self.m1 = m[0]  # m1
        self.m2 = m[1]  # m2
        self.m3 = m[2]  # m3

        # Definición de posición inicial de los vectores
        self.r1 = r[:3]  # m1
        self.r2 = r[3:6]  # m2
        self.r3 = r[6:9]  # m3

        # Conversión de vectores a matrices
        self.r1 = np.array(self.r1, dtype="float64")
        self.r2 = np.array(self.r2, dtype="float64")
        self.r3 = np.array(self.r3, dtype="float64")

        # Búsqueda de centro de masa
        self.r_com = (self.m1 * self.r1 + self.m2 * self.r2 + self.m3 * self.r3) / (self.m1 + self.m2 + self.m3)

        # Definición de velocidades iniciales
        self.v1 = v[:3]  # m/s
        self.v2 = v[3:6]  # m/s
        self.v3 = v[6:9]  # m/s

        # Conversión de vectores a matrices
        self.v1 = np.array(self.v1, dtype="float64")
        self.v2 = np.array(self.v2, dtype="float64")
        self.v3 = np.array(self.v3, dtype="float64")

        # Búsqueda de la velocidad del centro de masa
        self.v_com = (self.m1 * self.v1 + self.m2 * self.v2 + self.m3 * self.v3) / (self.m1 + self.m2 + self.m3)

        # Parámetros iniciales
        self.init_params = np.array([self.r1, self.r2, self.r3, self.v1, self.v2, self.v3])  # Creación de array inicial
        self.init_params = self.init_params.flatten()  # Convertir array en 1 dimesión
        self.time_span = np.linspace(0, t, t * 25)  # t periodos orbitales, t*25 puntos

        self.three_body_sol = integrat.odeint(self.ThreeBodyEquations, self.init_params,
                                              self.time_span, args=(self.G, self.m1, self.m2, self.m3))

        self.r1_sol = self.three_body_sol[:, :3]
        self.r2_sol = self.three_body_sol[:, 3:6]
        self.r3_sol = self.three_body_sol[:, 6:9]

        # Transpuesta de r1_sol
        self.data = self.r1_sol.T

        # Transpuesta de r2_sol
        self.data2 = self.r2_sol.T

        # Transpuesta de r3_sol
        self.data3 = self.r3_sol.T

        self.ax.plot(self.r1_sol[:, 0], self.r1_sol[:, 1], self.r1_sol[:, 2], alpha=0)
        self.line, = self.ax.plot(self.data[0, 0:1], self.data[1, 0:1], self.data[2, 0:1], color="darkblue")
        self.point, = self.ax.plot(self.data[0, 0:1], self.data[1, 0:1], self.data[2, 0:1], marker="o",
                                   color="darkblue")

        self.line2, = self.ax.plot(self.data2[0, 0:1], self.data2[1, 0:1], self.data2[2, 0:1], color="tab:red")
        self.point2, = self.ax.plot(self.data2[0, 0:1], self.data2[1, 0:1], self.data2[2, 0:1], marker="o",
                                    color="tab:red")

        self.line3, = self.ax.plot(self.data3[0, 0:1], self.data3[1, 0:1], self.data3[2, 0:1], color="black")
        self.point3, = self.ax.plot(self.data3[0, 0:1], self.data3[1, 0:1], self.data3[2, 0:1], marker="o",
                                    color="black")

        self.ax.set_xlabel("x-coordinate", fontsize=14)
        self.ax.set_ylabel("y-coordinate", fontsize=14)
        self.ax.set_zlabel("z-coordinate", fontsize=14)
        self.ax.set_title("Visualización de órbitas de estrellas en un sistema de tres cuerpos\n", fontsize=14)

    def Simulation(self):
        writer = PillowWriter(fps=25)

        print("Cargando...")
        anim = animation.FuncAnimation(self.fig, self.anima, len(self.time_span), interval=10000 / len(self.time_span),
                                       blit=False)
        anim.save("threeBody.gif", writer=writer)

    # Función que define las ecuaciones de movimiento
    def ThreeBodyEquations(self, w, t, G, m1, m2, m3):
        r1 = w[:3]
        r2 = w[3:6]
        r3 = w[6:9]
        v1 = w[9:12]
        v2 = w[12:15]
        v3 = w[15:18]

        # Calcula la magnitud del vector
        r12 = sci.linalg.norm(r2 - r1)
        r13 = sci.linalg.norm(r3 - r1)
        r23 = sci.linalg.norm(r3 - r2)

        dv1bydt = self.K1 * m2 * (r2 - r1) / r12 ** 3 + self.K1 * m3 * (r3 - r1) / r13 ** 3
        dv2bydt = self.K1 * m1 * (r1 - r2) / r12 ** 3 + self.K1 * m3 * (r3 - r2) / r23 ** 3
        dv3bydt = self.K1 * m1 * (r1 - r3) / r13 ** 3 + self.K1 * m2 * (r2 - r3) / r23 ** 3
        dr1bydt = self.K2 * v1
        dr2bydt = self.K2 * v2
        dr3bydt = self.K2 * v3

        r12_derivs = np.concatenate((dr1bydt, dr2bydt))
        r_derivs = np.concatenate((r12_derivs, dr3bydt))
        v12_derivs = np.concatenate((dv1bydt, dv2bydt))
        v_derivs = np.concatenate((v12_derivs, dv3bydt))
        derivs = np.concatenate((r_derivs, v_derivs))

        return derivs

    def anima(self, i):
        self.line.set_data(self.data[:2, :i])
        self.line.set_3d_properties(self.data[2, :i])
        self.point.set_data(self.data[:2, i])
        self.point.set_3d_properties(self.data[2, i])

        self.line2.set_data(self.data2[:2, :i])
        self.line2.set_3d_properties(self.data2[2, :i])
        self.point2.set_data(self.data2[:2, i])
        self.point2.set_3d_properties(self.data2[2, i])

        self.line3.set_data(self.data3[:2, :i])
        self.line3.set_3d_properties(self.data3[2, :i])
        self.point3.set_data(self.data3[:2, i])
        self.point3.set_3d_properties(self.data3[2, i])


def gif():
    with open("threeBody.gif", "rb") as image_file:
        return base64.b64encode(image_file.read())


#threeBody = ThreeBody(1.989e+30, 5.326e+12, 30000, 79.91 * 365 * 24 * 3600 * 0.51, [1.1, 0.907, 1.0],
                      #[-0.5, 0, 0, 0.5, 0, 0, 0, 1, 0], [0.01, 0.01, 0, -0.05, 0, -0.1, 0, -0.01, 0], 20)

#threeBody.Simulation()