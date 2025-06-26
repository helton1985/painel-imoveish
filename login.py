
import streamlit as st

def login():
    st.title("Login - Painel ImoveisH")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "helton1985" and password == "Indira1986@":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha incorretos.")
