
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Painel ImóveisH - Validação de Imóveis via Excel")

st.title("Painel ImóveisH - Validação de Imóveis via Excel")

st.markdown("📥 Faça upload de uma planilha `.xlsx` com os seguintes campos obrigatórios:")
st.code("nome, telefone, endereco, numero, apto, venda, cond, iptu")

uploaded_file = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type="xlsx")

def normalizar_colunas(df):
    colunas_renomeadas = {
        "valor_venda": "venda",
        "valor de venda": "venda",
        "valor_condomínio": "cond",
        "valor_condominio": "cond",
        "valor iptu": "iptu",
        "valor_iptu": "iptu",
        "endereço": "endereco",
        "número": "numero",
        "celular/telefone": "telefone",
        "celular": "telefone",
        "telefone/celular": "telefone",
    }
    df.columns = [col.lower().strip() for col in df.columns]
    df = df.rename(columns=colunas_renomeadas)
    return df

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df = normalizar_colunas(df)
        obrigatorias = ["nome", "telefone", "endereco", "numero", "apto", "venda", "cond", "iptu"]
        if not all(col in df.columns for col in obrigatorias):
            st.error("Erro ao processar o arquivo. Verifique se todos os campos estão corretos.")
        else:
            st.success(f"{len(df)} imóveis carregados com sucesso!")
            for idx, row in df.iterrows():
                try:
                    nome = row["nome"]
                    telefone = str(row["telefone"])
                    endereco = row["endereco"]
                    numero = row["numero"]
                    apto = row["apto"]
                    venda = row["venda"]
                    cond = row["cond"]
                    iptu = row["iptu"]
                    if len(telefone) >= 10:
                        msg = f"Olá {nome}, tudo bem?%0a%0aSou o corretor Helton da ImoveisH (www.imoveish.com.br).%0a%0aVerificamos que você possui um imóvel cadastrado com as seguintes informações:%0a📍 Endereço: {endereco}, nº {numero}, apto {apto}%0a💰 Valor de venda: R$ {venda}%0a🏢 Condomínio: R$ {cond}%0a📄 IPTU: R$ {iptu}%0a%0aGostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.%0a%0aAgradeço desde já pela atenção."
                        url = f"https://api.whatsapp.com/send?phone=55{telefone}&text={msg}"
                        st.markdown(f"✅ {endereco}, nº {numero}, apto {apto} — [📤 Enviar mensagem]({url})", unsafe_allow_html=True)
                    else:
                        st.markdown(f"❌ {endereco}, nº {numero}, apto {apto} — Telefone inválido")
                except Exception as e:
                    st.markdown("❌ Erro ao ler dados do imóvel.")
    except Exception as e:
        st.error("Erro ao processar o arquivo. Verifique se todos os campos estão corretos.")
