
import streamlit as st
import webbrowser
from urllib.parse import quote

# Login simples
def login():
    st.title("Painel ImóveisH - Login")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == "helton1985" and password == "Indira1986@":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha inválidos.")

# Dados mockados
dados = [
    {
        "nome": "João da Silva",
        "telefone": "11999999999",
        "endereco": "Rua das Flores",
        "numero": "123",
        "apto": "12",
        "venda": "450.000",
        "cond": "500",
        "iptu": "120"
    },
    {
        "nome": "Maria Oliveira",
        "telefone": "11888888888",
        "endereco": "Av. Paulista",
        "numero": "1000",
        "apto": "101",
        "venda": "650.000",
        "cond": "700",
        "iptu": "180"
    }
]

# Mensagem padrão
def gerar_link_whatsapp(d):
    msg = f"Olá {d['nome']}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {d['endereco']}, nº {d['numero']}, apto {d['apto']}%0a💰 Valor de venda: R$ {d['venda']}%0a🏢 Condomínio: R$ {d['cond']}%0a📄 IPTU: R$ {d['iptu']}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aAgradeço desde já pela atenção."
    return f"https://wa.me/55{d['telefone']}?text={quote(msg)}"

# App principal
def painel():
    st.title("Painel ImóveisH - Validação de Imóveis")
    for d in dados:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{d['nome']}** - {d['endereco']}, nº {d['numero']}, apto {d['apto']}")
        with col2:
            url = gerar_link_whatsapp(d)
            st.link_button("Enviar WhatsApp", url, use_container_width=True)

# Execução
if "logado" not in st.session_state:
    login()
else:
    painel()
