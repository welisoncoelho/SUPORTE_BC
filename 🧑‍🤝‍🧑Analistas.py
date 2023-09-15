import streamlit as st
import pandas as pd
import openpyxl as op


# Carregar os dados do arquivo Excel
# Carregar os dados do arquivo Excel
df = pd.read_excel("CHAMADOS_FRANQUIA.xlsx")

# Filtrar o DataFrame (se necessário)
filtered_df = df

st.markdown('## Dados Analistas')

# Converta a coluna 'Data de fechamento' para o formato de data e hora
df['Data de fechamento'] = pd.to_datetime(df['Data de fechamento'])

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
    filtered_df = filtered_df[(filtered_df['Data de fechamento'].dt.date >= selected_data_inicial) &
                              (filtered_df['Data de fechamento'].dt.date <= selected_data_final)]

    
dta_fechamento = filtered_df['Data de fechamento'].value_counts()


# Calcular a média individual de chamados por Alias do proprietário do caso
media_por_alias = filtered_df.groupby('Alias do proprietário do caso').size().reset_index(name='Média de Chamados')

st.title("Chamados por Analista")
st.table(media_por_alias)

st.title("Chamados Concluidos Por Data")
st.line_chart(dta_fechamento)

# Criar um DataFrame que contenha a contagem de chamados concluídos por data e analista
chamados_por_data_e_analista = filtered_df.groupby(['Data de fechamento', 'Alias do proprietário do caso']).size().reset_index(name='Chamados Concluídos')

# Calcular a média de chamados concluídos por data individualmente para cada analista
media_por_data_e_analista = chamados_por_data_e_analista.groupby('Alias do proprietário do caso')['Chamados Concluídos'].mean().reset_index(name='Média de Chamados Concluídos')

# Formatar a coluna de média com duas casas decimais
media_por_data_e_analista['Média de Chamados Concluídos'] = media_por_data_e_analista['Média de Chamados Concluídos'].apply(lambda x: f'{x:.2f}')

st.title("Média de Chamados Concluídos Por Data")
st.table(media_por_data_e_analista)

valores_unicos = filtered_df['FCR Formula'].value_counts()
valores_unicos_sla = filtered_df['Data Final SLA Violado'].value_counts()

# Calcular o percentual formatado com 2 casas decimais
percentual = valores_unicos / len(filtered_df) * 100
percentual_formatado = percentual.apply(lambda x: f"{x:.2f}%")




# Criar um DataFrame com a contagem e o percentual formatado
df_contagem_percentual = pd.DataFrame({'Contagem': valores_unicos, 'Percentual (%)': percentual_formatado})

# Exibir a contagem e o percentual em uma tabela
st.title("FCR")
st.table(df_contagem_percentual)


# Calcular o percentual formatado com 2 casas decimais para "Data Final SLA Violado"
valores_unicos_sla = filtered_df['Data Final SLA Violado'].value_counts()
percentual_sla = valores_unicos_sla / len(filtered_df) * 100
percentual_formatado_sla = percentual_sla.apply(lambda x: f"{x:.2f}%")

# Criar um DataFrame com a contagem e o percentual formatado para "Data Final SLA Violado"
df_contagem_percentual_sla = pd.DataFrame({'Contagem': valores_unicos_sla, 'Percentual (%)': percentual_formatado_sla})

# Exibir a contagem e o percentual em uma tabela para "Data Final SLA Violado"
st.title("% SLA")
st.table(df_contagem_percentual_sla)

#col1,col2 = st.columns(2)

# Exibir o gráfico de pizza no Streamlit
#col1.title("Gráfico FCR")

#col1.bar_chart(df_contagem_percentual)


# Exibir o gráfico de pizza no Streamlit para "Data Final SLA Violado"
#col2.title("SLA")
#col2.bar_chart(df_contagem_percentual_sla)
