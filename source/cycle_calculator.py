import pandas as pd


def calculate_cycle(df):
    """
    Calcula a coluna 'ciclo' no DataFrame analisando os concursos e contabilizando
    sempre que todos os 25 números foram sorteados.
    
    Args:
        df: DataFrame com as colunas Concurso, Bola1, Bola2, ..., Bola15
        
    Returns:
        DataFrame com a coluna 'ciclo' adicionada
    """
    lst_campos = [
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]
    
    # Criar uma cópia do DataFrame para não modificar o original
    df_result = df.copy()
    
    # Inicializar variáveis de controle
    numeros_sorteados = set()  # Conjunto de números já sorteados no ciclo atual
    ciclo_atual = 1
    ciclos = []  # Lista para armazenar o ciclo de cada concurso
    
    # Iterar sobre cada linha do DataFrame
    for index, row in df_result.iterrows():
        # Adicionar o ciclo atual à lista
        ciclos.append(ciclo_atual)
        
        # Coletar todos os números sorteados neste concurso
        numeros_concurso = set()
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):  # Verificar se o número não é NaN
                numeros_concurso.add(int(numero))
        
        # Adicionar os números do concurso ao conjunto de números sorteados
        numeros_sorteados.update(numeros_concurso)
        
        # Verificar se todos os 25 números foram sorteados
        if len(numeros_sorteados) == 25:
            # Todos os números foram sorteados, iniciar novo ciclo
            ciclo_atual += 1
            numeros_sorteados = set()  # Resetar o conjunto
    
    # Adicionar a coluna ciclo ao DataFrame
    df_result["ciclo"] = ciclos
    
    return df_result


def get_cycle_statistics(df):
    """
    Retorna estatísticas sobre os ciclos calculados.
    
    Args:
        df: DataFrame com a coluna 'ciclo' já calculada
        
    Returns:
        DataFrame com estatísticas dos ciclos
    """
    if "ciclo" not in df.columns:
        raise ValueError("DataFrame não possui a coluna 'ciclo'. Execute calculate_cycle() primeiro.")
    
    # Agrupar por ciclo e contar quantos concursos em cada ciclo
    cycle_stats = df.groupby("ciclo").agg({
        "Concurso": ["count", "min", "max"]
    }).reset_index()
    
    cycle_stats.columns = ["Ciclo", "Num_Concursos", "Concurso_Inicial", "Concurso_Final"]
    
    return cycle_stats


def get_numbers_in_current_cycle(df):
    """
    Retorna os números que já foram sorteados no ciclo atual (último ciclo incompleto).
    
    Args:
        df: DataFrame com a coluna 'ciclo' já calculada
        
    Returns:
        set: Conjunto de números já sorteados no ciclo atual
    """
    if "ciclo" not in df.columns:
        raise ValueError("DataFrame não possui a coluna 'ciclo'. Execute calculate_cycle() primeiro.")
    
    lst_campos = [
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]
    
    # Pegar o último ciclo
    ultimo_ciclo = df["ciclo"].max()
    
    # Filtrar apenas os concursos do último ciclo
    df_ultimo_ciclo = df[df["ciclo"] == ultimo_ciclo]
    
    # Coletar todos os números sorteados no último ciclo
    numeros_sorteados = set()
    for index, row in df_ultimo_ciclo.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                numeros_sorteados.add(int(numero))
    
    return numeros_sorteados


def get_missing_numbers_in_current_cycle(df):
    """
    Retorna os números que ainda NÃO foram sorteados no ciclo atual.
    
    Args:
        df: DataFrame com a coluna 'ciclo' já calculada
        
    Returns:
        set: Conjunto de números que faltam ser sorteados no ciclo atual
    """
    numeros_sorteados = get_numbers_in_current_cycle(df)
    todos_numeros = set(range(1, 26))  # Números de 1 a 25
    numeros_faltantes = todos_numeros - numeros_sorteados
    
    return numeros_faltantes
