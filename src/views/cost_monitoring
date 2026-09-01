import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_cost_monitoring(df):
    """
    Renderiza a aba de Monitoramento (Previsto vs Realizado).
    """
    total_previsto = df[df['tipo_lancamento'] == 'Previsto']['valor_total'].sum()
    total_realizado = df[df['tipo_lancamento'] == 'Realizado']['valor_total'].sum()
    
    desvio_absoluto = total_realizado - total_previsto
    
    if total_previsto > 0:
        desvio_percentual = (desvio_absoluto / total_previsto) * 100
    else:
        desvio_percentual = 0.0

    st.markdown("### ⚖️ Resumo Financeiro da Obra")
    col1, col2, col3, col4 = st.columns(4)
    
    fmt_prev = f"R$ {total_previsto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    fmt_real = f"R$ {total_realizado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    fmt_desv = f"R$ {desvio_absoluto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    col1.metric("Orçado (Previsto)", fmt_prev)
    col2.metric("Gasto (Realizado)", fmt_real)
    
    col3.metric("Desvio Financeiro", fmt_desv, delta=fmt_desv, delta_color="inverse")
    col4.metric("Desvio (%)", f"{desvio_percentual:.1f}%", delta=f"{desvio_percentual:.1f}%", delta_color="inverse")
    
    st.divider()

    st.markdown("#### Comparativo de Custos por Etapa")
    
    df_etapas = df.pivot_table(
        index='nome_etapa', 
        columns='tipo_lancamento', 
        values='valor_total', 
        aggfunc='sum'
    ).fillna(0).reset_index()

    if 'Previsto' not in df_etapas: df_etapas['Previsto'] = 0
    if 'Realizado' not in df_etapas: df_etapas['Realizado'] = 0

    fig_comparativo = go.Figure()
    
    fig_comparativo.add_trace(go.Bar(
        x=df_etapas['nome_etapa'], y=df_etapas['Previsto'],
        name='Previsto', marker_color='#2C3E50' # Azul Escuro
    ))
    
    fig_comparativo.add_trace(go.Bar(
        x=df_etapas['nome_etapa'], y=df_etapas['Realizado'],
        name='Realizado', marker_color='#27AE60' # Verde
    ))
    
    fig_comparativo.update_layout(barmode='group', xaxis_title="", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_comparativo, use_container_width=True)
