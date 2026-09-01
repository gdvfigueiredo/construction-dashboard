import streamlit as st
import pandas as pd

from src.data_loader import load_and_clean_data
from src.views.realized_costs import render_realized_costs
from src.views.planned_costs import render_planned_costs
from src.views.cost_monitoring import render_cost_monitoring    
from src.views.schedule_management import render_schedule_management

# 1. Configuração da Página
st.set_page_config(
    page_title="Gestão de Obras | Dashboard",
    page_icon="🏗️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

df = load_and_clean_data("data/raw/dataset_mock_produto_escalavel.csv")

with st.sidebar:
    st.title("Filtros Globais")
    st.markdown("Selecione os parâmetros para atualizar o painel.")
    
    obras = df['nome_obra'].unique().tolist()
    meses = sorted(df['mes_ano'].unique().tolist())
    
    obra_selecionada = st.selectbox("Selecione a Obra:", ["Todas"] + obras)
    mes_selecionado = st.selectbox("Mês de Referência:", ["Todos"] + meses)
    
    st.divider()
    st.caption("Desenvolvido para Gestão Escalável")

df_filtrado = df.copy()

if obra_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['nome_obra'] == obra_selecionada]

if mes_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['mes_ano'] == mes_selecionado]

st.title("📊 Dashboard de Gestão de Obras")
st.markdown("Acompanhamento financeiro e físico de projetos.")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Custos Planejados", 
    "📉 Custos Realizados", 
    "⚖️ Monitoramento", 
    "⏳ Gestão de Prazos"
])

with tab1:
    render_planned_costs(df_filtrado)

with tab2:
    render_realized_costs(df_filtrado)

with tab3:
    render_cost_monitoring(df_filtrado)

with tab4:
    render_schedule_management(df_filtrado)
