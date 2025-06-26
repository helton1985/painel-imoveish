
import streamlit as st
import pandas as pd

def painel():
    st.title("Painel ImoveisH - Validação de Imóveis via WhatsApp")

    frequencia_envio = st.text_input("Frequência de envio (segundos)", value="5")
    numero_base = st.text_input("Número de WhatsApp base", value="11992979858")

    conectado = st.button("Conectar ao WhatsApp Web")
    iniciar_envio = st.button("Iniciar envio automático")

    if conectado:
        st.success("Conectado ao WhatsApp Web (simulado)")

    uploaded_file = st.file_uploader("Envie a base de imóveis (.xlsx)", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())

        for index, row in df.iterrows():
            nome = row.get("Proprietário", "Proprietário")
            endereco = row.get("Endereço", "Rua desconhecida")
            numero = row.get("Número", "S/N")
            apto = row.get("apto", "")
            venda = row.get("Valor Venda", "")
            cond = row.get("Valor Condomínio", "")
            iptu = row.get("Valor IPTU", "")

            msg = (
                f"Olá {nome}, tudo bem?%0a%0a"
                f"Sou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0a"
                f"Verificamos que você possui um imóvel cadastrado com as seguintes informações:%0a"
                f"📍 Endereço: {endereco}, nº {numero}, apto {apto}%0a"
                f"💰 Valor de venda: R$ {venda}%0a"
                f"🏢 Condomínio: R$ {cond}%0a"
                f"📄 IPTU: R$ {iptu}%0a%0a"
                f"Gostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0a"
                f"Caso esteja disponível, podemos continuar com a divulgação para nossos clientes interessados."
            )

            st.text_area(f"Mensagem para {nome}", value=msg, height=200)

painel()
