import os

# Caminho do Oracle Instant Client
oracle_client_path = r"C:\oraclexe\app\oracle\product\11.2.0\server\bin"

# Verificar se o caminho existe
if os.path.exists(oracle_client_path):
    print(f"Caminho do Oracle Instant Client encontrado: {oracle_client_path}")
else:
    print(f"Caminho do Oracle Instant Client NÃO encontrado: {oracle_client_path}")
