# Use Python 3.11 slim image como base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Cria o diretório de dados se não existir
RUN mkdir -p /app/data

# Expõe a porta 4201
EXPOSE 4201

# Define variável de ambiente para a porta
ENV PORT=4201

# Comando para rodar a aplicação com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:4201", "--workers", "2", "--timeout", "120", "flask_app:app"]
