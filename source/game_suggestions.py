import pandas as pd
import random
from collections import Counter


def get_most_frequent_numbers(df, n=15):
    """
    Retorna os N números mais frequentes em todos os concursos.
    
    Args:
        df: DataFrame com as colunas Bola1, Bola2, ..., Bola15
        n: Quantidade de números a retornar
        
    Returns:
        list: Lista com os N números mais frequentes
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Contar frequência de cada número
    frequencias = Counter()
    for index, row in df.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                frequencias[int(numero)] += 1
    
    # Retornar os N mais frequentes
    mais_frequentes = [num for num, freq in frequencias.most_common(n)]
    return sorted(mais_frequentes)


def get_missing_in_cycle(df):
    """
    Retorna os números que ainda não saíram no ciclo atual.
    
    Args:
        df: DataFrame com a coluna 'ciclo' já calculada
        
    Returns:
        list: Lista de números faltantes no ciclo atual
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Pegar o último ciclo
    ultimo_ciclo = df["ciclo"].max()
    df_ultimo_ciclo = df[df["ciclo"] == ultimo_ciclo]
    
    # Coletar números sorteados no último ciclo
    numeros_no_ciclo = set()
    for index, row in df_ultimo_ciclo.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                numeros_no_ciclo.add(int(numero))
    
    # Números faltantes
    todos_numeros = set(range(1, 26))
    faltantes = sorted(list(todos_numeros - numeros_no_ciclo))
    
    return faltantes


def get_hot_numbers(df, last_n=50, top=15):
    """
    Retorna os números mais frequentes nos últimos N concursos.
    
    Args:
        df: DataFrame com os concursos
        last_n: Quantidade de concursos recentes a analisar
        top: Quantidade de números a retornar
        
    Returns:
        list: Lista com os números mais "quentes"
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Pegar últimos N concursos
    df_recentes = df.tail(last_n)
    
    # Contar frequência
    frequencias = Counter()
    for index, row in df_recentes.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                frequencias[int(numero)] += 1
    
    # Retornar os mais frequentes
    quentes = [num for num, freq in frequencias.most_common(top)]
    return sorted(quentes)


def generate_balanced_game(df):
    """
    Gera um jogo balanceado com proporção ideal de Pares-Ímpares-Primos.
    Baseado nas configurações mais frequentes.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números balanceados
    """
    # Definir conjuntos
    pares = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    impares = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    # Proporção ideal: 7-8 pares, 7-8 ímpares, 4-5 primos
    num_pares = 7
    num_impares = 8
    
    # Pegar números mais frequentes de cada categoria
    freq_pares = get_most_frequent_numbers(df, 25)
    freq_impares = get_most_frequent_numbers(df, 25)
    
    pares_freq = [n for n in freq_pares if n in pares][:num_pares]
    impares_freq = [n for n in freq_impares if n in impares][:num_impares]
    
    jogo = sorted(pares_freq + impares_freq)
    return jogo


def generate_mixed_strategy(df):
    """
    Gera um jogo misturando números frequentes e faltantes no ciclo.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    frequentes = get_most_frequent_numbers(df, 25)
    faltantes = get_missing_in_cycle(df)
    
    # Se há faltantes suficientes, usar 8 faltantes + 7 frequentes
    if len(faltantes) >= 8:
        jogo = faltantes[:8] + [n for n in frequentes if n not in faltantes][:7]
    else:
        # Caso contrário, completar com frequentes
        jogo = faltantes + [n for n in frequentes if n not in faltantes][:15-len(faltantes)]
    
    return sorted(jogo[:15])


def generate_cycle_priority(df):
    """
    Gera um jogo priorizando números faltantes no ciclo.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    faltantes = get_missing_in_cycle(df)
    frequentes = get_most_frequent_numbers(df, 25)
    
    # Priorizar faltantes, completar com frequentes
    if len(faltantes) >= 15:
        jogo = faltantes[:15]
    else:
        jogo = faltantes + [n for n in frequentes if n not in faltantes][:15-len(faltantes)]
    
    return sorted(jogo)


def generate_recent_hot(df):
    """
    Gera um jogo com números mais frequentes recentemente.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    return get_hot_numbers(df, last_n=30, top=15)


def generate_combined_analysis(df):
    """
    Gera um jogo combinando múltiplos fatores:
    - Frequência histórica
    - Números quentes recentes
    - Status no ciclo
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    # Pegar diferentes análises
    frequentes = get_most_frequent_numbers(df, 20)
    quentes = get_hot_numbers(df, last_n=40, top=20)
    faltantes = get_missing_in_cycle(df)
    
    # Criar sistema de pontuação
    pontos = {}
    for num in range(1, 26):
        pontos[num] = 0
        if num in frequentes[:10]:
            pontos[num] += 3
        if num in quentes[:10]:
            pontos[num] += 2
        if num in faltantes:
            pontos[num] += 1
    
    # Ordenar por pontuação e pegar top 15
    numeros_ordenados = sorted(pontos.items(), key=lambda x: x[1], reverse=True)
    jogo = [num for num, pts in numeros_ordenados[:15]]
    
    return sorted(jogo)


def generate_suggestions(df, num_games=6):
    """
    Gera sugestões de jogos com diferentes estratégias.
    
    Args:
        df: DataFrame com os concursos e coluna 'ciclo'
        num_games: Número de sugestões a gerar
        
    Returns:
        list: Lista de dicionários com 'estrategia', 'descricao' e 'numeros'
    """
    sugestoes = [
        {
            'estrategia': '🔥 Números Mais Frequentes',
            'descricao': 'Baseado nos números que mais saíram historicamente',
            'numeros': get_most_frequent_numbers(df, 15)
        },
        {
            'estrategia': '🎯 Faltantes no Ciclo',
            'descricao': 'Prioriza números que ainda não saíram no ciclo atual',
            'numeros': generate_cycle_priority(df)
        },
        {
            'estrategia': '⚖️ Estratégia Balanceada',
            'descricao': 'Mix equilibrado de pares, ímpares e primos',
            'numeros': generate_balanced_game(df)
        },
        {
            'estrategia': '🔥 Números Quentes',
            'descricao': 'Números mais frequentes nos últimos 30 concursos',
            'numeros': generate_recent_hot(df)
        },
        {
            'estrategia': '🎲 Mix Inteligente',
            'descricao': 'Combina números frequentes com faltantes no ciclo',
            'numeros': generate_mixed_strategy(df)
        },
        {
            'estrategia': '🧠 Análise Combinada',
            'descricao': 'Algoritmo que pondera múltiplos fatores estatísticos',
            'numeros': generate_combined_analysis(df)
        }
    ]
    
    return sugestoes[:num_games]
