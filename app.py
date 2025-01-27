import os
import pandas as pd
import oracledb  # Substituindo cx_Oracle por python-oracledb
import streamlit as st
import time
from datetime import datetime, timedelta


def reload_page_with_params(**params):
    """Força a página a recarregar ao definir parâmetros na URL."""
    st.experimental_set_query_params(**params)
    st.stop()


def formatar_numero(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_posit(valor):
    return f"{valor:,.0f}".replace(",", ".")


def style_metric_cards(border_left_color="#3e4095"):
    st.markdown(
        f"""
        <style>
        [data-testid="stMetricValue"] {{
            font-size: 20px;
        }}
        [data-testid="metric-container"] {{
            border-left: 5px solid {border_left_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def carregar_dados(query):
    try:
<<<<<<< HEAD:app/app.py
        # Habilitar o modo Thick (necessário para versões antigas do Oracle)
        oracledb.init_oracle_client(
            lib_dir=r"C:\oracle\instantclient_21_16")  # Ajuste o caminho

        # Configurar o DSN
        dsn_tns = oracledb.makedsn(
            "192.168.254.200",  # Endereço do servidor
            1521,  # Porta do Oracle
            service_name="DBPROD"  # Nome do serviço
        )

        # Conexão com o banco de dados
        conexao = oracledb.connect(
            user="CONSULTAPOWERBI",
            password="S0STQUERYPB",
            dsn=dsn_tns
        )

        # Executar a consulta e carregar os dados no DataFrame
=======
        oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient")  # Ajuste o caminho
        dsn_tns = oracledb.makedsn("192.168.254.200", 1521, service_name="DBPROD")
        conexao = oracledb.connect(user="CONSULTAPOWERBI", password="S0STQUERYPB", dsn=dsn_tns)
>>>>>>> 9ecfb98de3fd8772ce0c7402c5a320858dc8ca37:app.py
        df = pd.read_sql(query, conexao)
        conexao.close()
        return df

    except oracledb.DatabaseError as e:
        error, = e.args
        st.error(f"Erro ao conectar ao banco de dados: {error.message}")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return pd.DataFrame()


def aplicar_filtros(df, filtro_data, filtro_supervisor, filtro_nomerca):
    df_filtrado = df.copy()

    if filtro_data:
        filtro_data = pd.to_datetime(filtro_data)
        df_filtrado = df_filtrado[df_filtrado['DATA'] == filtro_data]

    if filtro_supervisor:
        df_filtrado = df_filtrado[df_filtrado['SUPERVISOR'].str.contains(
            filtro_supervisor, case=False, na=False)]

    if filtro_nomerca:
        df_filtrado = df_filtrado[df_filtrado['NOME'].str.contains(
            filtro_nomerca, case=False, na=False)]

    return df_filtrado


def exibir_metricas(df):
    total_meta = round(df['VLVENDAPREV'].sum(), 2)
    total_valorliquido = round(df['VL_LIQ_DSV_FAT'].sum(), 2)
    total_valorpedido = round(df['VL_LIQ_DSV_PED'].sum(), 2)
    total_gapdia = round(df['GAP_DIA'].sum(), 2)
    total_metanova = round(df['META_NOVA'].sum(), 2)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("R$ META", formatar_numero(total_meta))
        style_metric_cards()

    with col2:
        st.metric("R$ VALOR FATURADO", formatar_numero(total_valorliquido))

    with col3:
        st.metric("R$ PEDIDOS", formatar_numero(total_valorpedido))

    with col4:
        st.metric("R$ GAP DIA", formatar_numero(total_gapdia))

    with col5:
        st.metric("R$ META NOVA", formatar_numero(total_metanova))


def main():
    st.title("Tabela de Vendas 📊")

    # Controle da última atualização
    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.now()

    # Botão para atualização manual
    update_button = st.sidebar.button("Atualizar Dados Manualmente")

    # Definir intervalo para atualização automática (1 hora)
    auto_refresh_interval = timedelta(hours=1)
    now = datetime.now()

    # Atualização automática
    if now - st.session_state.last_update >= auto_refresh_interval:
        st.session_state.last_update = now
        st.session_state['reload'] = True
        reload_page_with_params(reload="auto")

    # Atualização manual
    if update_button:
        st.session_state.last_update = now
        st.session_state['reload'] = True
        reload_page_with_params(reload="manual")

    # Exibir informações de atualização na barra lateral
    st.sidebar.write(f"Última atualização: {st.session_state.last_update.strftime('%d/%m/%Y %H:%M:%S')}")
    st.sidebar.write("A próxima atualização automática será em 1 hora.")

    # Consulta SQL
    query = """
    SELECT * FROM DBAUSER.VIEW_PBI_METAPEDIDODIA T1
    WHERE T1.CODSUPERVISOR <> 39
    """

    # Carregar os dados
    start_time = time.time()
    df = carregar_dados(query)
    st.write(f"Tempo para carregar dados: {
             time.time() - start_time:.2f} segundos")

    if df.empty:
        st.warning("Nenhum dado encontrado.")
        return

    # Filtros na barra lateral
    with st.sidebar:
<<<<<<< HEAD:app/app.py
        st.image("E:/GitHub_Workspace/Projetos/MetaPedidoDia/LOGO SOST NOVO.png",
                 use_container_width=True)
=======
>>>>>>> 9ecfb98de3fd8772ce0c7402c5a320858dc8ca37:app.py
        filtro_data = st.date_input("Filtrar por Data")
        filtro_supervisor = st.text_input("Filtrar por Supervisor:")
        filtro_nomerca = st.text_input("Filtrar por NomeRca:")

    # Aplicar os filtros
    df_filtrado = aplicar_filtros(df, filtro_data, filtro_supervisor, filtro_nomerca)

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado após aplicar os filtros.")
        return

    # Exibir métricas
    exibir_metricas(df_filtrado)

    # Exibir DataFrame filtrado
    st.dataframe(df_filtrado)

    st.write(f"Tamanho do DataFrame final: {df_filtrado.shape}")


if __name__ == "__main__":
    main()
