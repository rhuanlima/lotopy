# Makefile para gerenciamento do ambiente Lotofácil

# Variáveis
VENV_NAME := .venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

# Cores para output
GREEN := \033[0;32m
NC := \033[0m # No Color

.PHONY: all help setup install run clean

all: help

help:
	@echo "Comandos disponíveis:"
	@echo "  $(GREEN)make setup$(NC)   - Cria o ambiente virtual (.venv)"
	@echo "  $(GREEN)make install$(NC) - Instala as dependências do requirements.txt"
	@echo "  $(GREEN)make run$(NC)     - Executa a aplicação Flask"
	@echo "  $(GREEN)make clean$(NC)   - Remove o ambiente virtual e arquivos de cache"

setup: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate:
	@echo "$(GREEN)Criando ambiente virtual...$(NC)"
	python3 -m venv $(VENV_NAME)
	@echo "$(GREEN)Ambiente criado. Para ativar manualmente use: source $(VENV_NAME)/bin/activate$(NC)"

install: setup
	@echo "$(GREEN)Instalando dependências...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependências instaladas!$(NC)"

run: install
	@echo "$(GREEN)Iniciando aplicação em modo DEV (Porta 5001)...$(NC)"
	FLASK_ENV=development PORT=5001 $(PYTHON) flask_app.py

clean:
	@echo "$(GREEN)Limpando ambiente...$(NC)"
	rm -rf $(VENV_NAME)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "$(GREEN)Limpeza concluída!$(NC)"
