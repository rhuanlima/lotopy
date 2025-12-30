# 🎰 Lotofácil - Sistema de Análise e Sugestões

Sistema completo de análise de dados da Lotofácil com interface web moderna e API REST para sugestões inteligentes de jogos.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estratégias de Sugestões](#estratégias-de-sugestões)
- [API REST](#api-rest)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido para análise estatística dos concursos da Lotofácil, oferecendo:
- Visualização dos últimos concursos
- Análise de ciclos (quando todos os 25 números foram sorteados)
- Configuração Pares-Ímpares-Primos (P-I-NP)
- **6 estratégias diferentes de sugestões de jogos** baseadas em análises estatísticas
- API REST para integração com outras aplicações

## ✨ Funcionalidades

### Interface Web

1. **Tabela de Concursos**
   - Visualização dos últimos 15 concursos
   - Números sorteados organizados em 2 linhas
   - Número do ciclo atual
   - Configuração P-I-NP de cada concurso

2. **Status dos Números**
   - Lista completa dos 25 números possíveis
   - Frequência total de cada número
   - Indicador visual se o número já saiu no ciclo atual

3. **Sugestões de Jogos**
   - 6 estratégias diferentes
   - Cada sugestão contém exatamente 15 números
   - Cards coloridos com descrição de cada estratégia

4. **Atualização de Dados**
   - Botão para buscar novos concursos sob demanda
   - Atualização automática dos dados

### API REST

- Endpoint `/api/suggestions` retorna sugestões em formato JSON
- Ideal para integração com bots, aplicativos mobile, etc.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.x, Flask
- **Análise de Dados:** Pandas
- **Frontend:** HTML5, CSS3 (design moderno com gradientes)
- **Dados:** Excel (XLSX) via openpyxl

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd lotopy
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python flask_app.py
```

5. Acesse no navegador:
```
http://localhost:5000
```

## 🌐 Deploy no Render

Este projeto está pronto para deploy no [Render](https://render.com). Siga os passos abaixo:

### Pré-requisitos
- Conta no GitHub
- Conta no Render (gratuita)
- Repositório Git com o código

### Passos para Deploy

1. **Faça push do código para o GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <url-do-seu-repositorio>
git push -u origin main
```

2. **Acesse o Render:**
   - Vá para [render.com](https://render.com)
   - Faça login ou crie uma conta

3. **Crie um novo Web Service:**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório `lotopy`

4. **Configure o serviço:**
   - **Name:** `lotofacil-app` (ou nome de sua escolha)
   - **Region:** Escolha a região mais próxima
   - **Branch:** `main`
   - **Root Directory:** (deixe em branco)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** (deixe em branco - usa o Procfile automaticamente)
   - **Plan:** Free

5. **Variáveis de Ambiente (opcional):**
   - Não são necessárias para este projeto

6. **Deploy:**
   - Clique em "Create Web Service"
   - Aguarde o build e deploy (leva alguns minutos)
   - Sua aplicação estará disponível em `https://seu-app.onrender.com`

### Arquivos de Configuração

O projeto já inclui os arquivos necessários para deploy:

- **`Procfile`**: Define o comando para iniciar a aplicação
  ```
  web: gunicorn flask_app:app
  ```

- **`requirements.txt`**: Lista todas as dependências com versões específicas
  ```
  Flask==3.1.2
  pandas==2.2.3
  requests==2.32.3
  openpyxl==3.1.5
  gunicorn==23.0.0
  Werkzeug==3.1.4
  ```

- **`flask_app.py`**: Configurado para usar a porta do ambiente
  ```python
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  ```

### Notas Importantes

- O plano gratuito do Render pode ter cold starts (demora inicial ao acessar)
- A aplicação baixa os dados da Caixa automaticamente na primeira execução
- Para atualizar os dados, use o botão "🔄 Atualizar Banco de Dados" na interface

## 🚀 Como Usar

### Interface Web

1. **Visualizar Concursos:** Acesse a página principal para ver os últimos 15 concursos
2. **Atualizar Dados:** Clique no botão "🔄 Atualizar Banco de Dados" para buscar novos concursos
3. **Ver Sugestões:** Role até a seção "🎲 Sugestões de Jogos" para ver as 6 estratégias
4. **Escolher Estratégia:** Selecione a estratégia que mais se adequa ao seu estilo de jogo

### API REST

Faça uma requisição GET para obter sugestões:

```bash
curl http://localhost:5000/api/suggestions
```

Resposta JSON:
```json
{
  "success": true,
  "total_concursos": 3574,
  "ciclo_atual": 759,
  "sugestoes": [
    {
      "estrategia": "🔥 Números Mais Frequentes",
      "descricao": "Baseado nos números que mais saíram historicamente",
      "numeros": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    },
    ...
  ]
}
```

## 🧠 Estratégias de Sugestões

O sistema implementa 6 estratégias diferentes para gerar sugestões de jogos. Cada uma utiliza análises estatísticas específicas:

### 1. 🔥 Números Mais Frequentes

**Como funciona:**
- Analisa **todos os concursos** da base de dados histórica
- Conta quantas vezes cada número (1-25) foi sorteado
- Seleciona os 15 números com maior frequência absoluta

**Quando usar:**
- Para jogadores conservadores que confiam em padrões históricos
- Baseado na teoria de que números frequentes tendem a continuar saindo

**Exemplo de lógica:**
```python
# Conta frequência de cada número em todos os concursos
frequencias = {1: 2450, 2: 2480, 3: 2430, ...}
# Retorna os 15 mais frequentes
numeros = [2, 11, 13, 4, 20, ...]
```

---

### 2. 🎯 Faltantes no Ciclo

**Como funciona:**
- Identifica o **ciclo atual** (conjunto de concursos até todos os 25 números serem sorteados)
- Lista os números que **ainda não saíram** no ciclo atual
- Prioriza esses números faltantes
- Se houver menos de 15 faltantes, completa com os mais frequentes historicamente

**Quando usar:**
- Para jogadores que acreditam na teoria dos ciclos
- Baseado na premissa de que todos os números devem sair em um ciclo

**Exemplo de lógica:**
```python
# Ciclo atual: 759
# Números já sorteados no ciclo: {1, 2, 3, 5, 7, 8, 10, 12, ...}
# Faltantes: {4, 6, 9, 11, 14, 15, 16, 19, 21, 22, 23, 24, 25}
# Retorna faltantes + complementa com frequentes se necessário
```

---

### 3. ⚖️ Estratégia Balanceada

**Como funciona:**
- Analisa a **proporção ideal** de Pares-Ímpares-Primos (P-I-NP)
- Baseado nas configurações mais frequentes historicamente
- Seleciona 7 pares e 8 ímpares (proporção comum)
- Prioriza números mais frequentes dentro de cada categoria

**Quando usar:**
- Para jogadores que buscam equilíbrio estatístico
- Baseado em padrões de distribuição observados

**Categorias:**
- **Pares:** 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24
- **Ímpares:** 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25
- **Primos:** 2, 3, 5, 7, 11, 13, 17, 19, 23

---

### 4. 🔥 Números Quentes

**Como funciona:**
- Analisa apenas os **últimos 30 concursos**
- Identifica números com alta frequência recente
- Captura **tendências de curto prazo**
- Retorna os 15 números mais "quentes" do momento

**Quando usar:**
- Para jogadores que acreditam em tendências recentes
- Quando há padrões de curto prazo observáveis

**Exemplo de lógica:**
```python
# Últimos 30 concursos
df_recentes = df.tail(30)
# Conta frequência apenas nesses concursos
frequencias_recentes = {13: 18, 11: 17, 20: 16, ...}
# Retorna os 15 mais quentes
```

---

### 5. 🎲 Mix Inteligente

**Como funciona:**
- **Combina duas estratégias:**
  - 8 números faltantes no ciclo atual
  - 7 números mais frequentes historicamente
- Cria um equilíbrio entre ciclo e frequência
- Estratégia híbrida balanceada

**Quando usar:**
- Para jogadores que querem combinar teoria dos ciclos com frequência histórica
- Abordagem intermediária entre conservador e agressivo

**Exemplo de lógica:**
```python
faltantes = [4, 6, 9, 11, 14, 15, 16, 19]  # 8 números
frequentes = [2, 13, 20, 1, 3, 5, 7]        # 7 números
jogo = sorted(faltantes + frequentes)        # 15 números
```

---

### 6. 🧠 Análise Combinada

**Como funciona:**
- **Sistema de pontuação multi-fatorial**
- Cada número recebe pontos baseado em 3 critérios:
  - **3 pontos:** Se está entre os 10 mais frequentes historicamente
  - **2 pontos:** Se está entre os 10 mais quentes (últimos 40 concursos)
  - **1 ponto:** Se está faltando no ciclo atual
- Seleciona os 15 números com maior pontuação total

**Quando usar:**
- Para jogadores que querem uma análise completa
- Algoritmo mais sofisticado que pondera múltiplos fatores

**Exemplo de lógica:**
```python
pontos = {
    1: 3 + 2 + 0 = 5,  # Frequente + Quente
    4: 0 + 0 + 1 = 1,  # Apenas faltante
    13: 3 + 2 + 1 = 6, # Todos os critérios
    ...
}
# Ordena por pontuação e pega top 15
```

---

## 📊 Conceitos Importantes

### O que é um Ciclo?

Um **ciclo** é o conjunto de concursos consecutivos necessários para que todos os 25 números possíveis (1 a 25) sejam sorteados pelo menos uma vez.

**Exemplo:**
- Concurso 3560: saem números {1, 2, 3, 5, 7, ...}
- Concurso 3561: saem números {4, 6, 8, 9, ...}
- ...
- Concurso 3570: sai o último número faltante (ex: 24)
- **Ciclo 758 completo!** Inicia-se o Ciclo 759

### Configuração P-I-NP

Indica a quantidade de:
- **P (Pares):** Números divisíveis por 2
- **I (Ímpares):** Números não divisíveis por 2
- **NP (Números Primos):** 2, 3, 5, 7, 11, 13, 17, 19, 23

**Exemplo:** "7P-8I-4NP" significa:
- 7 números pares
- 8 números ímpares
- 4 números primos

## 📁 Estrutura do Projeto

```
lotopy/
├── source/
│   ├── __init__.py
│   ├── db_update.py           # Atualização do banco de dados
│   ├── adjust_table.py         # Ajuste e limpeza dos dados
│   ├── cycle_calculator.py     # Cálculo de ciclos
│   ├── pip_config.py           # Configuração P-I-NP
│   ├── number_frequency.py     # Análise de frequência
│   ├── game_suggestions.py     # Geração de sugestões (6 estratégias)
│   └── analisys.py            # Análises diversas
├── templates/
│   └── index.html             # Template HTML principal
├── static/
│   └── style.css              # Estilos CSS
├── data/
│   └── D_lotfac.xlsx          # Base de dados dos concursos
├── flask_app.py               # Aplicação Flask principal
├── app.py                     # Script de análise standalone
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🔧 Módulos Principais

### `db_update.py`

Módulo responsável por baixar e atualizar a base de dados da Lotofácil diretamente da API da Caixa.

**Funções:**
- `download_url(url, save_path, chunk_size=128)`: Faz download de arquivo via streaming
- `update_db(save_path)`: Atualiza o banco de dados com os dados mais recentes

**Código:**
```python
import requests

def download_url(url, save_path, chunk_size=128):
    """Baixa arquivo via streaming para economizar memória."""
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def update_db(save_path):
    """
    Atualiza o banco de dados baixando o arquivo Excel da Caixa.
    
    Args:
        save_path: Caminho onde o arquivo será salvo (ex: "./data/D_lotfac.xlsx")
    """
    url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=Lotofácil"
    download_url(url, save_path)
```

**Uso:**
```python
import source.db_update as dbu

# Atualizar banco de dados
dbu.update_db(save_path="./data/D_lotfac.xlsx")
```

---

### `adjust_table.py`

Módulo para carregar e ajustar a tabela de dados da Lotofácil, selecionando apenas as colunas relevantes e garantindo tipos de dados corretos.

**Funções:**
- `adjust_table()`: Carrega e ajusta o DataFrame com os dados dos concursos

**Código:**
```python
import pandas as pd

def adjust_table():
    """
    Carrega e ajusta a tabela do banco de dados.
    
    - Seleciona apenas colunas relevantes (Concurso, Data, Bolas)
    - Remove duplicatas
    - Converte colunas de bolas para tipo Int64
    
    Returns:
        DataFrame ajustado e pronto para análise
    """
    df = pd.read_excel("data/D_lotfac.xlsx")
    
    # Selecionar apenas colunas relevantes
    df = df[[
        "Concurso",
        "Data Sorteio",
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]]
    
    # Remover duplicatas
    df = df.drop_duplicates()
    
    # Converter colunas de bolas para Int64 (suporta NaN)
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    df[lst_campos] = df[lst_campos].astype("Int64")
    
    return df
```

**Uso:**
```python
import source.adjust_table as at

# Carregar dados ajustados
df = at.adjust_table()
print(f"Total de concursos: {len(df)}")
```

---

### `analisys.py`

Módulo com análises estatísticas diversas, incluindo análise de frequência de combinações Pares-Ímpares-Primos.

**Funções:**
- `fr_pip(df)`: Analisa frequência de configurações P-I-NP

**Código (simplificado):**
```python
import pandas as pd
import collections

def fr_pip(df):
    """
    Analisa a frequência de combinações Pares-Ímpares-Primos.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        DataFrame com combinações e suas frequências
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Definir categorias
    nr_pares = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    nr_impares = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    comb = []
    
    # Analisar cada concurso
    for index, row in df.iterrows():
        v_pares = 0
        v_impares = 0
        v_primos = 0
        
        # Contar pares, ímpares e primos
        for campo in lst_campos:
            if row[campo] in nr_pares:
                v_pares += 1
            if row[campo] in nr_impares:
                v_impares += 1
            if row[campo] in nr_primos:
                v_primos += 1
        
        # Criar string de combinação (ex: "7p-8i-4np")
        comb.append(f"{v_pares}p-{v_impares}i-{v_primos}np")
    
    # Contar frequência de cada combinação
    counter = collections.Counter(comb)
    resultado = pd.DataFrame(counter.items(), columns=["Combinacao", "Frequencia"])
    resultado["p_freq"] = resultado["Frequencia"] / resultado["Frequencia"].sum() * 100
    
    return resultado.sort_values(by="p_freq", ascending=False)
```

**Uso:**
```python
import source.analisys as an

# Analisar configurações P-I-NP
df = adjust_table()
analise = an.fr_pip(df)
print("Configurações mais frequentes:")
print(analise.head(10))
```

**Exemplo de saída:**
```
   Combinacao  Frequencia  p_freq
0   7p-8i-4np         245    6.85
1   8p-7i-5np         230    6.43
2   7p-8i-5np         220    6.15
...
```

---

### `game_suggestions.py`

Módulo responsável por gerar as sugestões de jogos. Funções principais:

- `get_most_frequent_numbers(df, n=15)`: Números mais frequentes
- `get_missing_in_cycle(df)`: Números faltantes no ciclo
- `get_hot_numbers(df, last_n=50, top=15)`: Números quentes
- `generate_balanced_game(df)`: Jogo balanceado P-I-NP
- `generate_mixed_strategy(df)`: Mix de estratégias
- `generate_cycle_priority(df)`: Prioridade para faltantes
- `generate_recent_hot(df)`: Baseado em tendências
- `generate_combined_analysis(df)`: Análise multi-fatorial
- `generate_suggestions(df, num_games=6)`: Função principal

### `cycle_calculator.py`

Calcula os ciclos dos concursos:

- `calculate_cycle(df)`: Adiciona coluna de ciclo ao DataFrame
- `get_cycle_statistics(df)`: Estatísticas dos ciclos
- `get_numbers_in_current_cycle(df)`: Números no ciclo atual
- `get_missing_numbers_in_current_cycle(df)`: Números faltantes

### `pip_config.py`

Calcula configuração Pares-Ímpares-Primos para cada concurso:

- `calculate_pip_config(df)`: Adiciona coluna 'config_pip' ao DataFrame

**Exemplo:**
```python
import source.pip_config as pip

df = adjust_table()
df = pip.calculate_pip_config(df)
print(df[['Concurso', 'config_pip']].tail())
```

### `number_frequency.py`

Análise de frequência de números:

- `calculate_number_frequency(df)`: Conta ocorrências de cada número
- `get_numbers_status_in_cycle(df)`: Status de cada número no ciclo atual

## 🌐 API REST

### Endpoint: `/api/suggestions`

**Método:** GET

**Descrição:** Retorna sugestões de jogos em formato JSON

**Exemplo de Requisição:**
```bash
curl http://localhost:5000/api/suggestions
```

**Exemplo de Resposta:**
```json
{
  "success": true,
  "total_concursos": 3574,
  "ciclo_atual": 759,
  "sugestoes": [
    {
      "estrategia": "🔥 Números Mais Frequentes",
      "descricao": "Baseado nos números que mais saíram historicamente",
      "numeros": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    },
    {
      "estrategia": "🎯 Faltantes no Ciclo",
      "descricao": "Prioriza números que ainda não saíram no ciclo atual",
      "numeros": [4, 6, 9, 11, 14, 15, 16, 19, 21, 22, 23, 24, 25, 1, 2]
    },
    {
      "estrategia": "⚖️ Estratégia Balanceada",
      "descricao": "Mix equilibrado de pares, ímpares e primos",
      "numeros": [2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    },
    {
      "estrategia": "🔥 Números Quentes",
      "descricao": "Números mais frequentes nos últimos 30 concursos",
      "numeros": [13, 11, 20, 2, 3, 5, 7, 8, 10, 12, 14, 16, 18, 22, 24]
    },
    {
      "estrategia": "🎲 Mix Inteligente",
      "descricao": "Combina números frequentes com faltantes no ciclo",
      "numeros": [4, 6, 9, 11, 14, 15, 16, 19, 1, 2, 3, 5, 7, 8, 10]
    },
    {
      "estrategia": "🧠 Análise Combinada",
      "descricao": "Algoritmo que pondera múltiplos fatores estatísticos",
      "numeros": [13, 11, 2, 20, 3, 5, 7, 8, 10, 12, 14, 16, 18, 22, 24]
    }
  ]
}
```

**Uso em Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/suggestions')
data = response.json()

for sugestao in data['sugestoes']:
    print(f"{sugestao['estrategia']}: {sugestao['numeros']}")
```

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através do repositório.

---

**README criado usando IA**
