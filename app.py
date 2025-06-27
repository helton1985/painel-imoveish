
import streamlit as st
import pandas as pd
from io import BytesIO
from urllib.parse import quote

# Sessão de login
def login():
    st.title("Painel ImóveisH - Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == "helton1985" and senha == "Indira1986@":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha inválidos.")

# Gera o link de WhatsApp
def gerar_link(d):
    msg = f"""Olá {d['nome']}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a
Verificamos que você possui um imóvel cadastrado com as seguintes informações:%0a
📍 Endereço: {d['endereco']}, nº {d['numero']}, apto {d['apto']}%0a
💰 Valor de venda: R$ {d['venda']}%0a🏢 Condomínio: R$ {d['cond']}%0a📄 IPTU: R$ {d['iptu']}%0a%0a
Gostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a
Agradeço desde já pela atenção."""
    return f"https://wa.me/55{d['telefone']}?text={quote(msg)}"

# Gera botão de download da planilha
def baixar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button("📥 Baixar Excel Atual", output.getvalue(), file_name="imoveis_atual.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Interface principal
def painel():
    st.title("Painel ImóveisH - Validação de Imóveis")
    arquivo = st.file_uploader("📤 Enviar planilha Excel dos imóveis", type=["xlsx"])
    if arquivo:
        df = pd.read_excel(arquivo)
        baixar_excel(df)
        for i, row in df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['nome']}** - {row['endereco']}, nº {row['numero']}, apto {row['apto']}")
            with col2:
                url = gerar_link(row)
                st.link_button("Enviar WhatsApp", url, use_container_width=True)

# Execução principal
if "logado" not in st.session_state:
    login()
else:
    painel()
