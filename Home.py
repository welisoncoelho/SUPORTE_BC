import streamlit as st
import pandas as pd
from IPython.display import IFrame

# Carregar os dados do arquivo Excel
df = pd.read_csv("CHAMADOS_FRANQUIA.csv", encoding="utf-8", dayfirst=True, parse_dates=["Data de abertura", "Data de fechamento", "Data Final SLA Violado"])

# Filtrar o DataFrame (se necessário)
filtered_df = df

# Define a session state variable to store authentication status
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Function to check password and set authentication status
def check_password():
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state.authenticated = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # First run or not authenticated, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    else:
        # Authenticated, allow access to the content
        return True

# Check password before displaying any content
if not check_password():
    st.warning("Authentication failed. Please enter valid credentials.")
    st.stop()  # Stop execution if not authenticated

media_por_unidade = filtered_df.groupby('Unidade de Negócio')['Nome da conta'].count().mean()

# Contar o número de vezes que o nome da conta aparece no DataFrame
count = filtered_df['Unidade de Negócio'].value_counts()
count_dias = filtered_df['Data de abertura'].value_counts()
count_nivel1 = filtered_df['Nível 1'].value_counts()
count_nivel_3 = filtered_df['Nível 2'].value_counts()
count_nivel_5 = filtered_df['Nível 5'].value_counts()

# Calcular a média de registros por "Data de abertura"
media_registros = count_dias.mean() 

# Sidebar menu
st.sidebar.markdown("# Menu de Navegação")

# Add links to different pages
selected_page = st.sidebar.selectbox("Selecione a página desejada:", ["Análise Chamados", "Página Analistas","Página Clientes Ofensores","Contato de Clientes","Bi Linx"])

# Main content
st.markdown("#📊 RCA BC CONSULTÓRIA📊")

if selected_page == "Análise Chamados":
       st.title("Dash Principal")
    # Adicione o conteúdo específico da Página Chamados aqui.
              # Converta a coluna 'Data de abertura' para o formato de data e hora
       df['Data de abertura'] = pd.to_datetime(df['Data de abertura'])

       # Filtros para "Unidade de Negócio" e "Nome da conta"
       selected_unidade_negocio_1 = st.selectbox("Selecione a Unidade de Negócio", ['Todos'] + list(df['Unidade de Negócio'].unique()))
       selected_nome_conta_1 = st.selectbox("Selecione o Nome da Conta", ['Todos'] + list(df['Nome da conta'].unique()))

       # Filtros para data inicial e final
       selected_data_inicial = st.date_input("Selecione a Data Inicial")
       selected_data_final = st.date_input("Selecione a Data Final")

       # Aplicar os filtros
       filtered_df = df.copy()  # Crie uma cópia do DataFrame original
       if selected_unidade_negocio_1 != 'Todos':
              filtered_df = filtered_df[filtered_df['Unidade de Negócio'] == selected_unidade_negocio_1]
       if selected_nome_conta_1 != 'Todos':
              filtered_df = filtered_df[filtered_df['Nome da conta'] == selected_nome_conta_1]
       if selected_data_inicial and selected_data_final:
              filtered_df = filtered_df[(filtered_df['Data de abertura'].dt.date >= selected_data_inicial) &
                                   (filtered_df['Data de abertura'].dt.date <= selected_data_final)]
       

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

       # Crie duas colunas na mesma linha
       col1, col2 = st.columns(2)

       # Plote o gráfico de barras na primeira coluna
       col1.bar_chart(count)

       # Exiba a tabela na segunda coluna (abaixo da primeira)
       col2.line_chart(count_dias)


       # Mostre o total de registros
       total_registros = filtered_df.shape[0]
       st.write("Total de Registros:", total_registros, font=("arial", 24))

       # Exiba a média de registros em um card
       st.write("Média de registros por Data de Abertura:", f"{media_registros:.2f}")

       # Exiba a tabela de contagem de registros
       st.markdown("## Chamados por unidade de Negócio")
       st.table(count)

       st.markdown("## Chamados Por Classes")
       st.table(count_nivel1)

       st.markdown("## Chamados Por Modulos")
       st.table(count_nivel_3)

       st.markdown("## Ofensores")
       st.table(count_nivel_5)          
#########################################################################################################################################
elif selected_page == "Página Analistas":
       filtered_df = df

       st.markdown('## Dados Analistas')

       # Converta a coluna 'Data de fechamento' para o formato de data e hora
       df = pd.read_csv("CHAMADOS_FRANQUIA.csv", encoding="utf-8", dayfirst=True, parse_dates=["Data de abertura", "Data de fechamento", "Data Final SLA Violado"])


       # Filtros para "Unidade de Negócio" e "Nome da conta"
       selected_unidade_negocio_2 = st.selectbox("Selecione a Unidade de Negócio", ['Todos'] + list(df['Unidade de Negócio'].unique()))
       selected_nome_conta_2 = st.selectbox("Selecione o Analista", ['Todos'] + list(df['Alias do proprietário do caso'].unique()))

       # Filtros para data inicial e final
       selected_data_inicial = st.date_input("Selecione a Data Inicial")
       selected_data_final = st.date_input("Selecione a Data Final")

       # Aplicar os filtros
       filtered_df = df.copy()  # Crie uma cópia do DataFrame original
       if selected_unidade_negocio_2 != 'Todos':
              filtered_df = filtered_df[filtered_df['Unidade de Negócio'] == selected_unidade_negocio_2]
       if selected_nome_conta_2 != 'Todos':
              filtered_df = filtered_df[filtered_df['Alias do proprietário do caso'] == selected_nome_conta_2]
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
              
