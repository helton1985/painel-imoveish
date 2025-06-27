
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Painel ImóveisH - Validação de Imóveis via Excel")

st.title("Painel ImóveisH - Validação de Imóveis via Excel")
st.markdown("📥 Faça upload de uma planilha `.xlsx` com os seguintes campos obrigatórios:")
st.code("nome, telefone, endereco, numero, apto, venda, cond, iptu", language="markdown")

uploaded_file = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"{len(df)} imóveis carregados com sucesso!")

    # Normalizar os nomes das colunas para evitar erro com 'telefone'
    df.columns = [col.lower().strip().replace(" ", "_").replace("/", "_") for col in df.columns]

    telefone_col = None
    for col in df.columns:
        if "telefone" in col or "celular" in col:
            telefone_col = col
            break

    if not telefone_col:
        st.error("Erro: Nenhuma coluna de telefone encontrada na planilha.")
    else:
        for index, row in df.iterrows():
            try:
                nome = str(row.get("nome", ""))
                endereco = str(row.get("endereco", ""))
                numero = str(row.get("numero", ""))
                apto = str(row.get("apto", ""))
                venda = str(row.get("venda", ""))
                cond = str(row.get("cond", ""))
                iptu = str(row.get("iptu", ""))
                telefone = str(row.get(telefone_col, ""))

                # Validar telefone com 11 dígitos após o 55
                if telefone.startswith("55") and len(telefone) == 13:
                    mensagem = f"""Olá {nome}, tudo bem?

Sou o corretor Helton da ImoveisH (www.imoveish.com.br).

Verificamos que você possui um imóvel cadastrado com as seguintes informações:
📍 Endereço: {endereco}, nº {numero}, apto {apto}
💰 Valor de venda: R$ {venda}
🏢 Condomínio: R$ {cond}
📄 IPTU: R$ {iptu}

Gostaria de confirmar se este imóvel ainda está disponível para venda e se os valores acima estão atualizados.

Agradeço desde já pela atenção."""
                    mensagem_encoded = urllib.parse.quote(mensagem)
                    link_whatsapp = f"https://api.whatsapp.com/send?phone={telefone}&text={mensagem_encoded}"
                    st.markdown(f"✅ **{endereco}, nº {numero}, apto {apto}** - [📩 Enviar WhatsApp]({link_whatsapp})", unsafe_allow_html=True)
                else:
                    st.markdown(f"❌ **{endereco}, nº {numero}, apto {apto}** - Telefone inválido")
            except Exception as e:
                st.markdown(f"❌ Erro na linha {index + 2}: {e}")
