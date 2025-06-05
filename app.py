import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="BacAlert - Monitoramento de Surtos Bacterianos",
    page_icon="assets/bacterias.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cabeçalho
st.title(" BacAlert - Monitoramento de Surtos Bacterianos")
st.markdown("Sistema de monitoramento e alerta para surtos bacterianos em ambientes hospitalars.")

# Sidebar para filtros e configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Upload do arquivo
    arquivo = st.file_uploader("📂 Upload da tabela Excel", type=["xlsx", "xls"])
    
    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            st.success("✅ Arquivo carregado com sucesso!")
            
            # Filtros
            st.subheader("Filtros")
            
            # Filtro por data
            if 'Data_Coleta' in df.columns:
                df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'], errors='coerce')
                data_inicio = st.date_input(
                    " Data inicial",
                    value=df['Data_Coleta'].min().date()
                )
                data_fim = st.date_input(
                    " Data final",
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
    st.header("Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Casos", len(df))
    
    with col2:
        if 'Bactéria' in df.columns:
            st.metric("Bactérias Únicas", df['Bactéria'].nunique())
    
    with col3:
        if 'Unidade' in df.columns:
            st.metric("Unidades Afetadas", df['Unidade'].nunique())
    
    with col4:
        if 'Tempo_Internacao' in df.columns:
            st.metric("Média de Internação", f"{df['Tempo_Internacao'].mean():.1f} dias")

    # Alertas
    st.header("🚨 Sistema de Alertas Bcaterianos")
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
    st.header("📈 Visualizações")
    
    # Gráfico de evolução temporal
    if 'Data_Coleta' in df.columns:
        st.subheader("📅 Evolução dos Casos")
        casos_diarios = df.groupby('Data_Coleta').size().reset_index(name='Casos')
        fig = px.line(casos_diarios, x='Data_Coleta', y='Casos',
                     title='Evolução dos Casos ao Longo do Tempo')
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribuição por bactéria e unidade
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Bactéria' in df.columns:
            st.subheader("🦠 Distribuição por Bactéria")
            fig = px.pie(df, names='Bactéria', title='Proporção de Casos por Bactéria')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Unidade' in df.columns:
            st.subheader("Casos por Unidade")
            casos_unidade = df['Unidade'].value_counts().reset_index()
            casos_unidade.columns = ['Unidade', 'Casos']
            fig = px.bar(casos_unidade, x='Unidade', y='Casos',
                        title='Número de Casos por Unidade Hospitalar')
            st.plotly_chart(fig, use_container_width=True)
    
    # Mapa de calor de correlação
    if 'Tempo_Internacaot' in df.columns:
        st.subheader("📊 Análise de Correlação")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr,
                           title='Correlação entre Variáveis Numéricas',
                           color_continuous_scale='RdBu')
            st.plotly_chart(fig, use_container_width=True)
    
    # Exportação de relatório
    st.header("📤 Exportação de Dados")
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
