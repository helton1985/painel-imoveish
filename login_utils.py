
import json

def autenticar_usuario(username, password):
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        return usuarios.get(username) == password
    except Exception:
        return False
