import streamlit as st
import plotly.express as px
import pandas as pd

def render_schedule_management(df):
    """
    Renderiza a aba de Gestão de Prazos e Avanço Físico.
    """

    df_etapas = df.groupby('nome_etapa', as_index=False).agg({
        'peso_fisico_etapa_pct': 'max',
        'avanco_fisico_etapa_pct': 'max'
    })

    df_etapas['avanco_ponderado'] = df_etapas['avanco_fisico_etapa_pct'] * (df_etapas['peso_fisico_etapa_pct'] / 100)
    avanco_global = df_etapas['avanco_ponderado'].sum()

    st.markdown("### ⏳ Status Físico do Projeto")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Avanço Físico Global", f"{avanco_global:.1f}%")
    
    etapas_concluidas = df_etapas[df_etapas['avanco_fisico_etapa_pct'] == 100].shape[0]
    total_etapas = df_etapas.shape[0]
    col2.metric("Etapas Concluídas", f"{etapas_concluidas} de {total_etapas}")
    
    etapa_atrasada = df_etapas.sort_values(by='avanco_fisico_etapa_pct').iloc[0]['nome_etapa']
    col3.metric("Atenção (Menor Avanço)", etapa_atrasada)
    
    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("#### Conclusão por Etapa")
        df_etapas_sorted = df_etapas.sort_values(by='avanco_fisico_etapa_pct', ascending=True)

        fig_avanco = px.bar(
            df_etapas_sorted,
            x='avanco_fisico_etapa_pct',
            y='nome_etapa',
            orientation='h',
            text='avanco_fisico_etapa_pct',
            labels={'avanco_fisico_etapa_pct': 'Avanço (%)', 'nome_etapa': ''},
            color='avanco_fisico_etapa_pct',
            color_continuous_scale='Teal' 
        )
        
        fig_avanco.update_layout(xaxis=dict(range=[0, 100]), coloraxis_showscale=False)
        fig_avanco.update_traces(texttemplate='%{text}%') 
        st.plotly_chart(fig_avanco, use_container_width=True)

    with col5:
        st.markdown("#### Peso das Etapas no Projeto")
        
        fig_peso = px.pie(
            df_etapas,
            values='peso_fisico_etapa_pct',
            names='nome_etapa',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_peso, use_container_width=True)
