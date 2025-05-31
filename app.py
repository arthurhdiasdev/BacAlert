import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Surtos de Bactérias", layout="centered")

st.title("Dashboard de Surtos de Bactérias no Hospital")

arquivo = st.file_uploader("Faça upload da tabela Excel", type=["xlsx", "xls"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.success("Arquivo carregado com sucesso!")
    st.write("### Dados carregados")
    st.dataframe(df, use_container_width=True)

    st.subheader("Resumo estatístico")
    st.dataframe(df.describe(include='all').T, use_container_width=True)

    # Dashboard 1: Histograma do Tempo de Internação
    st.subheader("Histograma do Tempo de Internação")
    if 'Tempo_Internacao' in df.columns:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig1, ax1 = plt.subplots(figsize=(7, 3))
            ax1.hist(df['Tempo_Internacao'].dropna(), bins=20, color="#222", alpha=0.8)
            ax1.set_xlabel('Tempo de Internação (dias)')
            ax1.set_ylabel('Frequência')
            ax1.grid(axis='y', linestyle='--', alpha=0.3)
            st.pyplot(fig1)
        with col2:
            st.metric("Média", f"{df['Tempo_Internacao'].mean():.1f} dias")
            st.metric("Mediana", f"{df['Tempo_Internacao'].median():.1f} dias")
            st.metric("Máximo", f"{df['Tempo_Internacao'].max():.0f} dias")
    else:
        st.warning("Coluna 'Tempo_Internacao' não encontrada.")

    # Dashboard 2: Número de surtos por bactéria
    st.subheader("Número de surtos por bactéria")
    if 'Bactéria' in df.columns:
        contagem_bact = df['Bactéria'].dropna().value_counts()
        fig2, ax2 = plt.subplots(figsize=(8, 3.5))
        ax2.barh(contagem_bact.index, contagem_bact.values, color="#444", alpha=0.8)
        ax2.set_xlabel('Número de surtos')
        ax2.set_ylabel('Bactéria')
        ax2.grid(axis='x', linestyle='--', alpha=0.2)
        st.pyplot(fig2)
    else:
        st.warning("Coluna 'Bactéria' não encontrada.")

    # Dashboard 3: Casos por unidade hospitalar
    st.subheader("Casos por unidade hospitalar")
    if 'Unidade' in df.columns:
        casos_unidade = df['Unidade'].dropna().value_counts()
        fig3, ax3 = plt.subplots(figsize=(8, 3.5))
        ax3.barh(casos_unidade.index, casos_unidade.values, color="#888", alpha=0.8)
        ax3.set_xlabel('Número de casos')
        ax3.set_ylabel('Unidade Hospitalar')
        ax3.grid(axis='x', linestyle='--', alpha=0.2)
        st.pyplot(fig3)
    else:
        st.warning("Coluna 'Unidade' não encontrada.")

    # Dashboard 4: Evolução dos casos ao longo do tempo
    st.subheader("Evolução dos casos ao longo do tempo")
    if 'Data_Coleta' in df.columns:
        df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'], errors='coerce')
        casos_tempo = df.groupby('Data_Coleta').size().reset_index(name='Casos')
        casos_tempo = casos_tempo.sort_values('Data_Coleta')
        fig4, ax4 = plt.subplots(figsize=(10, 3.5))
        ax4.plot(casos_tempo['Data_Coleta'], casos_tempo['Casos'], marker='o', color="#222")
        ax4.set_xlabel('Data da Coleta')
        ax4.set_ylabel('Número de casos')
        ax4.grid(axis='y', linestyle='--', alpha=0.2)
        plt.xticks(rotation=45)
        st.pyplot(fig4)
    else:
        st.warning("Coluna 'Data_Coleta' não encontrada.")
