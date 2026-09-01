import streamlit as st
import plotly.express as px

def formata_brl(v):
    return f"R$ {v:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')

def render_realized_costs(df):
    df_real = df[df['tipo_lancamento'] == 'Realizado']
    
    if df_real.empty:
        st.info("Sem dados de custos realizados neste corte.")
        return

    st.metric("Custo Realizado", formata_brl(df_real['valor_total'].sum()))
    st.markdown("---")
    
    # linha 1 de gráficos
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Custo Mensal**")
        df_mes = df_real.groupby('mes_ano', as_index=False)['valor_total'].sum()
        
        fig_mes = px.bar(
            df_mes, x='mes_ano', y='valor_total', text_auto='.2s',
            labels={'valor_total': 'R$', 'mes_ano': ''}
        )
        fig_mes.update_traces(marker_color='#d62728')
        st.plotly_chart(fig_mes, use_container_width=True)
        
    with c2:
        st.markdown("**Top 5 Fornecedores**")
        df_forn = df_real.groupby('nome_fornecedor', as_index=False)['valor_total'].sum()
        df_forn = df_forn.sort_values('valor_total', ascending=False).head(5)
        
        fig_forn = px.bar(
            df_forn, x='valor_total', y='nome_fornecedor', orientation='h', text_auto='.2s',
            labels={'valor_total': 'R$', 'nome_fornecedor': ''}
        )
        fig_forn.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_forn.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig_forn, use_container_width=True)

    st.write("") # espaçamento
    
    # linha 2 de gráficos
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown("**Mão de Obra vs Material**")
        df_cat = df_real.groupby('categoria_insumo', as_index=False)['valor_total'].sum()
        fig_cat = px.pie(df_cat, values='valor_total', names='categoria_insumo', hole=0.4)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with c4:
        st.markdown("**Status Financeiro**")
        df_status = df_real.groupby('status_pagamento', as_index=False)['valor_total'].sum()
        fig_status = px.pie(df_status, values='valor_total', names='status_pagamento', hole=0.4)
        st.plotly_chart(fig_status, use_container_width=True)
