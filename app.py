
import streamlit as st
import pandas as pd
from io import BytesIO
from urllib.parse import quote

# Mapeamento de colunas alternativas
colunas_aceitas = {
    "proprietário": "nome",
    "nome": "nome",
    "celular/telefone": "telefone",
    "telefone": "telefone",
    "endereço": "endereco",
    "endereco": "endereco",
    "número": "numero",
    "numero": "numero",
    "apto": "apto",
    "valor_venda": "venda",
    "venda": "venda",
    "valor_condomínio": "cond",
    "r_condom": "cond",
    "cond": "cond",
    "valor_iptu": "iptu",
    "iptu": "iptu"
}

# Gerar link WhatsApp
def gerar_link_whatsapp(row):
    msg = f"""Olá {row['nome']}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {row['endereco']}, nº {row['numero']}, apto {row['apto']}%0a💰 Valor de venda: R$ {row['venda']}%0a🏢 Condomínio: R$ {row['cond']}%0a📄 IPTU: R$ {row['iptu']}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aAgradeço desde já pela atenç...
    return f"https://wa.me/55{row['telefone']}?text={quote(msg)}"

# Padronizar colunas
def padronizar_colunas(df):
    colunas_novas = {}
    for col in df.columns:
        key = col.strip().lower()
        key = key.replace("ã", "a").replace("á", "a").replace("é", "e").replace("ê", "e").replace("í", "i").replace("ô", "o").replace("ó", "o").replace("ú", "u").replace("/", "_")
        if key in colunas_aceitas:
            colunas_novas[col] = colunas_aceitas[key]
    df = df.rename(columns=colunas_novas)
    return df

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

# Painel com upload
def painel():
    st.title("Painel ImóveisH - Validação de Imóveis via Excel")
    uploaded_file = st.file_uploader("📤 Faça upload da planilha (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df = padronizar_colunas(df)
            obrigatorias = ["nome", "telefone", "endereco", "numero", "apto", "venda", "cond", "iptu"]
            if not all(col in df.columns for col in obrigatorias):
                st.error("Planilha inválida. Verifique se os campos obrigatórios estão presentes.")
                return
            st.success(f"{len(df)} imóveis carregados com sucesso!")
            for _, row in df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{row['nome']}** - {row['endereco']}, nº {row['numero']}, apto {row['apto']}")
                with col2:
                    url = gerar_link_whatsapp(row)
                    st.link_button("Enviar WhatsApp", url, use_container_width=True)
        except Exception as e:
            st.error("Erro ao processar o arquivo. Verifique se a planilha está no formato correto.")

# Execução
if "logado" not in st.session_state:
    login()
else:
    painel()
