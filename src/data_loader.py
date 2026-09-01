import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data(filepath="data/raw/dataset_mock_produto_escalavel.csv"):
    
    df = pd.read_csv(filepath, sep=';')

    df['data_referencia'] = pd.to_datetime(df['data_referencia'])
    
    df['mes_ano'] = df['data_referencia'].dt.to_period('M').astype(str)

    cols_to_fill = ['nome_fornecedor', 'forma_pagamento', 'status_pagamento']
    df[cols_to_fill] = df[cols_to_fill].fillna('Não Aplicável')
    
    numeric_cols = ['quantidade', 'valor_unitario', 'valor_total']
    df[numeric_cols] = df[numeric_cols].fillna(0.0)
    
    return df

if __name__ == "__main__":
    df_teste = load_and_clean_data("../data/raw/dataset_mock_produto_escalavel.csv")
    print("Base carregada com sucesso!")
    print(f"Total de linhas: {df_teste.shape[0]}")
    print(df_teste.info())
