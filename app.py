
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Painel ImóveisH - Validação", layout="wide")

st.title("Painel ImóveisH - Validação de Imóveis via Excel")

st.markdown("📂 Faça upload da planilha (.xlsx) com os seguintes campos obrigatórios:")
st.code("nome, telefone, endereco, numero, apto, venda, cond, iptu")

def telefone_valido(telefone):
    if isinstance(telefone, str):
        telefone = ''.join(filter(str.isdigit, telefone))
    return telefone.startswith("55") and 11 <= len(telefone) <= 13

def gerar_mensagem(row):
    msg = (
        f"Olá {row['nome']}, tudo bem?%0a%0a"
        "Sou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0a"
        "Verificamos que você possui um imóvel cadastrado com as seguintes informações:%0a"
        f"📍 Endereço: {row['endereco']}, nº {row['numero']}, apto {row['apto']}%0a"
        f"💰 Valor de venda: R$ {row['venda']}%0a"
        f"🏢 Condomínio: R$ {row['cond']}%0a"
        f"📄 IPTU: R$ {row['iptu']}%0a%0a"
        "Gostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0a"
        "Agradeço desde já pela atenção."
    )
    return msg

uploaded_file = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"{len(df)} imóveis carregados com sucesso!")
        for idx, row in df.iterrows():
            telefone = str(row["telefone"])
            endereco = f"{row['endereco']}, nº {row['numero']}, apto {row['apto']}"
            if telefone_valido(telefone):
                msg = gerar_mensagem(row)
                url = f"https://api.whatsapp.com/send?phone={telefone}&text={msg}"
                st.markdown(f"✅ {endereco} - [Enviar]({url})", unsafe_allow_html=True)
            else:
                st.markdown(f"❌ {endereco} - Telefone inválido")
    except Exception as e:
        st.error("Erro ao processar o arquivo. Verifique se todos os campos estão corretos.")
        st.exception(e)
