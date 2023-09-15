import streamlit as st
import pandas as pd
import openpyxl as op


# Carregar os dados do arquivo Excel


# Filtrar o DataFrame com base na data selecionada

    # Exibir o DataFrame filtrado no Streamlit
st.markdown("#📊 RCA BC CONSULTÓRIA📊")
    ##st.image("linx.png")

# Carregar os dados do arquivo Excel

df = pd.read_csv("CHAMADOS_FRANQUIA.csv", encoding="utf-8")

# Filtrar o DataFrame (se necessário)
filtered_df = df



 # a média de chamados por unidade de negócio
media_por_unidade = filtered_df.groupby('Unidade de Negócio')['Nome da conta'].count().mean()

# Contar o número de vezes que o nome da conta aparece no DataFrame
count = filtered_df['Unidade de Negócio'].value_counts()
count_dias = filtered_df['Data de abertura'].value_counts()
count_nivel1 = filtered_df['Nível 1'].value_counts()
count_nivel_3 = filtered_df['Nível 2'].value_counts()
count_nivel_5 = filtered_df['Nível 5'].value_counts()

# Calcular a média de registros por "Data de abertura"
media_registros = count_dias.mean() 

st.title("Análise Chamados") 


st.text("CHAMADOS POR UNIDADE DE NEGOCIO              CHAMADOS POR DATA")

# Crie duas colunas na mesma linha
col1, col2 = st.columns(2)

# Plote o gráfico de barras na primeira coluna


col1.bar_chart(count)

# Exiba a tabela na segunda coluna (abaixo da primeira)


col2.line_chart(count_dias)

# Exiba a média de registros em um card
st.write("Média de registros por Data de Abertura:", f"{media_registros:.2f}")


###################################################################################

dta_fechamento = filtered_df['Data de fechamento'].value_counts()


# Criar um DataFrame que contenha a contagem de chamados concluídos por data e analista
chamados_por_data_e_analista = filtered_df.groupby(['Data de fechamento', 'Alias do proprietário do caso']).size().reset_index(name='Chamados Concluídos')

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

# Criar um gráfico de pizza para os percentuais finais para "Data Final SLA Violado"
# Definir o tamanho da figura para o gráfico de pizza

col1,col2 = st.columns(2)

# Exibir o gráfico de pizza no Streamlit
##col1.title("Gráfico FCR")
##col1.bar_chart(df_contagem_percentual)


# Exibir o gráfico de pizza no Streamlit para "Data Final SLA Violado"
##col2.title("SLA")
##col2.line_chart(df_contagem_percentual_sla)

