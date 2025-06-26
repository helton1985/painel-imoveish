import streamlit as st
import pandas as pd

def login():
    st.image("logo_imoveish.png", width=200)
    st.title("Login - Painel ImoveisH")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == "helton1985" and senha == "Indira1986@":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha incorretos.")

def painel():
    st.sidebar.image("logo_imoveish.png", width=150)
    st.sidebar.success("Logado como: helton1985")
    st.title("Painel - Envio Automático WhatsApp")

    uploaded_file = st.file_uploader("Upload de planilha (.xlsx)", type="xlsx")
    freq = st.selectbox("Frequência de envio (segundos)", options=list(range(1, 61)))
    numero_base = st.text_input("Número de WhatsApp base", value="11992979858")

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("Arquivo carregado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

if "logado" not in st.session_state or not st.session_state["logado"]:
    login()
else:
    painel()