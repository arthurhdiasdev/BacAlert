import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="BacAlert - Monitoramento de Surtos Bacterianos",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
    <style>
    /* Estilos gerais */
    .main {
        padding: 2rem;
        background-color: #f5f7fa;
    }
    
    /* Cabeçalho */
    .header {
        background: linear-gradient(135deg, #2c5282 0%, #1f77b4 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .header h1 {
        font-size: 2.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header p {
        font-size: 1.3rem;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Cards e métricas */
    .metric-card {
        background: #f8fafc;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin: 0.8rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        background: #ffffff;
    }
    
    /* Alertas */
    .stAlert {
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1.2rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: none;
    }
    
    /* Gráficos */
    .stPlotlyChart {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f5f7fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f5f7fa;
        padding: 1rem;
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #2c5282 0%, #1f77b4 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1f77b4 0%, #2c5282 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Títulos das seções */
    h2, h3 {
        color: #2c5282;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Mensagens de informação */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1.2rem 0;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        color: #1a365d;
    }
    
    /* Upload de arquivo */
    .stFileUploader {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Selectbox e Date Input */
    .stSelectbox, .stDateInput {
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Métricas */
    .stMetric {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #2c5282;
    }
    
    .stMetric [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #4a5568;
    }

    /* Textos e labels */
    .stMarkdown {
        color: #2d3748;
    }

    /* Elementos de seleção */
    .stSelectbox > div {
        background-color: #f8fafc;
    }

    /* Títulos dos gráficos */
    .js-plotly-plot .plotly .main-svg {
        background-color: #f8fafc !important;
    }

    /* Tooltips e legendas */
    .plotly .hovertext {
        background-color: #2c5282 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho personalizado
st.markdown("""
    <div class="header">
        <h1>🦠 BacAlert - Monitoramento de Surtos Bacterianos</h1>
        <p>Sistema de monitoramento e alerta para surtos bacterianos em ambiente hospitalar.
        Faça upload dos dados para visualizar dashboards interativos e gerar alertas em tempo real.</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para filtros e configurações
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='color: #2c5282; font-size: 1.5rem;'>⚙️ Configurações</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Upload do arquivo
    arquivo = st.file_uploader("📂 Upload da tabela Excel", type=["xlsx", "xls"])
    
    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            st.success("✅ Arquivo carregado com sucesso!")
            
            # Filtros
            st.markdown("### 🔍 Filtros")
            
            # Filtro por data
            if 'Data_Coleta' in df.columns:
                df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'], errors='coerce')
                data_inicio = st.date_input(
                    "📅 Data inicial",
                    value=df['Data_Coleta'].min().date()
                )
                data_fim = st.date_input(
                    "📅 Data final",
                    value=df['Data_Coleta'].max().date()
                )
                df = df[(df['Data_Coleta'].dt.date >= data_inicio) & 
                       (df['Data_Coleta'].dt.date <= data_fim)]
            
            # Filtro por bactéria
            if 'Bactéria' in df.columns:
                bacterias = ['Todas'] + sorted(df['Bactéria'].unique().tolist())
                bacteria_selecionada = st.selectbox("🦠 Bactéria", bacterias)
                if bacteria_selecionada != 'Todas':
                    df = df[df['Bactéria'] == bacteria_selecionada]
            
            # Filtro por unidade
            if 'Unidade' in df.columns:
                unidades = ['Todas'] + sorted(df['Unidade'].unique().tolist())
                unidade_selecionada = st.selectbox("🏥 Unidade Hospitalar", unidades)
                if unidade_selecionada != 'Todas':
                    df = df[df['Unidade'] == unidade_selecionada]
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {str(e)}")
            df = None

# Conteúdo principal
if arquivo and df is not None:
    # Métricas principais
    st.markdown("### 📊 Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total de Casos", len(df))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'Bactéria' in df.columns:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Bactérias Únicas", df['Bactéria'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if 'Unidade' in df.columns:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Unidades Afetadas", df['Unidade'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        if 'Tempo_Internacao' in df.columns:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Média de Internação", f"{df['Tempo_Internacao'].mean():.1f} dias")
            st.markdown('</div>', unsafe_allow_html=True)

    # Alertas
    st.markdown("### 🚨 Sistema de Alertas")
    alertas = []
    
    if 'Data_Coleta' in df.columns:
        casos_ultimos_7_dias = df[df['Data_Coleta'] >= (datetime.now() - timedelta(days=7))].shape[0]
        if casos_ultimos_7_dias > 10:
            alertas.append(f"⚠️ Alerta: {casos_ultimos_7_dias} casos nos últimos 7 dias!")
    
    if 'Bactéria' in df.columns:
        for bacteria in df['Bactéria'].unique():
            casos_bacteria = df[df['Bactéria'] == bacteria].shape[0]
            if casos_bacteria > 5:
                alertas.append(f"⚠️ Alerta: {casos_bacteria} casos de {bacteria}!")
    
    if alertas:
        for alerta in alertas:
            st.warning(alerta)
    else:
        st.success("✅ Nenhum alerta ativo no momento.")

    # Visualizações
    st.markdown("### 📈 Visualizações")
    
    # Gráfico de evolução temporal
    if 'Data_Coleta' in df.columns:
        st.markdown('<div class="stPlotlyChart">', unsafe_allow_html=True)
        st.subheader("📅 Evolução dos Casos")
        casos_diarios = df.groupby('Data_Coleta').size().reset_index(name='Casos')
        fig = px.line(casos_diarios, x='Data_Coleta', y='Casos',
                     title='Evolução dos Casos ao Longo do Tempo')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Distribuição por bactéria e unidade
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Bactéria' in df.columns:
            st.markdown('<div class="stPlotlyChart">', unsafe_allow_html=True)
            st.subheader("🦠 Distribuição por Bactéria")
            fig = px.pie(df, names='Bactéria', title='Proporção de Casos por Bactéria')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'Unidade' in df.columns:
            st.markdown('<div class="stPlotlyChart">', unsafe_allow_html=True)
            st.subheader("🏥 Casos por Unidade")
            casos_unidade = df['Unidade'].value_counts().reset_index()
            casos_unidade.columns = ['Unidade', 'Casos']
            fig = px.bar(casos_unidade, x='Unidade', y='Casos',
                        title='Número de Casos por Unidade Hospitalar')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Mapa de calor de correlação
    if 'Tempo_Internacao' in df.columns:
        st.markdown('<div class="stPlotlyChart">', unsafe_allow_html=True)
        st.subheader("📊 Análise de Correlação")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr,
                           title='Correlação entre Variáveis Numéricas',
                           color_continuous_scale='RdBu')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Exportação de relatório
    st.markdown("### 📤 Exportação de Dados")
    if st.button("📥 Exportar Relatório"):
        try:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Dados', index=False)
                
                # Adicionar resumo estatístico
                if 'Tempo_Internacao' in df.columns:
                    df.describe().to_excel(writer, sheet_name='Estatísticas')
                
                # Adicionar contagem por bactéria
                if 'Bactéria' in df.columns:
                    df['Bactéria'].value_counts().to_excel(writer, sheet_name='Contagem_Bactérias')
            
            buffer.seek(0)
            st.download_button(
                label="📥 Baixar Relatório Excel",
                data=buffer,
                file_name=f"relatorio_surtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.ms-excel"
            )
        except Exception as e:
            st.error(f"Erro ao gerar relatório: {str(e)}")

else:
    st.info("👆 Por favor, faça upload de um arquivo Excel para começar.")
