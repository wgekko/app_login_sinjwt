import streamlit as st
from auth import authenticate
from utils import login_user, apply_custom_style, show_logo

st.set_page_config(page_title="App-Login", layout="centered", initial_sidebar_state="collapsed")
apply_custom_style()


if "user" in st.session_state:
    st.switch_page("pages/1_Redes Neuronales.py")


show_logo()
st.title("🔐 Inicio de Sesión")

username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Iniciar sesión"):
    role = authenticate(username, password)
    if role:
        login_user(username, role)
        st.success("Login exitoso" , icon=":material/check:")
        st.switch_page("pages/1_Redes Neuronales.py")
    else:
        st.error("Credenciales inválidas", icon=":material/close:" )


