# Use a imagem oficial do Python
FROM python:latest

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências necessárias para o Oracle Instant Client
RUN apt-get update && \
    apt-get install -y libaio1 libaio-dev unzip

# Copiar o Oracle Instant Client do host para o contêiner
COPY C:/oracle/instantclient_21_16 /opt/oracle/instantclient_21_16

# Configurar variáveis de ambiente
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_16
ENV PATH=/opt/oracle/instantclient_21_16:$PATH

# Verificar se o Oracle Instant Client foi configurado corretamente
RUN ls -l /opt/oracle/instantclient_21_16 && \
    echo $LD_LIBRARY_PATH

# Copiar o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/

# Instalar as dependências do Python
RUN pip install -r /app/requirements.txt

# Copiar o código do aplicativo para o contêiner
COPY . /app/

# Expor a porta do Streamlit
EXPOSE 8501

# Definir o comando de inicialização para o Streamlit
ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]





#1 comando: docker build -t streamlit-dataeditor .
#2  docker run -p 8501:8501 streamlit-dataeditor