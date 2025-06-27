
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
    nome = str(row.get("nome", "") or "")
    telefone = str(row.get("telefone", "") or "")
    endereco = str(row.get("endereco", "") or "")
    numero = str(row.get("numero", "") or "")
    apto = str(row.get("apto", "") or "")
    venda = str(row.get("venda", "") or "")
    cond = str(row.get("cond", "") or "")
    iptu = str(row.get("iptu", "") or "")

    msg = f"Olá {nome}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {endereco}, nº {numero}, apto {apto}%0a💰 Valor de venda: R$ {venda}%0a🏢 Condomínio: R$ {cond}%0a📄 IPTU: R$ {iptu}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aAgradeço desde já pela atenção."
    return f"https://wa.me/55{telefone}?text={quote(msg)}"

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

# Painel
def painel():
    st.title("Painel ImóveisH - Validação de Imóveis via Excel")
    uploaded_file = st.file_uploader("📤 Faça upload da planilha (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df = padronizar_colunas(df)
            obrigatorias = ["nome", "telefone", "endereco", "numero", "apto", "venda", "cond", "iptu"]
            for col in obrigatorias:
                if col not in df.columns:
                    df[col] = ""
            st.success(f"{len(df)} imóveis carregados com sucesso!")
            for _, row in df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{row.get('nome', '')}** - {row.get('endereco', '')}, nº {row.get('numero', '')}, apto {row.get('apto', '')}")
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
