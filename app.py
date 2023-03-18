import streamlit as st
from functions import executar
import pandas as pd

st.set_page_config(
    page_title="Coopemg file lock",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título da página
st.title("Coopemg File Lock")

# Seção para buscar arquivos com lock
st.subheader("Verificar lock de arquivos da coopemg")
st.write("Digite os parâmetros de busca abaixo:")

# Entrada de texto para os parâmetros de busca
parametro = st.text_input("Parâmetros de busca")

# Botão para executar a busca
btn_executar = st.button("Executar")

# Exibição dos resultados da busca
if btn_executar:
    retorno = executar(parametro)
    if retorno:
        columns = ["Usuário", "Arquivo/Diretório aberto", "Data/Hora"]
        df = pd.DataFrame(retorno, columns=columns)
        st.table(df)

    else:
        st.warning("Nenhum arquivo encontrado com lock.")
