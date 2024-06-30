import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import requests
from io import BytesIO

# Definir o tema padrão para plotly
pio.templates.default = "plotly_dark"

# URL do arquivo no GitHub
url = 'https://github.com/aventuras-collab/dashpy/raw/main/estagioo.xlsx'

# Baixar o arquivo do GitHub
response = requests.get(url)
file = BytesIO(response.content)

# Carregar o arquivo Excel usando pandas
df = pd.read_excel(file)

# Calcular as médias
media_idades = df['IDADE'].mean()
media_tempo_meses = df['Tempo em meses'].mean()
media_vencimento_total = df['Total de vencimentos'].mean()

# Normalizar os valores da coluna 'GÊNERO'
df['GÊNERO'] = df['GÊNERO'].str.strip().str.lower().replace({
    'feminino': 'Feminino',
    'masculino': 'Masculino'
}).fillna('vazio')

# Contar a quantidade de cada gênero
gender_counts = df['GÊNERO'].value_counts().reset_index()
gender_counts.columns = ['Gênero', 'Quantidade']

# Criar uma figura de pizza
fig_pie = px.pie(gender_counts, values='Quantidade', names='Gênero', title='Distribuição por Gênero')
fig_pie.update_traces(marker=dict(colors=['#ff69b4', '#1e90ff']))  # rosa para feminino, azul para masculino
fig_pie.update_layout(title_x=0.5, font=dict(size=18, family='Arial, sans-serif', color='white'))

# Layout da aplicação Streamlit
st.set_page_config(page_title="Dashpy", layout="wide")
st.title("Dashboard de Visualização da Tabela de Estágios Não Obrigatórios")

# Exibir o gráfico
st.plotly_chart(fig_pie, use_container_width=True)

# Exibir as estatísticas
st.markdown("### Estatísticas")
st.metric(label="Média das Idades", value=f"{media_idades:.2f} anos")
st.metric(label="Média do Tempo em Meses", value=f"{media_tempo_meses:.2f} meses")
st.metric(label="Média do Vencimento Total", value=f"R$ {media_vencimento_total:.2f}")

st.write("Aplicação Streamlit executada com sucesso!")

