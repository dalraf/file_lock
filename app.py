import streamlit as st
from functions import executar

st.set_page_config(
    page_title="Coopemg file lock",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("### Verificar lock de arquivos da coopemg")

parametro = st.text_input('*Paramentos de busca*')


if st.button("Executar"):
    if parametro != '':
        retorno = executar(parametro)
        for line in retorno:
            st.markdown(line)

    
