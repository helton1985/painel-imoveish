
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

st.set_page_config(page_title="ImóveisH - Envio WhatsApp", layout="centered")

st.title("Imóveis via WhatsApp")

frequencia = st.number_input("Frequência de envio (segundos)", min_value=1, value=5)
numero_base = st.text_input("Número de WhatsApp base", value="11992979858")

if "whatsapp_connected" not in st.session_state:
    st.session_state["whatsapp_connected"] = False

def conectar_whatsapp():
    try:
        service = Service(executable_path="chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=chrome-data")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://web.whatsapp.com")
        st.success("Navegador iniciado. Faça login no WhatsApp Web.")
        st.session_state["driver"] = driver
        st.session_state["whatsapp_connected"] = True
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")

if not st.session_state["whatsapp_connected"]:
    if st.button("Conectar ao WhatsApp Web"):
        conectar_whatsapp()

if st.session_state["whatsapp_connected"]:
    st.success("Conectado ao WhatsApp Web.")

    uploaded_file = st.file_uploader("Envie a base de imóveis (.xlsx)", type="xlsx")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write(df.head())

        if st.button("Iniciar envio automático"):
            for index, row in df.iterrows():
                nome = row["proprietario"]
                endereco = row["endereco"]
                numero = row["numero"]
                apto = row["apto"]
                venda = row["venda"]
                cond = row["condominio"]
                iptu = row["iptu"]
                telefone = row["telefone"]

                msg = f"Olá {nome}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {endereco}, nº {numero}, apto {apto}%0a💰 Valor de venda: R$ {venda}%0a🏢 Condomínio: R$ {cond}%0a📄 IPTU: R$ {iptu}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aCaso esteja disponível, podemos continuar com a divulgação para nossos clientes interessados."

                link = f"https://web.whatsapp.com/send?phone=55{telefone}&text={msg}"
                st.session_state["driver"].get(link)
                time.sleep(frequencia)

            st.success("Mensagens enviadas com sucesso.")
