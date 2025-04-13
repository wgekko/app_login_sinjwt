import streamlit as st
import time
from datetime import datetime
import os

def login_user(username, role):
    st.session_state.user = username
    st.session_state.role = role
    st.session_state.login_time = time.time()
    st.session_state.token = {
        "exp": time.time() + 300,
        "refresh": time.time() + 150,
    }

def refresh_token():
    if "token" in st.session_state:
        if time.time() < st.session_state.token["refresh"]:
            st.session_state.token["exp"] = time.time() + 300

def is_token_expired():
    return "token" not in st.session_state or time.time() > st.session_state.token["exp"]

def require_auth(roles):
    if "user" not in st.session_state or "role" not in st.session_state:
        st.switch_page("app.py")

    if is_token_expired():
        st.warning("Sesión expirada. Redirigiendo al login...", icon=":material/warning:")
        st.session_state.clear()
        st.switch_page("app.py")

    refresh_token()

    if st.session_state.get("role") not in roles:
        st.error("Acceso denegado: No tienes permiso para ver esta página.", icon=":material/error:")
        st.stop()

    # Mostrar logout solo después de login
    with st.sidebar:
        st.write("---")        
        st.markdown(f"**Usuario:** `{st.session_state.user}`")
        st.markdown(f"**Rol :** `{st.session_state.role}`")
        st.markdown(f"**Inicio Sesión :** `{datetime.fromtimestamp(st.session_state.login_time).strftime('%H:%M:%S')}`")
        st.markdown(f"**Sesión Expira :** `{datetime.fromtimestamp(st.session_state.token['exp']).strftime('%H:%M:%S')}`")
        st.write("---") 
        if st.button("Cerrar sesión", icon=":material/logout:"):
            st.session_state.clear()
            st.switch_page("app.py")            
           
        st.sidebar.image("img/main-page.jpg",use_container_width=True)    

def apply_custom_style():
    with open("asset/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# LOGO SEGÚN ROL
def show_logo_by_role():
    if "role" not in st.session_state:
        return

    role = st.session_state.role
    logo_map = {
        "admin": "img/usuario-administrador.gif",
        "usuario1": "img/user1.gif",
        "usuario2": "img/user2.gif",
    }

    logo_path = logo_map.get(role)

    # Verifica si el archivo existe antes de mostrarlo
    if logo_path and os.path.exists(logo_path):
        st.image(logo_path, caption=None, width=60, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)
    else:
        st.warning("No se pudo cargar el logo para este rol.", icon=":material/warning:")

def show_logo():
    st.image("img/login-usuario.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)
 
def show_login_logo():
    st.image("img/login-usuario.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)

def show_logo_red_neuronal():
    st.image("img/inteligencia-artificial.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)
        
def show_logo_arbol_decision():
    st.image("img/arbol-decision.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)

def show_logo_gaussiana():
    st.image("img/histograma.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)
                
def show_logo_calibracion():
    st.image("img/neuronal_1.gif", caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=False)
                
                 
    