import streamlit as st
import plotly.express as px

def render_schedule_management(df):
    # previne erro de tela se não houver dados no filtro
    if df.empty:
        st.warning("Sem dados pra calcular o avanço físico no filtro atual.")
        return

    df_etapas = df.groupby('nome_etapa', as_index=False).agg({
        'peso_fisico_etapa_pct': 'max',
        'avanco_fisico_etapa_pct': 'max'
    })

    df_etapas['avanco_ponderado'] = df_etapas['avanco_fisico_etapa_pct'] * (df_etapas['peso_fisico_etapa_pct'] / 100)
    avanco_global = df_etapas['avanco_ponderado'].sum()

    st.subheader("Status Físico")
    c1, c2, c3 = st.columns(3)
    
    c1.metric("Avanço Global", f"{avanco_global:.1f}%")
    
    etapas_ok = df_etapas[df_etapas['avanco_fisico_etapa_pct'] == 100].shape[0]
    c2.metric("Etapas Concluídas", f"{etapas_ok} de {len(df_etapas)}")
    
    # previne Index Error na busca da pior etapa
    etp_atrasada = df_etapas.sort_values('avanco_fisico_etapa_pct').iloc[0]['nome_etapa'] if len(df_etapas) > 0 else "-"
    c3.metric("Maior Atraso", etp_atrasada)
    
    st.markdown("---")
    
    c4, c5 = st.columns(2)

    with c4:
        st.markdown("**Conclusão por Etapa**")
        df_sorted = df_etapas.sort_values('avanco_fisico_etapa_pct', ascending=True)

        fig_av = px.bar(
            df_sorted, x='avanco_fisico_etapa_pct', y='nome_etapa', orientation='h',
            text='avanco_fisico_etapa_pct', color='avanco_fisico_etapa_pct', color_continuous_scale='Blues' 
        )
        fig_av.update_layout(
            xaxis=dict(range=[0, 100], title="Avanço (%)"), 
            yaxis_title=None, coloraxis_showscale=False
        )
        fig_av.update_traces(texttemplate='%{text}%') 
        st.plotly_chart(fig_av, use_container_width=True)

    with c5:
        st.markdown("**Peso das Etapas**")
        fig_peso = px.pie(df_etapas, values='peso_fisico_etapa_pct', names='nome_etapa', hole=0.4)
        st.plotly_chart(fig_peso, use_container_width=True)
