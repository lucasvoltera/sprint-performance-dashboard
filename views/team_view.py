import streamlit as st
from utils import charts
from services.metrics_service import calculate_team_metrics

def render_team_tab(actual_df, analysis_columns, name_col):
    metrics = calculate_team_metrics(actual_df, analysis_columns)
    current_sprint = analysis_columns[-1]

    _render_current_cycle_kpis(metrics)
    _render_current_cycle_charts(actual_df, current_sprint, name_col, metrics)
    _render_global_history_charts(actual_df, analysis_columns, name_col, metrics)
    _render_global_ranking(actual_df, name_col)
    _render_member_evolution(actual_df, analysis_columns, name_col)

def _render_current_cycle_kpis(metrics):
    st.markdown("### Desempenho do ciclo atual")
    st.caption("Métricas e resultados focados no ciclo atual.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Tarefas entregues no ciclo", int(metrics["current_total"]), f"{int(metrics['velocity_delta'])} vs ciclo anterior")
    col2.metric("Média de entregas / Membro", f"{metrics['average_per_member']:.1f}")
    col3.metric("Quantidade de pessoas", metrics["people_count"])
    st.write("") 

def _render_current_cycle_charts(actual_df, current_sprint, name_col, metrics):
    col_current_rank, col_current_donut = st.columns([2, 1])
    with col_current_rank:
        st.markdown("##### Ranqueamento de entregas do ciclo atual")
        fig_current_rank = charts.create_ranking_chart(actual_df, current_sprint, name_col)
        st.plotly_chart(fig_current_rank, use_container_width=True)
        
    with col_current_donut:
        st.markdown("##### Carga de trabalho do ciclo atual")
        fig_current_donut = charts.create_donut_chart(actual_df, current_sprint, name_col, metrics["current_total"])
        st.plotly_chart(fig_current_donut, use_container_width=True)

def _render_global_history_charts(actual_df, analysis_columns, name_col, metrics):
    st.write("\n\n") 
    st.markdown("### Histórico e visão geral")
    st.caption("Análise acumulada e evolução de todas as sprints selecionadas no filtro.")
    st.divider()

    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.markdown("##### Histórico global")
        velocity_df = actual_df[analysis_columns].sum().reset_index()
        velocity_df.columns = ['Sprint', 'Tarefas']
        moving_average = velocity_df['Tarefas'].expanding().mean()
        
        fig_velocity = charts.create_velocity_chart(velocity_df, moving_average)
        st.plotly_chart(fig_velocity, use_container_width=True)

    with col_chart2:
        st.markdown("##### Carga de trabalho global")
        actual_df['Global_Total'] = actual_df[analysis_columns].sum(axis=1)
        fig_global_donut = charts.create_donut_chart(actual_df, 'Global_Total', name_col, metrics["global_sprints_total"])
        st.plotly_chart(fig_global_donut, use_container_width=True)

def _render_global_ranking(actual_df, name_col):
    st.divider()
    st.markdown("##### Ranqueamento geral de entregas")
    st.caption("Soma de todas as tarefas de cada membro no período.")
    fig_global_rank = charts.create_ranking_chart(actual_df, 'Global_Total', name_col)
    st.plotly_chart(fig_global_rank, use_container_width=True)

def _render_member_evolution(actual_df, analysis_columns, name_col):
    st.divider()
    st.markdown("##### Histórico de evolução por pessoa")
    st.caption("Acompanhamento do volume de entregas de cada membro no tempo.")
    
    fig_multi_evolution = charts.create_evolution_chart(actual_df, name_col, analysis_columns)
    st.plotly_chart(fig_multi_evolution, use_container_width=True)
