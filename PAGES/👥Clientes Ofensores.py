import streamlit as st
import pandas as pd

# Carregar os dados do arquivo Excel
df = pd.read_excel("CHAMADOS_FRANQUIA.xlsx")


# Converta a coluna 'Data de abertura' para o formato de data e hora
df['Data de abertura'] = pd.to_datetime(df['Data de abertura'])

# Filtros para "Unidade de Negócio" e "Nome da conta"
selected_unidade_negocio = st.selectbox("Selecione a Unidade de Negócio", ['Todos'] + list(df['Unidade de Negócio'].unique()))
selected_nome_conta = st.selectbox("Selecione o Nome da Conta", ['Todos'] + list(df['Nome da conta'].unique()))

# Filtros para data inicial e final
selected_data_inicial = st.date_input("Selecione a Data Inicial")
selected_data_final = st.date_input("Selecione a Data Final")

# Aplicar os filtros
filtered_df = df.copy()  # Crie uma cópia do DataFrame original
if selected_unidade_negocio != 'Todos':
    filtered_df = filtered_df[filtered_df['Unidade de Negócio'] == selected_unidade_negocio]
if selected_nome_conta != 'Todos':
    filtered_df = filtered_df[filtered_df['Nome da conta'] == selected_nome_conta]
if selected_data_inicial and selected_data_final:
    filtered_df = filtered_df[(filtered_df['Data de abertura'].dt.date >= selected_data_inicial) &
                              (filtered_df['Data de abertura'].dt.date <= selected_data_final)]

# Calcular a média de chamados por unidade de negócio
media_por_unidade = filtered_df.groupby('Unidade de Negócio')['Nome da conta'].count().mean()


# Mostre o total de registros
total_registros = filtered_df.shape[0]
st.write("Total de Registros:", total_registros, font=("arial", 24))

# Contar o número de vezes que o nome da conta aparece no DataFrame
count = filtered_df['Nome da conta'].value_counts()
count_dias = filtered_df['Data de abertura'].value_counts()

# Calcular a média de registros por "Data de abertura"
media_registros = count_dias.mean()

st.title("Ofensores/clientes")

# Crie duas colunas na mesma linha
col1, col2 = st.columns(2)

# Plote o gráfico de barras na primeira coluna
col1.bar_chart(count)

# Exiba a tabela na segunda coluna (abaixo da primeira)
col2.line_chart(count_dias)

# Exiba a média de registros em um card
st.write("Média de registros por Data de Abertura:", f"{media_registros:.2f}")

# Contar o número de vezes que o nome da conta aparece no DataFrame
count = filtered_df['Unidade de Negócio'].value_counts()
count_dias = filtered_df['Data de abertura'].value_counts()

# Contar o número de vezes que o Nível 1 aparece no DataFrame
count_nivel1 = filtered_df['Nível 1'].value_counts()
count_nivel_3 = filtered_df['Nível 2'].value_counts()
count_nivel_5 = filtered_df['Nível 5'].value_counts()
count_clientes= filtered_df['Nome da conta'].value_counts()
count_contato= filtered_df['Nome do contato'].value_counts()



st.table(count_clientes)

# Exiba a tabela de contagem de registros
st.markdown("## Chamados por Unidade de Negócio")
st.table(count)

st.markdown("## Chamados Fila")
st.table(count_nivel1)

st.markdown("## Chamados Módulos")
st.table(count_nivel_3)

st.markdown("## Ofensores")
st.table(count_nivel_5)

# Exiba a tabela de contagem de registros
st.table(count)


# Exiba a tabela de contagem contatos
st.title("Relação de Contatos")
st.table(count_contato)


