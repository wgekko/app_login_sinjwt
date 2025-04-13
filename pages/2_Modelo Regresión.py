import streamlit as st
from utils import require_auth,  apply_custom_style,show_logo_by_role, show_logo_arbol_decision
import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

st.set_page_config(page_title="Modelo de Regresión",  page_icon="img/logo2.png", layout="wide", initial_sidebar_state="expanded")

 
#add_local_sidebar_image("img/fondo.jpg")
require_auth(["admin", "usuario1"])
apply_custom_style()

show_logo_by_role()  
st.subheader(f"Bienvenido a Modelo de Regresión : `{st.session_state.user}`.")

#st.header(':green[Árboles de decisión ]') # si se desea cambiar el color del titulo
#st.subheader(':green[Regresión del árbol de decisión ]') # si se desea cambiar el color del titulo
show_logo_arbol_decision()    
st.header('Modelos de Regresión')
st.subheader('Comparación de la regresión de cresta del núcleo y SVR')    
    
# crecion de datos aleatorios 
st.warning("Authors: The scikit-learn developers # SPDX-License-Identifier: BSD-3-Clause")

# =========================
# 1. Generación de datos base
# =========================
rng = np.random.default_rng(seed=42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = X.ravel() * np.sin(X.ravel())

# Datos de entrenamiento
X_train = np.linspace(0, 10, 10).reshape(-1, 1)
y_train = X_train.ravel() * np.sin(X_train.ravel())

# ============
# Gráfico 1: Generación de datos
# ============
st.subheader("1. Generación de Datos")
fig1, ax1 = plt.subplots()
ax1.plot(X, y, label=r"$f(x) = x \sin(x)$", color="tab:orange")
ax1.set_xlabel("$x$")
ax1.set_ylabel("$f(x)$")
ax1.set_title("Función base sin ruido")
ax1.legend()
st.pyplot(fig1)

# ============
# Gráfico 2: Datos con ruido
# ============
st.subheader("2. Observaciones con Ruido")
noise_std_base = 0.5
y_train_noisy_base = y_train + rng.normal(0, noise_std_base, size=y_train.shape)

fig2, ax2 = plt.subplots()
ax2.plot(X, y, label="Función original", linestyle="dashed", color="tab:gray")
ax2.errorbar(
    X_train.ravel(),
    y_train_noisy_base,
    noise_std_base,
    linestyle="None",
    color="tab:blue",
    marker="o",
    markersize=8,
    label="Datos ruidosos",
)
ax2.set_xlabel("$x$")
ax2.set_ylabel("$f(x)$")
ax2.set_title("Datos observados con ruido")
ax2.legend()
st.pyplot(fig2)

# ============
# Gráfico 3: Predicción simulada (sin modelo real)
# ============
st.subheader("3. Predicción simulada (sin modelo real)")
mean_prediction = X.ravel() * np.sin(X.ravel())  # Simulación
std_prediction = 0.3 * np.ones_like(mean_prediction)

fig3, ax3 = plt.subplots()
ax3.plot(X, y, label=r"$f(x) = x \sin(x)$", linestyle="dotted")
ax3.errorbar(
    X_train.ravel(),
    y_train_noisy_base,
    noise_std_base,
    linestyle="None",
    color="tab:blue",
    marker=".",
    markersize=10,
    label="Observations",
)
ax3.plot(X, mean_prediction, label="Mean prediction")
ax3.fill_between(
    X.ravel(),
    mean_prediction - 1.96 * std_prediction,
    mean_prediction + 1.96 * std_prediction,
    color="tab:orange",
    alpha=0.5,
    label=r"95% confidence interval",
)
ax3.set_xlabel("$x$")
ax3.set_ylabel("$f(x)$")
ax3.set_title("Predicción estimada con intervalo de confianza")
ax3.legend()
st.pyplot(fig3)

# ============
# Gráfico 4: Modelo real con GaussianProcessRegressor
# ============
st.subheader("4. Ejemplo con objetivos ruidosos (modelo real)")

# Nuevo ruido y entrenamiento
noise_std = 0.75
y_train_noisy = y_train + rng.normal(loc=0.0, scale=noise_std, size=y_train.shape)

# Kernel y modelo GP
kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
gaussian_process = GaussianProcessRegressor(
    kernel=kernel, alpha=noise_std**2, n_restarts_optimizer=9
)
gaussian_process.fit(X_train, y_train_noisy)
mean_prediction, std_prediction = gaussian_process.predict(X, return_std=True)

# Visualización
fig4, ax4 = plt.subplots()
ax4.plot(X, y, label=r"$f(x) = x \sin(x)$", linestyle="dotted")
ax4.errorbar(
    X_train.ravel(),
    y_train_noisy,
    noise_std,
    linestyle="None",
    color="tab:blue",
    marker=".",
    markersize=10,
    label="Observations",
)
ax4.plot(X, mean_prediction, label="Mean prediction")
ax4.fill_between(
    X.ravel(),
    mean_prediction - 1.96 * std_prediction,
    mean_prediction + 1.96 * std_prediction,
    color="tab:orange",
    alpha=0.5,
    label=r"95% confidence interval",
)
ax4.set_xlabel("$x$")
ax4.set_ylabel("$f(x)$")
ax4.set_title("Gaussian process regression on a noisy dataset")
ax4.legend()
st.pyplot(fig4)

# --------------- footer -----------------------------
st.write("---")
with st.container():
  #st.write("---")
  st.write("&copy; - derechos reservados -  2025 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
  #st.write("##")
  left, right = st.columns(2, gap='medium', vertical_alignment="bottom")
  with left:
    #st.write('##')
    st.link_button("Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-datascience-businessintelligence-finanzas-python/",use_container_width=False)
  with right: 
     #st.write('##') 
    st.link_button("Mi Porfolio", "https://walter-portfolio-animado.netlify.app/", use_container_width=False)
      
