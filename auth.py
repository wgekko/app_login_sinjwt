import streamlit as st
import os
import base64
from roles import ROLES


def authenticate(username, password):
    user = ROLES.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None


#----------------------------------------------------------        
def apply_custom_style():
    css_file = "asset/style.css"
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de estilo: {css_file}", icon=":material/cancel:")

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
    logo_path = "img/tareas.gif"  # Cambia por el nombre correcto de tu gif
    st.markdown(
        f"""
        <div style='text-align:center; margin-top: 20px; animation: fadeIn 2s ease-in-out;'>
            <img src='{logo_path}' style='width:200px; border-radius:15px;' />
        </div>
        """,
        unsafe_allow_html=True
    )


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
                
      

#""" imagen de background"""
#def add_local_background_image(image):
#  with open(image, "rb") as image:
#    encoded_string = base64.b64encode(image.read())
#    st.markdown(
#      f"""
#      <style>
#      .stApp{{
#        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
#      }}    
#      </style>
#      """,
#      unsafe_allow_html=True
#    )
#add_local_background_image("img/fondo.jpg")


#""" imagen de sidebar"""
#def add_local_sidebar_image(image):
#  with open(image, "rb") as image:
#    encoded_string = base64.b64encode(image.read())
#    st.markdown(
#      f"""
#      <style>
#      .stSidebar{{
#        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
#      }}    
#      </style>
#      """,
#      unsafe_allow_html=True
#    )
    
                          