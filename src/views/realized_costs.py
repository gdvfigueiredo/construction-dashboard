import streamlit as st
import plotly.express as px
import pandas as pd

def render_realized_costs(df):
    """
    Renderiza a aba de Custos Realizados.
    Filtra os dados para mostrar apenas o que já foi executado.
    """

    df_realizado = df[df['tipo_lancamento'] == 'Realizado']
    
    if df_realizado.empty:
        st.warning("⚠️ Não há dados de custos realizados para os filtros selecionados.")
        return

    custo_total = df_realizado['valor_total'].sum()
    moeda_formatada = f"R$ {custo_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    st.metric(label="Custo Total Realizado", value=moeda_formatada)
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Custo Mensal")
        df_mes = df_realizado.groupby('mes_ano', as_index=False)['valor_total'].sum()
        
        fig_mes = px.bar(
            df_mes, 
            x='mes_ano', 
            y='valor_total', 
            text_auto='.2s',
            labels={'valor_total': 'Custo (R$)', 'mes_ano': 'Mês de Referência'},
            color_discrete_sequence=['#27AE60'] # Verde escuro para indicar "Realizado"
        )
        fig_mes.update_layout(yaxis_title=None)
        st.plotly_chart(fig_mes, use_container_width=True)
        
    with col2:
        st.markdown("#### Top 5 Fornecedores")
        df_fornecedor = df_realizado.groupby('nome_fornecedor', as_index=False)['valor_total'].sum()
        df_fornecedor = df_fornecedor.sort_values(by='valor_total', ascending=False).head(5)
        
        fig_fornecedor = px.bar(
            df_fornecedor, 
            x='valor_total', 
            y='nome_fornecedor', 
            orientation='h',
            text_auto='.2s',
            labels={'valor_total': 'Custo (R$)', 'nome_fornecedor': ''},
            color_discrete_sequence=['#E67E22'] # Laranja
        )
        fig_fornecedor.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_fornecedor, use_container_width=True)

    st.write("")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Mão de Obra vs Material")
        df_categoria = df_realizado.groupby('categoria_insumo', as_index=False)['valor_total'].sum()
        
        fig_categoria = px.pie(
            df_categoria, 
            values='valor_total', 
            names='categoria_insumo',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_categoria, use_container_width=True)
        
    with col4:
        st.markdown("#### Status Financeiro")
        df_status = df_realizado.groupby('status_pagamento', as_index=False)['valor_total'].sum()
        
        fig_status = px.pie(
            df_status, 
            values='valor_total', 
            names='status_pagamento',
            hole=0.4,
            color_discrete_sequence=['#2ECC71', '#E74C3C']
        )
        st.plotly_chart(fig_status, use_container_width=True)
