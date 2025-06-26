
import streamlit as st
import pandas as pd
import time
from login_utils import autenticar_usuario

st.set_page_config(page_title="Painel ImoveisH", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'usuario' not in st.session_state:
    st.session_state.usuario = ""

def login():
    st.image("logo_imoveish.png", width=200)
    st.title("Login - Painel ImoveisH")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(username, password):
            st.session_state.logged_in = True
            st.session_state.usuario = username
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def painel():
    st.sidebar.success(f"Logado como: {st.session_state.usuario}")
    st.title("Envio Automático - ImoveisH")
    uploaded_file = st.file_uploader("Enviar planilha Excel", type=["xlsx"])
    tempo_envio = st.selectbox("Frequência de envio (segundos)", [1, 2, 3, 4, 5, 10, 15, 20, 30, 60])
    celular_base = st.text_input("Número de WhatsApp base", value="11992979858")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Pré-visualização da planilha:")
        st.dataframe(df)

        if st.button("Iniciar Envio"):
            for idx, row in df.iterrows():
                nome = row.get("Proprietário", "")
                endereco = row.get("Endereço", "")
                numero = row.get("Número", "")
                apto = row.get("apto", "")
                venda = row.get("Valor Venda", "")
                cond = row.get("Valor Condomínio", "")
                iptu = row.get("Valor IPTU", "")
                celular = row.get("Celular/Telefone", "")

                msg = f"Olá {nome}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {endereco}, nº {numero}, apto {apto}%0a💰 Valor de venda: R$ {venda}%0a🏢 Condomínio: R$ {cond}%0a📄 IPTU: R$ {iptu}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aCaso esteja disponível, podemos continuar com a divulgação para noss...
                link = f"https://wa.me/55{str(celular)}?text={msg}"
                st.markdown(f"[Abrir mensagem para {nome}]({link})", unsafe_allow_html=True)
                time.sleep(tempo_envio)

if not st.session_state.logged_in:
    login()
else:
    painel()
