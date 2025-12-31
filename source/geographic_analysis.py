"""
Módulo para análise geográfica dos números da Lotofácil.

A cartela da Lotofácil é organizada em uma grade 5x5:
    1   2   3   4   5
    6   7   8   9  10
   11  12  13  14  15
   16  17  18  19  20
   21  22  23  24  25

Este módulo analisa a distribuição dos números em:
- MOLDURA: bordas da cartela (primeira/última linha e colunas laterais)
- MIOLO: centro da cartela
- LINHAS: distribuição por cada uma das 5 linhas
"""


def get_number_position(numero):
    """
    Retorna a posição (linha, coluna) de um número na cartela.
    
    Args:
        numero: Número de 1 a 25
        
    Returns:
        tuple: (linha, coluna) onde linha e coluna vão de 0 a 4
    """
    if numero < 1 or numero > 25:
        return None
    
    numero_idx = numero - 1
    linha = numero_idx // 5
    coluna = numero_idx % 5
    
    return (linha, coluna)


def is_moldura(numero):
    """
    Verifica se um número está na moldura da cartela.
    
    MOLDURA inclui:
    - Primeira linha: 1, 2, 3, 4, 5
    - Última linha: 21, 22, 23, 24, 25
    - Colunas laterais: 6, 10, 11, 15, 16, 20
    
    Args:
        numero: Número de 1 a 25
        
    Returns:
        bool: True se está na moldura, False caso contrário
    """
    moldura = {1, 2, 3, 4, 5, 21, 22, 23, 24, 25, 6, 10, 11, 15, 16, 20}
    return numero in moldura


def is_miolo(numero):
    """
    Verifica se um número está no miolo da cartela.
    
    MIOLO inclui: 7, 8, 9, 12, 13, 14, 17, 18, 19
    
    Args:
        numero: Número de 1 a 25
        
    Returns:
        bool: True se está no miolo, False caso contrário
    """
    miolo = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    return numero in miolo


def get_line_number(numero):
    """
    Retorna o número da linha (1-5) onde o número está localizado.
    
    Args:
        numero: Número de 1 a 25
        
    Returns:
        int: Número da linha (1 a 5)
    """
    if numero < 1 or numero > 25:
        return None
    
    return ((numero - 1) // 5) + 1


def analyze_geographic_distribution(numeros):
    """
    Analisa a distribuição geográfica de um conjunto de números.
    
    Args:
        numeros: Lista ou conjunto de números sorteados
        
    Returns:
        dict: Dicionário com as seguintes chaves:
            - moldura: quantidade de números na moldura
            - miolo: quantidade de números no miolo
            - linha1: quantidade de números na linha 1 (1-5)
            - linha2: quantidade de números na linha 2 (6-10)
            - linha3: quantidade de números na linha 3 (11-15)
            - linha4: quantidade de números na linha 4 (16-20)
            - linha5: quantidade de números na linha 5 (21-25)
            - distribuicao_linhas: string no formato "L1-L2-L3-L4-L5"
    """
    # Definir conjuntos
    moldura = {1, 2, 3, 4, 5, 21, 22, 23, 24, 25, 6, 10, 11, 15, 16, 20}
    miolo = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    
    # Linhas da cartela
    linha1 = {1, 2, 3, 4, 5}
    linha2 = {6, 7, 8, 9, 10}
    linha3 = {11, 12, 13, 14, 15}
    linha4 = {16, 17, 18, 19, 20}
    linha5 = {21, 22, 23, 24, 25}
    
    # Contar
    count_moldura = sum(1 for n in numeros if n in moldura)
    count_miolo = sum(1 for n in numeros if n in miolo)
    
    count_linha1 = sum(1 for n in numeros if n in linha1)
    count_linha2 = sum(1 for n in numeros if n in linha2)
    count_linha3 = sum(1 for n in numeros if n in linha3)
    count_linha4 = sum(1 for n in numeros if n in linha4)
    count_linha5 = sum(1 for n in numeros if n in linha5)
    
    return {
        'moldura': count_moldura,
        'miolo': count_miolo,
        'linha1': count_linha1,
        'linha2': count_linha2,
        'linha3': count_linha3,
        'linha4': count_linha4,
        'linha5': count_linha5,
        'distribuicao_linhas': f"{count_linha1}-{count_linha2}-{count_linha3}-{count_linha4}-{count_linha5}"
    }


def get_numbers_by_position(numeros):
    """
    Organiza os números por suas posições na cartela.
    
    Args:
        numeros: Lista de números sorteados
        
    Returns:
        dict: Dicionário com listas de números organizados por:
            - moldura: números na moldura
            - miolo: números no miolo
            - linha1, linha2, linha3, linha4, linha5: números em cada linha
    """
    moldura_nums = []
    miolo_nums = []
    linha1_nums = []
    linha2_nums = []
    linha3_nums = []
    linha4_nums = []
    linha5_nums = []
    
    for num in numeros:
        if is_moldura(num):
            moldura_nums.append(num)
        if is_miolo(num):
            miolo_nums.append(num)
        
        linha = get_line_number(num)
        if linha == 1:
            linha1_nums.append(num)
        elif linha == 2:
            linha2_nums.append(num)
        elif linha == 3:
            linha3_nums.append(num)
        elif linha == 4:
            linha4_nums.append(num)
        elif linha == 5:
            linha5_nums.append(num)
    
    return {
        'moldura': sorted(moldura_nums),
        'miolo': sorted(miolo_nums),
        'linha1': sorted(linha1_nums),
        'linha2': sorted(linha2_nums),
        'linha3': sorted(linha3_nums),
        'linha4': sorted(linha4_nums),
        'linha5': sorted(linha5_nums)
    }
