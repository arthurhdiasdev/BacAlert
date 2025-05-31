import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard de Surtos de Bactérias no Hospital")

arquivo = st.file_uploader("Faça upload da tabela Excel", type=["xlsx", "xls"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.write("Dados carregados:")
    st.dataframe(df)

    st.subheader("Resumo estatístico")
    st.write(df.describe(include='all'))

    # Dashboard 1: Histograma do Tempo de Internação
    st.subheader("Histograma do Tempo de Internação")
    if 'Tempo_Internacao' in df.columns:
        fig1, ax1 = plt.subplots()
        df['Tempo_Internacao'].hist(bins=20, ax=ax1)
        ax1.set_xlabel('Tempo de Internação (dias)')
        ax1.set_ylabel('Frequência')
        st.pyplot(fig1)
    else:
        st.warning("Coluna 'Tempo_Internacao' não encontrada.")

    # Dashboard 2: Número de surtos por bactéria
    st.subheader("Número de surtos por bactéria")
    if 'Bactéria' in df.columns:
        contagem_bact = df['Bactéria'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(8,4))
        sns.barplot(x=contagem_bact.index, y=contagem_bact.values, ax=ax2)
        ax2.set_xlabel('Bactéria')
        ax2.set_ylabel('Número de surtos')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig2)
    else:
        st.warning("Coluna 'Bactéria' não encontrada.")

    # Dashboard 3: Casos por unidade hospitalar
    st.subheader("Casos por unidade hospitalar")
    if 'Unidade' in df.columns:
        casos_unidade = df['Unidade'].value_counts()
        fig3, ax3 = plt.subplots(figsize=(8,4))
        sns.barplot(x=casos_unidade.index, y=casos_unidade.values, ax=ax3)
        ax3.set_xlabel('Unidade Hospitalar')
        ax3.set_ylabel('Número de casos')
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig3)
    else:
        st.warning("Coluna 'Unidade' não encontrada.")

    # Dashboard 4: Evolução dos casos ao longo do tempo
    st.subheader("Evolução dos casos ao longo do tempo")
    if 'Data_Coleta' in df.columns:
        df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'], errors='coerce')
        casos_tempo = df.groupby('Data_Coleta').size().reset_index(name='Casos')
        fig4, ax4 = plt.subplots(figsize=(10,4))
        sns.lineplot(data=casos_tempo, x='Data_Coleta', y='Casos', ax=ax4)
        ax4.set_xlabel('Data da Coleta')
        ax4.set_ylabel('Número de casos')
        st.pyplot(fig4)
    else:
        st.warning("Coluna 'Data_Coleta' não encontrada.")
