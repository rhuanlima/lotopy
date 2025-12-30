import pandas as pd


def calculate_pip_config(df):
    """
    Calcula a configuração de Pares-Ímpares-Primos para cada concurso.
    
    Args:
        df: DataFrame com as colunas Bola1, Bola2, ..., Bola15
        
    Returns:
        DataFrame com a coluna 'config_pip' adicionada (formato: "XP-YI-ZNP")
    """
    lst_campos = [
        "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
        "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
    ]
    
    # Definir conjuntos de números
    nr_pares = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24}
    nr_impares = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25}
    nr_primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    
    # Criar uma cópia do DataFrame
    df_result = df.copy()
    
    # Lista para armazenar as configurações
    configs = []
    
    # Iterar sobre cada linha do DataFrame
    for index, row in df_result.iterrows():
        v_pares = 0
        v_impares = 0
        v_primos = 0
        
        # Contar pares, ímpares e primos
        for campo in lst_campos:
            numero = row[campo]
            if pd.notna(numero):
                numero = int(numero)
                if numero in nr_pares:
                    v_pares += 1
                if numero in nr_impares:
                    v_impares += 1
                if numero in nr_primos:
                    v_primos += 1
        
        # Criar string de configuração
        config = f"{v_pares}P-{v_impares}I-{v_primos}NP"
        configs.append(config)
    
    # Adicionar coluna ao DataFrame
    df_result["config_pip"] = configs
    
    return df_result
