import streamlit as st
import plotly.express as px

# Dados simples para o gráfico
data = {
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Grapes'],
    'Amount': [10, 15, 7, 12]
}

# Criação do DataFrame
df = pd.DataFrame(data)

# Criação do gráfico de barras
fig = px.bar(df, x='Fruit', y='Amount', title='Quantidade de Frutas')

# Layout da aplicação Streamlit
st.title('Teste Simples de Streamlit com Plotly')
st.plotly_chart(fig)

st.write("Aplicação executada com sucesso!")
