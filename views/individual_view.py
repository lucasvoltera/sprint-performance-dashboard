import streamlit as st
import pandas as pd
from utils import charts
from services.metrics_service import calculate_individual_metrics

def render_individual_tab(actual_df, analysis_columns, name_col, team_average_per_sprint):
    st.markdown("### Análise de performance individual")
    st.markdown("Selecione um membro da equipe para visualizar métricas referentes ao período selecionado.")
    
    selected_member = st.selectbox("Selecione o colaborador:", options=actual_df[name_col].unique())
    
    if selected_member:
        st.divider()
        metrics = calculate_individual_metrics(actual_df, analysis_columns, name_col, selected_member)
        overall_team_average = team_average_per_sprint.mean()
        current_sprint = analysis_columns[-1]
        
        _render_individual_kpis(metrics, current_sprint, overall_team_average)
        _render_comparison_chart(analysis_columns, metrics, selected_member, team_average_per_sprint)
        _render_statistical_summary(metrics)


def _render_individual_kpis(metrics, current_sprint, overall_team_average):
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric(f"Entregas ({current_sprint})", int(metrics["current_delivery"]), f"{int(metrics['individual_delta'])} vs anterior")
    c2.metric("Média histórica", f"{int(round(metrics['individual_average']))}", "tarefas / sprint", delta_color="off")
    
    average_status = "Acima da média" if metrics['individual_average'] > overall_team_average else "Abaixo da média"
    status_color = "normal" if metrics['individual_average'] > overall_team_average else "inverse"
    c3.metric("Comparativo com time", average_status, delta=f"Média: {int(round(overall_team_average))}", delta_color=status_color)
    
    c4.metric("Desvio padrão", f"{int(round(metrics['individual_std_dev']))}", "Risco de oscilação", delta_color="off")

def _render_comparison_chart(analysis_columns, metrics, selected_member, team_average_per_sprint):
    st.divider()
    st.markdown("##### Curva de Performance: Indivíduo vs Média do Time")
    fig_comparison = charts.create_individual_comparison_chart(
        analysis_columns, metrics["member_history"], selected_member, team_average_per_sprint
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

def _render_statistical_summary(metrics):
    st.divider()
    st.markdown("##### Resumo estatístico do período")
    stats_df = pd.DataFrame({
        "Métrica": [
            "Quantidade de tarefas entregues", "Média", "Desvio padrão",
            "Melhor sprint", "Mediana", "Pior sprint", "Participação no total do time"
        ],
        "Valor": [
            f"{int(metrics['total_deliveries'])} tarefas",
            f"{int(round(metrics['individual_average']))} tarefas",
            f"{int(round(metrics['individual_std_dev']))} tarefas",
            f"{int(metrics['best_sprint'])} tarefas", 
            f"{int(round(metrics['individual_median']))} tarefas",
            f"{int(metrics['worst_sprint'])} tarefas", 
            f"{int(round(metrics['participation_percentage']))}%"
        ]
    })
    st.dataframe(stats_df, hide_index=True, width='stretch')