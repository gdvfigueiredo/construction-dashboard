import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def formata_brl(valor):
    return f"R$ {valor:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')

def render_cost_monitoring(df):
    # totalizadores
    total_prev = df[df['tipo_lancamento'] == 'Previsto']['valor_total'].sum()
    total_real = df[df['tipo_lancamento'] == 'Realizado']['valor_total'].sum()
    
    desvio_abs = total_real - total_prev
    
    # previne erro de divisão por zero se o filtro vier vazio
    desvio_pct = (desvio_abs / total_prev * 100) if total_prev > 0 else 0.0

    st.subheader("Resumo Financeiro")
    
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("Orçado", formata_brl(total_prev))
    c2.metric("Gasto", formata_brl(total_real))
    
    c3.metric("Desvio Financeiro", formata_brl(desvio_abs), delta=formata_brl(desvio_abs), delta_color="inverse")
    c4.metric("Desvio (%)", f"{desvio_pct:.1f}%", delta=f"{desvio_pct:.1f}%", delta_color="inverse")
    
    st.markdown("---")
    st.markdown("**Comparativo por Etapa**")
    
    # pivota a base pra agrupar no gráfico
    df_etapas = df.pivot_table(
        index='nome_etapa', 
        columns='tipo_lancamento', 
        values='valor_total', 
        aggfunc='sum'
    ).fillna(0).reset_index()

    # garante que as colunas existem
    if 'Previsto' not in df_etapas: df_etapas['Previsto'] = 0
    if 'Realizado' not in df_etapas: df_etapas['Realizado'] = 0

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_etapas['nome_etapa'], 
        y=df_etapas['Previsto'],
        name='Previsto', 
        marker_color='#1f77b4' 
    ))
    
    fig.add_trace(go.Bar(
        x=df_etapas['nome_etapa'], 
        y=df_etapas['Realizado'],
        name='Realizado', 
        marker_color='#d62728' 
    ))
    
    fig.update_layout(
        barmode='group', 
        xaxis_title=None, 
        yaxis_title="R$"
    )
    
    st.plotly_chart(fig, use_container_width=True)
