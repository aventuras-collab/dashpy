import streamlit as st
import pandas as pd

# Dados simples para exibir
data = {
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Grapes'],
    'Amount': [10, 15, 7, 12]
}

# Criação do DataFrame
df = pd.DataFrame(data)

# Layout da aplicação Streamlit
st.title('Teste Simples de Streamlit sem Plotly')
st.write("Tabela de Dados:")
st.dataframe(df)

st.write("Aplicação executada com sucesso!")
