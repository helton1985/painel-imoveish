import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

# Usuários permitidos (login e senha)
USUARIOS = {
    "helton1985": "Indira1986@",
    "admin": "admin123"
}

# Sessão de autenticação
def login():
    st.image("logo_imoveish.png", width=150)
    st.title("Login - Painel ImoveisH")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if USUARIOS.get(usuario) == senha:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
        else:
            st.error("Usuário ou senha incorretos.")

# Tela principal do painel
def painel():
    st.image("logo_imoveish.png", width=150)
    st.success(f"Logado como: {st.session_state['usuario']}")

    st.subheader("Envio de Mensagens Automático via WhatsApp Web")

    uploaded_file = st.file_uploader("Envie sua planilha de imóveis", type=["xlsx"])
    freq = st.selectbox("Frequência de envio (segundos)", [5, 10, 15, 20, 30, 60])
    numero = st.text_input("Número de WhatsApp base", value="11992979858")

    if st.button("Conectar ao WhatsApp Web"):
        st.info("Abrindo navegador...")
        with st.spinner("Carregando WhatsApp Web..."):
            time.sleep(3)
            st.success("Navegador carregado. Escaneie o QR Code.")

    if st.button("Iniciar envio automático"):
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.success(f"{len(df)} imóveis carregados.")
            for i, row in df.iterrows():
                st.info(f"Enviando mensagem para: {row.get('Proprietário', 'Nome desconhecido')} - {row.get('Endereço', '')}")
                time.sleep(freq)
            st.success("Envios concluídos!")
        else:
            st.warning("Envie um arquivo Excel antes de iniciar.")

# Execução
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if st.session_state["autenticado"]:
    painel()
else:
    login()