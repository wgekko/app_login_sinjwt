import streamlit as st
from utils import require_auth, apply_custom_style, show_logo_by_role, show_logo_calibracion
import base64
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from sklearn.calibration import CalibrationDisplay, CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")


st.set_page_config(page_title="Calibracióon",  page_icon="img/logo2.png",
                   layout="wide", initial_sidebar_state="expanded")

#st.set_page_config(page_title="Nombre Página", layout="wide", initial_sidebar_state="expanded")

require_auth(["admin"])
#add_local_sidebar_image("img/fondo.jpg")
apply_custom_style()

show_logo_by_role()
st.subheader(f"Bienvenido a Calibración : `{st.session_state.user}`.")

show_logo_calibracion()
st.header('Calibración')

st.subheader('Curvas de calibración de probabilidad')
# Definimos los parámetros de configuración de la aplicación
# Datos
X, y = make_classification(
    n_samples=100_000, n_features=20, n_informative=2, n_redundant=10, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.99, random_state=42
)

# Primera parte: Naive Bayes y Regresión Logística
lr = LogisticRegression(C=1.0)
gnb = GaussianNB()
gnb_isotonic = CalibratedClassifierCV(gnb, cv=2, method="isotonic")
gnb_sigmoid = CalibratedClassifierCV(gnb, cv=2, method="sigmoid")

clf_list_nb = [
    (lr, "Logistic"),
    (gnb, "Naive Bayes"),
    (gnb_isotonic, "Naive Bayes + Isotonic"),
    (gnb_sigmoid, "Naive Bayes + Sigmoid"),
]

colors = plt.get_cmap("Dark2")

# Parte Naive Bayes + Logística
fig_nb = plt.figure(figsize=(7, 6))  # Reducido desde (10, 6)
gs_nb = GridSpec(4, 2, figure=fig_nb)
ax_calibration_curve_nb = fig_nb.add_subplot(gs_nb[:2, :2])
calibration_displays_nb = {}

for i, (clf, name) in enumerate(clf_list_nb):
    clf.fit(X_train, y_train)
    display = CalibrationDisplay.from_estimator(
        clf,
        X_test,
        y_test,
        n_bins=10,
        name=name,
        ax=ax_calibration_curve_nb,
        color=colors(i),
    )
    calibration_displays_nb[name] = display

ax_calibration_curve_nb.grid()
ax_calibration_curve_nb.set_title("Calibration plots (Naive Bayes + Logistic)")

grid_positions = [(2, 0), (2, 1), (3, 0), (3, 1)]
for i, (_, name) in enumerate(clf_list_nb):
    row, col = grid_positions[i]
    ax = fig_nb.add_subplot(gs_nb[row, col])
    ax.hist(
        calibration_displays_nb[name].y_prob,
        range=(0, 1),
        bins=10,
        label=name,
        color=colors(i),
    )
    ax.set(title=name, xlabel="Mean predicted probability", ylabel="Count")

fig_nb.tight_layout(pad=2.0)  # Ajustado para más compacidad
st.header("Gráficos de calibración - Naive Bayes y Regresión Logística")
st.pyplot(fig_nb)

# Segunda parte: Linear SVC

class NaivelyCalibratedLinearSVC(LinearSVC):
    def fit(self, X, y):
        super().fit(X, y)
        df = self.decision_function(X)
        self.df_min_ = df.min()
        self.df_max_ = df.max()

    def predict_proba(self, X):
        df = self.decision_function(X)
        calibrated_df = (df - self.df_min_) / (self.df_max_ - self.df_min_)
        proba_pos_class = np.clip(calibrated_df, 0, 1)
        proba_neg_class = 1 - proba_pos_class
        return np.c_[proba_neg_class, proba_pos_class]

lr = LogisticRegression(C=1.0)
svc = NaivelyCalibratedLinearSVC(max_iter=10_000)
svc_isotonic = CalibratedClassifierCV(svc, cv=2, method="isotonic")
svc_sigmoid = CalibratedClassifierCV(svc, cv=2, method="sigmoid")

clf_list_svc = [
    (lr, "Logistic"),
    (svc, "SVC"),
    (svc_isotonic, "SVC + Isotonic"),
    (svc_sigmoid, "SVC + Sigmoid"),
]

# Parte SVC
fig_svc = plt.figure(figsize=(7, 6))  # Reducido también
gs_svc = GridSpec(4, 2, figure=fig_svc)
ax_calibration_curve_svc = fig_svc.add_subplot(gs_svc[:2, :2])
calibration_displays_svc = {}

for i, (clf, name) in enumerate(clf_list_svc):
    clf.fit(X_train, y_train)
    display = CalibrationDisplay.from_estimator(
        clf,
        X_test,
        y_test,
        n_bins=10,
        name=name,
        ax=ax_calibration_curve_svc,
        color=colors(i),
    )
    calibration_displays_svc[name] = display

ax_calibration_curve_svc.grid()
ax_calibration_curve_svc.set_title("Calibration plots (SVC)")

for i, (_, name) in enumerate(clf_list_svc):
    row, col = grid_positions[i]
    ax = fig_svc.add_subplot(gs_svc[row, col])
    ax.hist(
        calibration_displays_svc[name].y_prob,
        range=(0, 1),
        bins=10,
        label=name,
        color=colors(i),
    )
    ax.set(title=name, xlabel="Mean predicted probability", ylabel="Count")

fig_svc.tight_layout(pad=2.0)  # Igual aquí
st.header("Gráficos de calibración - SVC")
st.pyplot(fig_svc)


# --------------- footer -----------------------------
st.write("---")
with st.container():
    # st.write("---")
    st.write("&copy; - derechos reservados -  2025 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
    # st.write("##")
    left, right = st.columns(2, gap='medium', vertical_alignment="bottom")
    with left:
        # st.write('##')
        st.link_button(
            "Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-datascience-businessintelligence-finanzas-python/", use_container_width=False)
    with right:
       # st.write('##')
        st.link_button(
            "Mi Porfolio", "https://walter-portfolio-animado.netlify.app/", use_container_width=False)
