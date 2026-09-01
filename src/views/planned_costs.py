import streamlit as st
import plotly.express as px
import pandas as pd

def render_planned_costs(df):
    """
    Renderiza a aba de Custos Planejados.
    Recebe o dataframe já filtrado globalmente pela sidebar.
    """
  
    df_previsto = df[df['tipo_lancamento'] == 'Previsto']
    
    if df_previsto.empty:
        st.warning("⚠️ Não há dados previstos para os filtros selecionados.")
        return


    custo_total = df_previsto['valor_total'].sum()
    moeda_formatada = f"R$ {custo_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    st.metric(label="Orçamento Total Previsto", value=moeda_formatada)
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Custos por Etapa da Obra")
        df_etapa = df_previsto.groupby('nome_etapa', as_index=False)['valor_total'].sum()
        df_etapa = df_etapa.sort_values(by='valor_total', ascending=True)
        
        fig_etapa = px.bar(
            df_etapa, 
            x='valor_total', 
            y='nome_etapa', 
            orientation='h',
            text_auto='.2s',
            labels={'valor_total': 'Custo Previsto (R$)', 'nome_etapa': ''},
            color_discrete_sequence=['#2C3E50']
        )
        fig_etapa.update_layout(yaxis_title=None)
        st.plotly_chart(fig_etapa, use_container_width=True)
        
    with col2:
        st.subheader("Distribuição por Grupo de Custo")
        df_grupo = df_previsto.groupby('grupo_custo', as_index=False)['valor_total'].sum()
        
        fig_grupo = px.pie(
            df_grupo, 
            values='valor_total', 
            names='grupo_custo',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        st.plotly_chart(fig_grupo, use_container_width=True)
