import streamlit as st
import pandas as pd

# importando as views
from src.data_loader import load_and_clean_data
from src.views.realized_costs import render_realized_costs
from src.views.planned_costs import render_planned_costs
from src.views.cost_monitoring import render_cost_monitoring    
from src.views.schedule_management import render_schedule_management

st.set_page_config(
    page_title="Dashboard Obras",
    layout="wide"
)

# TODO: trocar o caminho do csv quando conectar com o banco de dados
df = load_and_clean_data("data/dataset_mock_produto_escalavel.csv")

with st.sidebar:
    st.header("Filtros")
    
    lista_obras = df['nome_obra'].unique().tolist()
    lista_meses = sorted(df['mes_ano'].unique().tolist())
    
    obra_sel = st.selectbox("Obra:", ["Todas"] + lista_obras)
    mes_sel = st.selectbox("Mês:", ["Todos"] + lista_meses)
    
    st.markdown("---")
    st.caption("v1.0 - Em desenvolvimento")

# aplicando os filtros
df_filtrado = df.copy()

if obra_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['nome_obra'] == obra_sel]

if mes_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['mes_ano'] == mes_sel]


st.title("Dashboard de Obras")
st.markdown("Acompanhamento financeiro e físico")
st.write("")

t_plan, t_real, t_mon, t_prazos = st.tabs([
    "Planejado", 
    "Realizado", 
    "Monitoramento", 
    "Prazos"
])

with t_plan:
    render_planned_costs(df_filtrado)

with t_real:
    render_realized_costs(df_filtrado)

with t_mon:
    render_cost_monitoring(df_filtrado)

with t_prazos:
    render_schedule_management(df_filtrado)