##############################################################################################################################################
    



elif selected_page == "Página Clientes Ofensores":
    st.title("Página Clientes Ofensores")
    # Adicione o conteúdo específico da Página Clientes Ofensores aqui.



       # Converta a coluna 'Data de abertura' para o formato de data e hora
              # Converta a coluna 'Data de abertura' para o formato de data e hora
    df['Data de abertura'] = pd.to_datetime(df['Data de abertura'], format="%d/%m/%Y")

       # Filtros para "Unidade de Negócio" e "Nome da conta"
    selected_unidade_negocio_3 = st.selectbox("Selecione a Unidade de Negócio", ['Todos'] + list(df['Unidade de Negócio'].unique()), key="clientes_unidade_negocio")
    selected_nome_conta_3 = st.selectbox("Selecione o Nome da Conta", ['Todos'] + list(df['Nome da conta'].unique()), key="clientes_nome_conta")

       # Filtros para data inicial e final
    selected_data_inicial = st.date_input("Selecione a Data Inicial", key="data_inicial_clientes_ofensores")
    selected_data_final = st.date_input("Selecione a Data Final",key="data_final_clientes_ofensores")

       # Aplicar os filtros
    filtered_df = df.copy()  # Crie uma cópia do DataFrame original
    if selected_unidade_negocio_3 != 'Todos':
      filtered_df = filtered_df[filtered_df['Unidade de Negócio'] == selected_unidade_negocio_3]  # Corrigido para usar selected_unidade_negocio_3
    if selected_nome_conta_3 != 'Todos':
       filtered_df = filtered_df[filtered_df['Nome da conta'] == selected_nome_conta_3]  # Corrigido para usar selected_nome_conta_3
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
       count_uf =filtered_df ['Estado'].value_counts()

       st.markdown("# Acionamento por Estado")
       st.bar_chart(count_uf)

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

       

elif selected_page == "Contato de Clientes":
    st.title("Relação de Clientes")

    # Converta a coluna 'Data de abertura' para o formato de data e hora
    df['Data de abertura'] = pd.to_datetime(df['Data de abertura'], format="%d/%m/%Y")

    # Filtros para "Unidade de Negócio" e "Nome da conta"
    selected_unidade_negocio_3 = st.selectbox("Selecione a Unidade de Negócio", ['Todos'] + list(df['Unidade de Negócio'].unique()), key="clientes_unidade_negocio")
    selected_nome_conta_3 = st.selectbox("Selecione o Nome da Conta", ['Todos'] + list(df['Nome da conta'].unique()), key="clientes_nome_conta")

    # Filtro para o Estado
    selected_estado = st.selectbox("Selecione o Estado", ['Todos'] + list(df['Estado'].unique()), key="clientes_estado")

    # Filtros para data inicial e final
    selected_data_inicial = st.date_input("Selecione a Data Inicial", key="data_inicial_clientes_ofensores")
    selected_data_final = st.date_input("Selecione a Data Final",key="data_final_clientes_ofensores")

    # Aplicar os filtros
    filtered_df = df.copy()  # Crie uma cópia do DataFrame original

    if selected_unidade_negocio_3 != 'Todos':
        filtered_df = filtered_df[filtered_df['Unidade de Negócio'] == selected_unidade_negocio_3]

    if selected_nome_conta_3 != 'Todos':
        filtered_df = filtered_df[filtered_df['Nome da conta'] == selected_nome_conta_3]

    if selected_estado != 'Todos':
        filtered_df = filtered_df[filtered_df['Estado'] == selected_estado]

    if selected_data_inicial and selected_data_final:
        filtered_df = filtered_df[(filtered_df['Data de abertura'].dt.date >= selected_data_inicial) &
                                   (filtered_df['Data de abertura'].dt.date <= selected_data_final)]

    columns = ['Nome da conta', 'Nome do contato', 'Contato: Email', 'Contato: Telefone', 'Estado']
    st.dataframe(filtered_df[columns], width=1500, height=1500)

elif selected_page == "BI LINX":
    st.title("BI LINX")
    import streamlit as st

# URL do Power BI
power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiODJkNGVhNGQtMDA2Zi00YmQ2LWIxYzMtN2E4OGE5Y2NlZWMwIiwidCI6ImM1OGY4NTY1LTdhYjQtNDQwZi04NGYyLWRkNzVmMzc0NWE2OSIsImMiOjR9"

# Display the content of the IFrame using Streamlit
st.write(f'<iframe width="800" height="600" src="{power_bi_url}"></iframe>', unsafe_allow_html=True)
