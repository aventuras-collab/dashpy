import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

# Carregar dados
df = pd.read_excel('estagioo.xlsx')

# Calcular estatísticas
media_idades = df['IDADE'].mean()
media_tempo_meses = df['Tempo em meses'].mean()
media_vencimento_total = df['Total de vencimentos'].mean()

# Visualizações
fig_pie = px.pie(df, values='Quantidade', names='Gênero', title='Distribuição por Gênero')

# Layout da aplicação Streamlit
st.title("Dashboard de Visualização da Tabela de Estágios Não Obrigatórios")
st.plotly_chart(fig_pie, use_container_width=True)
st.write(f"Média das Idades: {media_idades:.2f} anos")
st.write(f"Média do Tempo em Meses: {media_tempo_meses:.2f} meses")
st.write(f"Média do Vencimento Total: R$ {media_vencimento_total:.2f}")
