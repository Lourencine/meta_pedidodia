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
    # Conectar ao banco de dados usando variáveis de ambiente
    dsn_tns = cx_Oracle.makedsn(
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        service_name=os.getenv("DB_SERVICE_NAME")
    )
    conexao = cx_Oracle.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=dsn_tns
    )
    df = pd.read_sql(query, conexao)
    conexao.close()
    return df


def main():
    st.title("Tabela de Vendas 📊")

    # Consulta SQL otimizada com limite de registros
    query = """
    SELECT * FROM DBAUSER.VIEW_PBI_METAPEDIDODIA T1
    WHERE T1.CODSUPERVISOR <> 39
    """

    start_time = time.time()
    df = carregar_dados(query)
    st.write(f"Tempo para carregar dados: {time.time() - start_time:.2f} segundos")

    if df.empty:
        st.warning("Nenhum dado encontrado para os critérios informados.")
        return

    # O resto do código permanece inalterado...


    # Agrupando os dados
    df_agrupado = df.groupby(['DATA', 'CODSUPERVISOR', 'SUPERVISOR', 'CODUSUR', 'NOME'], as_index=False).agg({
        'VLVENDAPREV': 'sum',
        'VL_LIQ_DSV_FAT': 'sum',
        'VL_LIQ_DSV_PED': 'sum',
        'GAP_DIA': 'sum',
        'META_NOVA': 'sum'
    })

    # Inicializar DataFrame filtrado
    df_filtrado = df_agrupado.copy()

    # Adicionar a logo na barra lateral acima dos filtros
    with st.sidebar:
        st.image("E:/GitHub_Workspace/Projetos/Meta_PedidoDia/LOGO SOST NOVO.png",
                 use_container_width=True)
        filtro_data = st.date_input(
            "Filtrar por Data",
            value=None,  # Valor padrão
            min_value=df_agrupado['DATA'].min(
            ) if not df_agrupado.empty else None,
            max_value=df_agrupado['DATA'].max(
            ) if not df_agrupado.empty else None
        )
        filtro_supervisor = st.text_input("Filtrar por Supervisor:")
        filtro_nomerca = st.text_input("Filtrar por NomeRca:")

    # Aplicar os filtros
    if filtro_data:
        if isinstance(filtro_data, list) and len(filtro_data) == 2:
            # Filtro de intervalo de datas
            data_inicio, data_fim = pd.to_datetime(filtro_data)
            df_filtrado = df_filtrado[
                (df_filtrado['DATA'] >= data_inicio) & (
                    df_filtrado['DATA'] <= data_fim)
            ]
        else:
            # Filtro de uma única data
            filtro_data = pd.to_datetime(filtro_data)
            df_filtrado = df_filtrado[df_filtrado['DATA'] == filtro_data]

    if filtro_supervisor:
        df_filtrado = df_filtrado[df_filtrado['SUPERVISOR'].str.contains(
            filtro_supervisor, case=False, na=False)]

    if filtro_nomerca:
        df_filtrado = df_filtrado[df_filtrado['NOME'].str.contains(
            filtro_nomerca, case=False, na=False)]

    # Verificar se há dados após os filtros
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado após aplicar os filtros.")
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
