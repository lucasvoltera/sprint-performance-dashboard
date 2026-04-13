import plotly.express as px
import plotly.graph_objects as go

def create_velocity_chart(velocity_df, moving_average):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=velocity_df['Sprint'], y=velocity_df['Tarefas'],
        name="Entregas do time", marker_color='#3B82F6', text=velocity_df['Tarefas'], textposition='auto'
    ))
    fig.add_trace(go.Scatter(
        x=velocity_df['Sprint'], y=moving_average,
        name="Média acumulada", mode='lines+markers', line=dict(color='#F59E0B', width=3)
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=30, b=10)
    )
    return fig

def create_donut_chart(df, value_col, name_col, total_val):
    fig = px.pie(
        df, values=value_col, names=name_col, hole=0.6,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=0, r=0))
    fig.add_annotation(text=f"Total<br><b>{int(total_val)}</b>", x=0.5, y=0.5, font_size=20, showarrow=False)
    return fig

def create_evolution_chart(actual_df, name_col, analysis_columns):
    melted_df = actual_df.melt(id_vars=[name_col], value_vars=analysis_columns, var_name='Sprint', value_name='Tarefas')
    fig = px.line(melted_df, x='Sprint', y='Tarefas', color=name_col, markers=True)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', 
        margin=dict(t=10, b=10, l=10, r=10),
        yaxis=dict(title="Quantidade de tarefas"), xaxis=dict(title="")
    )
    return fig

def create_ranking_chart(df, value_col, name_col):
    sorted_df = df.sort_values(by=value_col, ascending=True)
    fig = px.bar(
        sorted_df, x=value_col, y=name_col, orientation='h',
        color=value_col, color_continuous_scale='Blues', text=value_col
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(t=10, b=10), 
        xaxis_title="Tarefas entregues", 
        yaxis_title="", 
        height=400,
        coloraxis_showscale=False  
    )
    return fig

def create_individual_comparison_chart(analysis_columns, member_history, selected_member, team_average_per_sprint):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=analysis_columns, y=member_history,
        mode='lines+markers', name=selected_member,
        line=dict(color='#2563EB', width=4), marker=dict(size=10)
    ))
    fig.add_trace(go.Scatter(
        x=analysis_columns, y=team_average_per_sprint,
        mode='lines', name='Média do time',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig