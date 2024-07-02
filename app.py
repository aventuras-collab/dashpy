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

# Definir as faixas etárias
bins = [0, 21, 25, 29, 34, 100]
labels = ['-18 até 21', '22 até 25', '26 até 29', '30 até 34', '35 ou +']
df['Faixa Etária'] = pd.cut(df['IDADE'], bins=bins, labels=labels, right=False)

# Contar a quantidade de pessoas em cada faixa etária e gênero
age_gender_counts = df[df['GÊNERO'] != 'vazio'].groupby(['Faixa Etária', 'GÊNERO'], observed=False).size().unstack().fillna(0)

# Criar a pirâmide etária
trace1 = go.Bar(
    y=age_gender_counts.index,
    x=-age_gender_counts['Masculino'],
    name='Masculino',
    orientation='h',
    marker=dict(color='#1e90ff')
)
trace2 = go.Bar(
    y=age_gender_counts.index,
    x=age_gender_counts['Feminino'],
    name='Feminino',
    orientation='h',
    marker=dict(color='#ff69b4')
)

data_pyramid = [trace1, trace2]

layout_pyramid = go.Layout(
    title='Distribuição Etária por Gênero',
    title_x=0.5,
    barmode='overlay',
    bargap=0.1,
    xaxis=dict(title='Quantidade'),
    yaxis=dict(title='Faixa Etária', categoryorder='category ascending'),
    template='plotly_dark',
    font=dict(size=18, family='Arial, sans-serif', color='white')
)

fig_pyramid = go.Figure(data=data_pyramid, layout=layout_pyramid)

# Lista de cidades da região metropolitana de Recife
rmr_cities = [
    'recife', 'olinda', 'jaboatão dos guararapes', 'paulista', 'cabo de santo agostinho',
    'camaragibe', 'igarassu', 'abreu e lima', 'ipojuca', 'itapissuma', 'moreno', 'araçoiaba',
    'itamaracá', 'são lourenço da mata'
]

# Normalizar a coluna 'CIDADE'
df['CIDADE'] = df['CIDADE'].str.strip().str.lower()

# Categorizar as cidades corretamente
def categorize_city(city):
    if pd.isna(city) or city == '':
        return 'vazio'
    elif city == 'recife':
        return 'Recife'
    elif city in rmr_cities:
        return 'Dentro da RMR'
    else:
        return 'Fora da RMR'

df['Região Metropolitana'] = df['CIDADE'].apply(categorize_city)

# Contar a quantidade de pessoas em cada categoria
rmr_counts = df['Região Metropolitana'].value_counts().reset_index()
rmr_counts.columns = ['Categoria', 'Quantidade']

# Criar uma figura de barras para a distribuição das cidades
fig_rmr = px.bar(rmr_counts, x='Categoria', y='Quantidade', title='Distribuição por Região Metropolitana', color='Categoria')
fig_rmr.update_layout(title_x=0.5, font=dict(size=18, family='Arial, sans-serif', color='white'))

# Analisar a coluna de iniciativa
df['INICIATIVA'] = df['INICIATIVA'].str.strip().str.lower().fillna('vazio')
initiative_counts = df['INICIATIVA'].value_counts().reset_index()
initiative_counts.columns = ['Iniciativa', 'Quantidade']

