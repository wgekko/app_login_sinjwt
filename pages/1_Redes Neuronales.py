import streamlit as st
from utils import require_auth, apply_custom_style, show_logo
from utils import require_auth, apply_custom_style, show_logo_by_role, show_logo_red_neuronal
import matplotlib.pyplot as plt
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_digits
import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

st.set_page_config(page_title="Redes Neuronales", page_icon="img/logo2.png", layout="wide", initial_sidebar_state="expanded")
#st.set_page_config(page_title="Nombre Página", layout="wide", initial_sidebar_state="expanded")

require_auth(["admin", "usuario1", "usuario2"])
apply_custom_style()

show_logo_by_role() 
#st.title("Página de Inicio")
st.subheader(f"Bienvenido a Redes Neuronales : `{st.session_state.user}`.")

# st.header(':red[Redes Neuronales]') # si se buscar cambiar de color del titulo
show_logo_red_neuronal()
st.header('Redes Neuronales')
st.write("---")
st.subheader('Comparar estrategias de aprendizaje estocástico para MLPClassifier')
st.warning("Authors: The scikit-learn developers # SPDX-License-Identifier: BSD-3-Clause") 
        


st.header("Visualización de Estrategias de Aprendizaje y Regularización")

# Parámetros para los modelos MLP
params = [
    {"solver": "sgd", "learning_rate": "constant", "momentum": 0, "learning_rate_init": 0.2},
    {"solver": "sgd", "learning_rate": "constant", "momentum": 0.9, "nesterovs_momentum": False, "learning_rate_init": 0.2},
    {"solver": "sgd", "learning_rate": "constant", "momentum": 0.9, "nesterovs_momentum": True, "learning_rate_init": 0.2},
    {"solver": "sgd", "learning_rate": "invscaling", "momentum": 0, "learning_rate_init": 0.2},
    {"solver": "sgd", "learning_rate": "invscaling", "momentum": 0.9, "nesterovs_momentum": False, "learning_rate_init": 0.2},
    {"solver": "sgd", "learning_rate": "invscaling", "momentum": 0.9, "nesterovs_momentum": True, "learning_rate_init": 0.2},
    {"solver": "adam", "learning_rate_init": 0.01},
]

labels = [
    "constant learning-rate",
    "constant with momentum",
    "constant with Nesterov's momentum",
    "inv-scaling learning-rate",
    "inv-scaling with momentum",
    "inv-scaling with Nesterov's momentum",
    "adam",
]

plot_args = [
    {"c": "red", "linestyle": "-"},
    {"c": "green", "linestyle": "-"},
    {"c": "blue", "linestyle": "-"},
    {"c": "red", "linestyle": "--"},
    {"c": "green", "linestyle": "--"},
    {"c": "blue", "linestyle": "--"},
    {"c": "black", "linestyle": "-"},
]

def plot_on_dataset(X, y, name):
    st.write(f"### Dataset: {name}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title(f"Loss curves - {name}")

    # Normalizamos los datos
    X = MinMaxScaler().fit_transform(X)
    mlps = []
    max_iter = 15 if name.lower() == "digits" else 400

    for param in params:
        mlp = MLPClassifier(random_state=0, max_iter=max_iter, **param)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ConvergenceWarning)
            mlp.fit(X, y)
        mlps.append(mlp)

    for mlp, label, args in zip(mlps, labels, plot_args):
        ax.plot(mlp.loss_curve_, label=label, **args)

    ax.legend(loc="best")
    fig.tight_layout()
    st.pyplot(fig)

    # Mostrar el loss final de cada modelo
    st.subheader("Pérdida final de cada modelo:")
    for label, mlp in zip(labels, mlps):
        st.write(f"{label}: {mlp.loss_:.4f}")

def main():
    st.subheader("Comparación de MLP con diferentes configuraciones de entrenamiento")
   # Cargar ambos datasets
    iris_data = load_iris()
    digits_data = load_digits()
    # Mostrar ambos gráficos uno debajo del otro
    plot_on_dataset(iris_data.data, iris_data.target, "Iris")
    st.markdown("---")  # Separador visual
    plot_on_dataset(digits_data.data, digits_data.target, "Digits")
    
if __name__ == "__main__":
    main()

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
          