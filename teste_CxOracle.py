import cx_Oracle

try:
    oracle_client_path = r"C:\oraclexe\app\oracle\product\11.2.0\server\bin"
    cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

    dsn_tns = cx_Oracle.makedsn("192.168.254.200", "1521", service_name="DBPROD")
    connection = cx_Oracle.connect(user="CONSULTAPOWERBI", password="S0STQUERYPB", dsn=dsn_tns)

    print("Conexão com o banco de dados bem-sucedida!")
    connection.close()
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print(f"Erro ao conectar ao banco de dados: {error.message}")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
