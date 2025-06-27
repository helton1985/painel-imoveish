
import streamlit as st
import pandas as pd
from io import BytesIO
from urllib.parse import quote

# Função para gerar link WhatsApp com mensagem personalizada
def gerar_link_whatsapp(row):
    msg = f"""Olá {row['nome']}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {row['endereco']}, nº {row['numero']}, apto {row['apto']}%0a💰 Valor de venda: R$ {row['venda']}%0a🏢 Condomínio: R$ {row['cond']}%0a📄 IPTU: R$ {row['iptu']}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aAgradeço desde já pela atenção."""
    return f"https://wa.me/55{row['telefone']}?text={quote(msg)}"

# Login
def login():
    st.title("Painel ImóveisH - Login")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == "helton1985" and password == "Indira1986@":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha inválidos.")

# Painel principal com upload
def painel():
    st.title("Painel ImóveisH - Validação de Imóveis via Excel")
    st.markdown("📤 Faça upload de uma planilha `.xlsx` com os seguintes campos obrigatórios:")
    st.code("nome, telefone, endereco, numero, apto, venda, cond, iptu")
    uploaded_file = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"{len(df)} imóveis carregados com sucesso!")
            for idx, row in df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{row['nome']}** - {row['endereco']}, nº {row['numero']}, apto {row['apto']}")
                with col2:
                    url = gerar_link_whatsapp(row)
                    st.link_button("Enviar WhatsApp", url, use_container_width=True)
        except Exception as e:
            st.error("Erro ao processar o arquivo. Verifique se todos os campos estão corretos.")

# Execução
if "logado" not in st.session_state:
    login()
else:
    painel()
