FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    libaio1 \
    unzip \
    curl \
    && apt-get clean

# Configurar diretório de trabalho
WORKDIR /workspace

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão
CMD ["python"]
