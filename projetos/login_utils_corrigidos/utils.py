
import pandas as pd

def carregar_dados(uploaded_file):
    return pd.read_excel(uploaded_file)
