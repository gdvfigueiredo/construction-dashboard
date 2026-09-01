import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_and_clean_data(filepath="data/raw/base_obras_v1.csv"):
    try:
        df = pd.read_csv(filepath, sep=';', encoding='utf-8')
    except FileNotFoundError:
        # joga o erro na tela sem quebrar a aplicação inteira
        st.error(f"Arquivo não encontrado: {filepath}. Dá uma checada no caminho.")
        return pd.DataFrame() 

    # arrumando as datas
    df['data_referencia'] = pd.to_datetime(df['data_referencia'], errors='coerce')
    df['mes_ano'] = df['data_referencia'].dt.to_period('M').astype(str)

    # tratando os vazios
    cols_text = ['nome_fornecedor', 'forma_pagamento', 'status_pagamento']
    df[cols_text] = df[cols_text].fillna('N/A')
    
    cols_num = ['quantidade', 'valor_unitario', 'valor_total']
    df[cols_num] = df[cols_num].fillna(0)
    
    return df

if __name__ == "__main__":
    # teste rápido rodando direto no terminal
    caminho_teste = "../data/raw/base_obras_v1.csv"
    
    if os.path.exists(caminho_teste):
        df_teste = load_and_clean_data(caminho_teste)
        print(f"-> linhas carregadas: {len(df_teste)}")
        print(df_teste[['mes_ano', 'valor_total']].head())
    else:
        print("Caminho do arquivo de teste não encontrado. Rodando da pasta raiz?")
