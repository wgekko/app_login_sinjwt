import streamlit as st
from utils import require_auth, apply_custom_style, show_logo_by_role, show_logo_gaussiana
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF,
    RationalQuadratic,
    ExpSineSquared,
    ConstantKernel,
    DotProduct,
    Matern,
)
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, ExpSineSquared, ConstantKernel, DotProduct, Matern
import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

st.set_page_config(page_title="Modelos Gaussiana",  page_icon="img/logo2.png", layout="wide", initial_sidebar_state="expanded")
#st.set_page_config(page_title="Nombre Página", layout="wide", initial_sidebar_state="expanded")

require_auth(["admin", "usuario2"])
apply_custom_style()

show_logo_by_role()
st.subheader(f"Bienvenido a Modelos Gaussiana : `{st.session_state.user}`.")
    

#st.header(':orange[Modelos de mezcla gaussiana]') # si se desea cambiar el color del texto
show_logo_gaussiana()
st.header('Modelos de mezcla gaussiano')

st.write("---")    
#st.subheader(':orange[Análisis de variación de tipo previo de concentración Bayesiano Gaussiano Mezcla]') # si se desea cambiar el color del texto
st.subheader('Ilustración del proceso gaussiano anterior y posterior para diferentes núcleos')
    
st.warning("Authors: The scikit-learn developers # SPDX-License-Identifier: BSD-3-Clause")
    
# Función modificada para graficar con Matplotlib y aceptar un kernel personalizado
def plot_gpr(kernel, X_train, y_train, n_samples=5, title=""):
    gpr = GaussianProcessRegressor(kernel=kernel, random_state=0)
    
    x = np.linspace(0, 5, 100)
    X = x.reshape(-1, 1)

    # PRIOR
    fig, axs = plt.subplots(nrows=2, sharex=True, sharey=True, figsize=(10, 6))

    y_prior_samples = gpr.sample_y(X, n_samples)
    for idx, sample in enumerate(y_prior_samples.T):
        axs[0].plot(x, sample, linestyle="--", alpha=0.7, label=f"Sample #{idx + 1}")
    axs[0].set_title("Prior")
    axs[0].set_ylim([-3, 3])

    # POSTERIOR
    gpr.fit(X_train, y_train)
    y_mean, y_std = gpr.predict(X, return_std=True)
    y_samples = gpr.sample_y(X, n_samples)

    for idx, sample in enumerate(y_samples.T):
        axs[1].plot(x, sample, linestyle="--", alpha=0.7, label=f"Sample #{idx + 1}")
    axs[1].plot(x, y_mean, color="black", label="Mean")
    axs[1].fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.1, color="black", label=r"$\pm$ 1 std. dev.")
    axs[1].scatter(X_train[:, 0], y_train, color="red", zorder=10, label="Observations")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Posterior")
    axs[1].set_ylim([-3, 3])

    fig.suptitle(title, fontsize=18)
    st.pyplot(fig)

# Datos
rng = np.random.RandomState(4)
X_train = rng.uniform(0, 5, 10).reshape(-1, 1)
y_train = np.sin((X_train[:, 0] - 2.5) ** 2)
n_samples = 5

st.title("Gaussian Process Regression with Different Kernels")

# 1. RBF Kernel
plot_gpr(
    kernel=1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)),
    X_train=X_train,
    y_train=y_train,
    n_samples=n_samples,
    title="Radial Basis Function Kernel"
)

# 2. Rational Quadratic Kernel
plot_gpr(
    kernel=1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1, alpha_bounds=(1e-5, 1e15)),
    X_train=X_train,
    y_train=y_train,
    n_samples=n_samples,
    title="Rational Quadratic Kernel"
)

# 3. Exp-Sine-Squared Kernel
plot_gpr(
    kernel=1.0 * ExpSineSquared(length_scale=1.0, periodicity=3.0,
                                length_scale_bounds=(0.1, 10.0),
                                periodicity_bounds=(1.0, 10.0)),
    X_train=X_train,
    y_train=y_train,
    n_samples=n_samples,
    title="Exp-Sine-Squared Kernel"
)

# 4. Dot Product Kernel
plot_gpr(
    kernel=ConstantKernel(0.1, (0.01, 10.0)) * (
        DotProduct(sigma_0=1.0, sigma_0_bounds=(0.1, 10.0)) ** 2
    ),
    X_train=X_train,
    y_train=y_train,
    n_samples=n_samples,
    title="Dot Product Kernel"
)

# 5. Matérn Kernel
plot_gpr(
    kernel=1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0), nu=1.5),
    X_train=X_train,
    y_train=y_train,
    n_samples=n_samples,
    title="Matérn Kernel"
)


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
      

