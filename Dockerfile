# Use a imagem base do Python
FROM python:3.11.4

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . .

# Exponha a porta onde a aplicação FastAPI será executada
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "ocr_server.py"]