# Criar uma figura de pizza para a distribuição de iniciativas
fig_initiative_pie = go.Figure(data=[go.Pie(
    labels=initiative_counts['Iniciativa'], 
    values=initiative_counts['Quantidade'],
    hole=.4,
    textinfo='percent',
    textfont=dict(size=16, color='white'),
    marker=dict(colors=px.colors.qualitative.Plotly)
)])
fig_initiative_pie.update_layout(
    title='Distribuição por Iniciativa',
    title_x=0.5,
    font=dict(size=18, family='Arial, sans-serif', color='white'),
    annotations=[dict(text='Iniciativas', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# Identificar o nome exato da coluna 'TIPO\nCONVÊNIO'
convenio_column_name = [col for col in df.columns if 'CONVÊNIO' in col][0]

# Analisar a coluna de convênios
df['TIPO_CONVÊNIO'] = df[convenio_column_name].str.strip().str.lower().replace({
    'agente de integração': 'agente de integração',
    'concedente': 'concedente',
    'unidade da ufpe': 'unidade da ufpe'
}).fillna('vazio')
convenio_counts = df['TIPO_CONVÊNIO'].value_counts().reset_index()
convenio_counts.columns = ['Tipo de Convênio', 'Quantidade']

# Criar uma figura de pizza para a distribuição de tipos de convênios
fig_convenio_pie = go.Figure(data=[go.Pie(
    labels=convenio_counts['Tipo de Convênio'], 
    values=convenio_counts['Quantidade'],
    pull=[0.1, 0, 0],
    textinfo='percent+label',
    textfont=dict(size=16, color='white'),
    marker=dict(colors=px.colors.qualitative.Set2)
)])
fig_convenio_pie.update_layout(
    title='Distribuição por Tipo de Convênio',
    title_x=0.5,
    font=dict(size=18, family='Arial, sans-serif', color='white')
)

# Identificar o nome exato da coluna 'AGENTE\nINTEGRAÇÃO'
agente_column_name = [col for col in df.columns if 'INTEGRAÇÃO' in col][0]

# Analisar a coluna de agentes de integração
df['AGENTE_INTEGRAÇÃO'] = df[agente_column_name].str.strip().str.lower().fillna('vazio')
top_5_agentes = df[df['AGENTE_INTEGRAÇÃO'] != 'vazio']['AGENTE_INTEGRAÇÃO'].value_counts().nlargest(5).reset_index()
top_5_agentes.columns = ['Agente de Integração', 'Quantidade']

# Criar uma figura de barras para os top 5 agentes de integração
fig_top_5_agentes = px.bar(top_5_agentes, x='Agente de Integração', y='Quantidade', title='Top 5 Agentes de Integração')
fig_top_5_agentes.update_layout(title_x=0.5, font=dict(size=18, family='Arial, sans-serif', color='white'))

# Identificar o nome exato da coluna 'CARGA\nHORÁRIA'
carga_horaria_column_name = [col for col in df.columns if 'CARGA' in col][0]

# Analisar a coluna de carga horária
df['CARGA_HORÁRIA'] = df[carga_horaria_column_name].str.lower().str.strip()

# Criar um ranking dos tipos de 'CARGA_HORÁRIA'
carga_horaria_ranking = df['CARGA_HORÁRIA'].value_counts().reset_index()
carga_horaria_ranking.columns = ['CARGA_HORARIA', 'COUNT']

# Extrair a parte numérica da coluna 'CARGA_HORÁRIA'
df['CARGA_HORARIA_NUM'] = df['CARGA_HORÁRIA'].str.extract('(\\d+)').astype(float)

# Calcular a média da carga horária
average_carga_horaria = df['CARGA_HORARIA_NUM'].mean()

# Criar um gráfico de barras usando Plotly
fig_carga_horaria = px.bar(carga_horaria_ranking, x='CARGA_HORARIA', y='COUNT', 
                           labels={'CARGA_HORARIA': 'Carga Horária', 'COUNT': 'Contagem'},
                           title='Distribuição de Carga Horária')
fig_carga_horaria.update_layout(title_x=0.5, font=dict(size=18, family='Arial, sans-serif', color='white'))

# Iniciar a aplicação Streamlit
st.set_page_config(page_title="Dashpy", layout="wide")

# Ajustar o fundo para uma mescla de azul escuro e preto
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #1a1a2e;
    }
    .css-1d391kg {
        background-color: #1a1a2e;
    }
    .css-1v3fvcr {
        background-color: #16213e;
    }
    .css-1offfwp {
        background-color: #1a1a2e;
    }
    .card {
        background-color: #2a3b4c;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-family: 'Arial, sans-serif';
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 24px;
        margin-bottom: 10px;
    }
    .card-value {
        font-size: 28px;
        font-weight: bold;
    }
    .css-1pjc44v {
        font-family: 'Arial, sans-serif';
    }
    .css-hxt7ib {
        font-family: 'Arial, sans-serif';
    }
    h1 {
        text-align: center;
        color: white;
        font-family: 'Arial, sans-serif';
    }
    h2 {
        text-align: center;
        color: white;
        font-family: 'Arial, sans-serif';
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Dashboard de Visualização da Tabela de Estágios Não Obrigatórios")

# Exibir os gráficos
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    st.plotly_chart(fig_pyramid, use_container_width=True)

st.plotly_chart(fig_rmr, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_initiative_pie, use_container_width=True)
with col2:
    st.plotly_chart(fig_convenio_pie, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_top_5_agentes, use_container_width=True)
with col2:
    st.plotly_chart(fig_carga_horaria, use_container_width=True)

# Exibir as estatísticas em "cards"
st.markdown("---")
st.markdown("### Estatísticas")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="card">
            <div class="card-title">Média das Idades</div>
            <div class="card-value">{:.2f} anos</div>
        </div>
    """.format(media_idades), unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="card">
            <div class="card-title">Média do Tempo em Meses</div>
            <div class="card-value">{:.2f} meses</div>
        </div>
    """.format(media_tempo_meses), unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="card">
            <div class="card-title">Média do Vencimento Total</div>
            <div class="card-value">R$ {:.2f}</div>
        </div>
    """.format(media_vencimento_total), unsafe_allow_html=True)

