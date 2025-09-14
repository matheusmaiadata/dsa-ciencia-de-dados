# Projeto 3 - Limpeza e Preparação de Dados Para Modelos de Machine Learning com SageMaker, Docker e Python

# Usar uma imagem base do Python
FROM python:3.11-slim

# Atualizar o sistema e instalar dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws/

# Configurar diretório de trabalho
WORKDIR /scripts

# Copiar o arquivo de requisitos e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Definir o comando padrão ao iniciar o container
CMD ["bash"]
