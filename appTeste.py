import os
import pandas as pd
import cx_Oracle
import streamlit as st
import time


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
        # Configurar o caminho do Oracle Instant Client
        oracle_client_path = r"C:\oraclexe\app\oracle\product\11.2.0\server\bin"  # Ajuste conforme necessário
        if not os.path.exists(oracle_client_path):
            st.error("O caminho do Oracle Instant Client não é válido.")
            return pd.DataFrame()  # Retorna um DataFrame vazio

        os.environ["PATH"] = oracle_client_path + ";" + os.environ.get("PATH", "")
        cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

        # Obter variáveis de ambiente
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_service_name = os.getenv("DB_SERVICE_NAME")

        # Validar as variáveis de ambiente
        if not all([db_user, db_password, db_host, db_port, db_service_name]):
            st.error("Uma ou mais variáveis de ambiente do banco de dados não estão configuradas.")
            return pd.DataFrame()

        # Configurar o DSN
        dsn_tns = cx_Oracle.makedsn(db_host, db_port, service_name=db_service_name)

        # Conectar ao banco de dados
        conexao = cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn_tns)

        # Executar a query e carregar os dados no DataFrame
        df = pd.read_sql(query, conexao)
        conexao.close()
        return df
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        st.error(f"Erro ao conectar ao banco de dados: {error.message}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return pd.DataFrame()


def main():
    st.title("Tabela de Vendas 📊")

    # Consulta SQL
    query = """
    SELECT * FROM DBAUSER.VIEW_PBI_METAPEDIDODIA T1
    WHERE T1.CODSUPERVISOR <> 39
    """

    start_time = time.time()

    # Carregar os dados
    df = carregar_dados(query)
    st.write(f"Tempo para carregar dados: {time.time() - start_time:.2f} segundos")

    if df.empty:
        st.warning("Nenhum dado encontrado para os critérios informados.")
        return

# Recalcular os totais com base no DataFrame filtrado
    total_meta = round(df_filtrado['VLVENDAPREV'].sum(), 2)
    total_valorliquido = round(df_filtrado['VL_LIQ_DSV_FAT'].sum(), 2)
    total_metadia = round(df_filtrado['VL_LIQ_DSV_PED'].sum(), 2)
    total_gapdia = round(df_filtrado['GAP_DIA'].sum(), 2)
    total_metanova = round(df_filtrado['META_NOVA'].sum(), 2)

    # Formatar valores como moeda (R$)
    total_meta_format = formatar_numero(total_meta)
    total_valorliquido_format = formatar_numero(total_valorliquido)
    total_metadia_format = formatar_numero(total_metadia)
    total_gapdia_format = formatar_numero(total_gapdia)
    total_metanova_format = formatar_numero(total_metanova)

    # Exibir os cards com as métricas
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("R$ META", total_meta_format)
        style_metric_cards(border_left_color="#3e4095")

    with col2:
        st.metric("R$ VALOR FATURADO", total_valorliquido_format)

    with col3:
        st.metric("R$ METADIA", total_metadia_format)

    with col4:
        st.metric("R$ GAP DIA", total_gapdia_format)

    with col5:
        st.metric("R$ META NOVA", total_metanova_format)

    # CSS para forçar largura total do DataFrame
    st.markdown(
        """
        <style>
        .custom-container {
            width: 100%; /* Força largura total */
            max-width: 1200px; /* Define limite máximo opcional */
            margin: 20px auto; /* Centraliza */
        }
        .custom-container table {
            width: 100%; /* Largura da tabela dentro do contêiner */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Exibir o DataFrame filtrado dentro do contêiner
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    st.dataframe(df_filtrado)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"Tamanho do DataFrame final: {df_filtrado.shape}")


if __name__ == "__main__":
    main()