import bcrypt
# Simulación de usuarios con contraseñas cifradas y roles
# users.py

USUARIOS = {
    "admin": {
        "password": "admin123",  # Contraseña (en la práctica debería estar cifrada)
        "role": "admin"
    },
    "editor": {
        "password": "user123",
        "role": "usuario1"
    },
    "viewer": {
        "password": "user234",
        "role": "usuario2"
    }
}

def get_user(username):
    return USUARIOS.get(username)



