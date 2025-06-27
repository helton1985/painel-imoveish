
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Painel ImóveisH - Validação de Imóveis via Excel", layout="wide")
st.title("Painel ImóveisH - Validação de Imóveis via Excel")

st.markdown("📂 Faça upload de uma planilha `.xlsx` com os seguintes campos obrigatórios:")
st.code("nome, telefone, endereco, numero, apto, venda, cond, iptu")

uploaded_file = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    expected_columns = ["nome", "telefone", "endereco", "numero", "apto", "venda", "cond", "iptu"]

    if all(col in df.columns for col in expected_columns):
        st.success(f"{len(df)} imóveis carregados com sucesso!")

        for _, row in df.iterrows():
            nome = str(row["nome"])
            telefone = str(row["telefone"])
            endereco = str(row["endereco"])
            numero = str(row["numero"])
            apto = str(row["apto"])
            venda = str(row["venda"])
            cond = str(row["cond"])
            iptu = str(row["iptu"])

            msg = f"Olá {nome}, tudo bem?\n\nSou o corretor Helton da ImoveisH (www.imoveish.com.br).\n\nVerificamos que você possui um imóvel cadastrado com as seguintes informações:\n📍 Endereço: {endereco}, nº {numero}, apto {apto}\n💰 Valor de venda: R$ {venda}\n🏢 Condomínio: R$ {cond}\n📄 IPTU: R$ {iptu}\n\nGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.\n\nAgradeço desde já pela atenção."
            encoded_msg = urllib.parse.quote(msg)
            url = f"https://api.whatsapp.com/send?phone=55{telefone}&text={encoded_msg}"

            st.markdown(f"✅ **{endereco}**, nº {numero}, apto {apto} — [📤 Enviar mensagem]({url})")
    else:
        st.error("Erro ao processar o arquivo. Verifique se todos os campos estão corretos.")
