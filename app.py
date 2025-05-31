import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Título do app
st.title("Análise de Dados") 

# Upload de arquivo
arquivo = st.file_uploader("envie aqui seu arquivo .xlsx", type=["xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)
    st.write("Dados carregados:")
    st.dataframe(df)

    st.subheader("Resumo estatístico")
    st.write(df.describe())

    # Selecionar coluna para gráfico
    coluna = st.selectbox("Escolha uma coluna numérica para ver o histograma", df.select_dtypes(include='number').columns)

    # Exibir histograma
    fig, ax = plt.subplots()
    df[coluna].hist(bins=20, ax=ax)
    st.pyplot(fig)