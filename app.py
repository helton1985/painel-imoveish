
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel ImoveisH", layout="centered")

# Logo correto
st.image("logo_imoveish.png", width=200)

# Usuários cadastrados
usuarios = {
    "helton1985": "Indira1986@"
}

# Sessão de autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("Login - Painel ImoveisH")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

# Painel principal
st.title("Painel de Validação - ImoveisH")

# Upload da planilha
uploaded_file = st.file_uploader("Upload da planilha de imóveis", type=["xlsx"])
frequencia = st.selectbox("Frequência de envio (segundos)", [1, 5, 10, 30, 60])
numero = st.text_input("Número de WhatsApp base", "11992979858")

# Botões principais
col1, col2 = st.columns(2)
with col1:
    if st.button("Conectar ao WhatsApp Web"):
        st.success("Conectado ao WhatsApp Web (simulado)")
with col2:
    if st.button("Iniciar envio automático"):
        st.success(f"Envio iniciado com frequência de {frequencia} segundos (simulado)")

# Exibição do conteúdo do Excel
if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.dataframe(df.head())
