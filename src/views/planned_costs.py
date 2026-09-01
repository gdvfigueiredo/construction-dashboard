import streamlit as st
import plotly.express as px

# TODO: mover essa função depois pra um arquivo utils.py compartilhado
def formata_brl(v):
    return f"R$ {v:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')

def render_planned_costs(df):
    df_prev = df[df['tipo_lancamento'] == 'Previsto']
    
    if df_prev.empty:
        st.warning("Nenhum custo previsto encontrado para os filtros atuais.")
        return

    custo_total = df_prev['valor_total'].sum()
    
    st.metric("Orçamento Previsto", formata_brl(custo_total))
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Custos por Etapa**")
        # agrupando e já ordenando direto na mesma linha
        df_etapa = df_prev.groupby('nome_etapa', as_index=False)['valor_total'].sum().sort_values('valor_total')
        
        fig_etapa = px.bar(
            df_etapa, x='valor_total', y='nome_etapa', orientation='h',
            text_auto='.2s', labels={'valor_total': 'Custo (R$)', 'nome_etapa': ''}
        )
        fig_etapa.update_layout(yaxis_title=None, showlegend=False)
        fig_etapa.update_traces(marker_color='#1f77b4')
        st.plotly_chart(fig_etapa, use_container_width=True)
        
    with c2:
        st.markdown("**Distribuição por Grupo**")
        df_grupo = df_prev.groupby('grupo_custo', as_index=False)['valor_total'].sum()
        
        fig_grupo = px.pie(df_grupo, values='valor_total', names='grupo_custo', hole=0.4)
        st.plotly_chart(fig_grupo, use_container_width=True)
