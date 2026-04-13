import streamlit as st
from streamlit_autorefresh import st_autorefresh

from config import settings
from data.gsheets_client import fetch_data
from utils.data_processing import process_dataframe
from views.team_view import render_team_tab
from views.individual_view import render_individual_tab

def setup_page():
    """Configurações iniciais da página, remoção de logos e CSS de impressão."""
    st.set_page_config(page_title="Sprint Analytics - Live", layout="wide")
    st_autorefresh(interval=settings.REFRESH_INTERVAL, key="datarefresh")
    
    st.markdown("""
        <style>
        header[data-testid="stHeader"] {
            display: none !important; /* Esconde o logo, menu e botão de deploy */
        }
        footer {
            display: none !important; /* Esconde o 'Made with Streamlit' no rodapé */
        }
        div[data-testid="stToolbar"] {
            display: none !important; /* Esconde botões flutuantes extras */
        }
        
        /* Ajusta o espaço vazio que fica no topo quando tiramos o cabeçalho */
        .block-container {
            padding-top: 2rem !important; 
        }

        @media print {
            html, body, .stApp { height: auto !important; overflow: visible !important; background-color: white !important; }
            .block-container, div[data-testid="stMainBlockContainer"] { overflow: visible !important; height: auto !important; max-width: 100% !important; padding-top: 0 !important; }
            [data-testid="stSidebar"], button, .stSlider, .stSelectbox, .stRadio { display: none !important; } /* Esconde os filtros na hora da foto */
            .js-plotly-plot { page-break-inside: avoid !important; }
        }
        </style>
    """, unsafe_allow_html=True)

def load_dashboard_data():
    """Tenta baixar e processar os dados, parando a tela em caso de erro."""
    try:
        raw_df = fetch_data(settings.SHEET_URL, settings.CACHE_TTL)
        return process_dataframe(raw_df)
    except Exception as e:
        st.error(f"Erro ao conectar ou processar dados da planilha: {e}")
        st.stop()

def render_header(all_columns):
    """Renderiza o título e o seletor principal de Sprint."""
    title_col, sprint_col = st.columns([3, 1])
    
    with sprint_col:
        selectable_sprints = all_columns[1:] if len(all_columns) > 1 else all_columns
        selected_sprint = st.selectbox(
            "Ciclo de análise ativo:", 
            options=selectable_sprints, 
            index=len(selectable_sprints)-1
        )
        
    with title_col:
        st.title(f"Ally Project - {selected_sprint}")
        
    st.divider()
    return selected_sprint

def get_analysis_window(all_columns, selected_sprint):
    """Lida com a lógica da janela de tempo (slider) baseada na sprint escolhida."""
    sprint_idx = all_columns.index(selected_sprint)
    columns_up_to_selected = all_columns[:sprint_idx + 1]

    if len(columns_up_to_selected) > 3:
        num_sprints = st.slider(
            "Janela de histórico:", 
            min_value=3, 
            max_value=len(columns_up_to_selected), 
            value=len(columns_up_to_selected) 
        )
        return columns_up_to_selected[-num_sprints:]
    
    return columns_up_to_selected

def main():
    setup_page()
    
    # 1. Carrega os Dados
    actual_df, name_col, all_columns = load_dashboard_data()
    
    # 2. Renderiza Controles de Topo
    selected_sprint = render_header(all_columns)
    analysis_columns = get_analysis_window(all_columns, selected_sprint)
    
    # 3. Métricas Globais Iniciais
    team_average_per_sprint = actual_df[analysis_columns].mean(numeric_only=True)

    # 4. Roteamento de abas
    selected_tab = st.radio(
        "Navegação do Dashboard:",
        options=["Visão do time", "Visão individual"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if selected_tab == "Visão do time":
        render_team_tab(actual_df, analysis_columns, name_col)
    else:
        render_individual_tab(actual_df, analysis_columns, name_col, team_average_per_sprint)

if __name__ == "__main__":
    main()
