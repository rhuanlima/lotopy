import pandas as pd


def calculate_number_frequency(df):
    """
    Calcula a frequência de cada número (1-25) em todos os concursos.
    
    Args:
        df: DataFrame com as colunas Bola1, Bola2, ..., Bola15
        
    Returns:
        DataFrame com colunas: numero, frequencia
    """
    lst_campos = [
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]
    
    # Dicionário para contar frequência de cada número
    frequencias = {i: 0 for i in range(1, 26)}
    
    # Contar frequência de cada número
    for index, row in df.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                numero = int(numero)
                if 1 <= numero <= 25:
                    frequencias[numero] += 1
    
    # Criar DataFrame com resultados
    df_freq = pd.DataFrame([
        {"numero": num, "frequencia": freq}
        for num, freq in sorted(frequencias.items())
    ])
    
    return df_freq


def get_numbers_status_in_cycle(df):
    """
    Retorna o status de cada número (1-25) no ciclo atual.
    
    Args:
        df: DataFrame com a coluna 'ciclo' já calculada
        
    Returns:
        DataFrame com colunas: numero, frequencia, no_ciclo_atual
    """
    if "ciclo" not in df.columns:
        raise ValueError("DataFrame não possui a coluna 'ciclo'. Execute calculate_cycle() primeiro.")
    
    lst_campos = [
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]
    
    # Calcular frequência total
    df_freq = calculate_number_frequency(df)
    
    # Pegar o último ciclo
    ultimo_ciclo = df["ciclo"].max()
    
    # Filtrar apenas os concursos do último ciclo
    df_ultimo_ciclo = df[df["ciclo"] == ultimo_ciclo]
    
    # Coletar números sorteados no último ciclo
    numeros_no_ciclo = set()
    for index, row in df_ultimo_ciclo.iterrows():
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                numeros_no_ciclo.add(int(numero))
    
    # Adicionar coluna indicando se o número está no ciclo atual
    df_freq["no_ciclo_atual"] = df_freq["numero"].apply(
        lambda x: x in numeros_no_ciclo
    )
    
    return df_freq
