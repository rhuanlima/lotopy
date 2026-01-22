import pandas as pd
from collections import Counter
import source.cycle_calculator as cc

def analyze_cycle_exit_patterns(df):
    """
    Analisa a ordem de saída dos números em cada ciclo e identifica padrões comuns.
    
    Retorna:
    - DataFrame com as sequências de contagem de números sorteados por concurso dentro de cada ciclo.
      Ex: 15-5-3-2 (15 no 1º sorteio, 5 novos no 2º, 3 novos no 3º, etc.)
    """
    if "ciclo" not in df.columns:
        df = cc.calculate_cycle(df)
        
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    cycle_patterns = []
    
    # Agrupar por ciclo
    for ciclo, df_ciclo in df.groupby("ciclo"):
        # Ignorar o último ciclo se ele não estiver fechado e for o último (checagem: se não tem 25 numeros total)
        # Queremos padrões de ciclos FECHADOS
        
        numeros_acumulados = set()
        padrao_ciclo = []
        
        # Ordenar concursos dentro do ciclo
        df_ciclo = df_ciclo.sort_values("Concurso")
        
        for idx, row in df_ciclo.iterrows():
            numeros_concurso = set()
            for campo in lst_campos:
                if pd.notna(row[campo]):
                    numeros_concurso.add(int(row[campo]))
            
            # Novos números neste sorteio (que não estavam nos acumulados)
            novos = numeros_concurso - numeros_acumulados
            qtd_novos = len(novos)
            
            padrao_ciclo.append(qtd_novos)
            numeros_acumulados.update(numeros_concurso)
            
        # Verificar se o ciclo fechou (25 números)
        if len(numeros_acumulados) == 25:
            # Converter padrão para string para contar: "15-5-3-2"
            pattern_str = "-".join(map(str, padrao_ciclo))
            cycle_patterns.append(pattern_str)

    # Contar frequência dos padrões
    counter = Counter(cycle_patterns)
    df_patterns = pd.DataFrame(counter.items(), columns=["Padrao", "Frequencia"])
    df_patterns["Percentual"] = (df_patterns["Frequencia"] / df_patterns["Frequencia"].sum()) * 100
    df_patterns = df_patterns.sort_values("Frequencia", ascending=False)
    
    return df_patterns

def analyze_new_numbers_distribution(df):
    """
    Analisa quantos números NOVOS são sorteados em cada passo do ciclo (tirando o 1º sorteio do ciclo).
    
    Retorna:
    - Dicionário onde a chave é o passo do ciclo (2, 3, 4...) e o valor é um DataFrame
      com a distribuição de probabilidade da quantidade de números novos.
    """
    if "ciclo" not in df.columns:
        df = cc.calculate_cycle(df)
        
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Armazenar contagens por passo: passo_stats[2] = [5, 4, 5, 3...] (quantidades de novos no passo 2)
    passo_stats = {} 
    
    for ciclo, df_ciclo in df.groupby("ciclo"):
        numeros_acumulados = set()
        df_ciclo = df_ciclo.sort_values("Concurso")
        
        passo = 1
        for idx, row in df_ciclo.iterrows():
            numeros_concurso = set()
            for campo in lst_campos:
                if pd.notna(row[campo]):
                    numeros_concurso.add(int(row[campo]))
            
            novos = numeros_concurso - numeros_acumulados
            qtd_novos = len(novos)
            
            if passo > 1:
                # Se não é o primeiro sorteio (que sempre tem 15 novos)
                if passo not in passo_stats:
                    passo_stats[passo] = []
                passo_stats[passo].append(qtd_novos)
            
            numeros_acumulados.update(numeros_concurso)
            passo += 1
            
            # Se completou o ciclo, paramos
            if len(numeros_acumulados) == 25:
                break
                
    # Processar estatísticas
    results = {}
    for passo, contagens in passo_stats.items():
        counter = Counter(contagens)
        df_dist = pd.DataFrame(counter.items(), columns=["Qtd_Novos", "Frequencia"])
        # Garantir que Qtd_Novos seja inteiro para ordenação correta
        df_dist["Qtd_Novos"] = df_dist["Qtd_Novos"].astype(int)
        df_dist["Percentual"] = (df_dist["Frequencia"] / df_dist["Frequencia"].sum()) * 100
        df_dist = df_dist.sort_values("Qtd_Novos")
        results[passo] = df_dist
        
    return results

def analyze_frequency_by_cycle_step(df, max_steps=4):
    """
    Analisa quais números mais saem em cada rodada (passo) do ciclo.
    
    Args:
        df: DataFrame com dados
        max_steps: Número máximo de passos a analisar (padrão 4)
        
    Returns:
        dict: {passo: DataFrame com frequências}
    """
    if "ciclo" not in df.columns:
        df = cc.calculate_cycle(df)
        
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Armazenar contagens por passo: step_counts[1] = Counter({1: 50, 2: 30...})
    step_counts = {step: Counter() for step in range(1, max_steps + 1)}
    
    for ciclo, df_ciclo in df.groupby("ciclo"):
        df_ciclo = df_ciclo.sort_values("Concurso")
        
        passo = 1
        for idx, row in df_ciclo.iterrows():
            if passo > max_steps:
                break
                
            numeros_concurso = []
            for campo in lst_campos:
                if pd.notna(row[campo]):
                    numeros_concurso.append(int(row[campo]))
            
            # Contar números neste passo
            step_counts[passo].update(numeros_concurso)
            passo += 1

    # Formatar resultados
    results = {}
    for step, contador in step_counts.items():
        if not contador:
            continue
            
        df_freq = pd.DataFrame(contador.items(), columns=["Numero", "Frequencia"])
        
        total_occurrences = df_freq["Frequencia"].sum()
        # O total de ocorrências é (num_ciclos * 15), mas usamos a soma real
        
        df_freq["Percentual"] = (df_freq["Frequencia"] / total_occurrences) * 100
        # Normalizar percentual por jogo (frequência / num_jogos_nesse_passo)
        # Mas para simplificar, vamos manter percentual relativo ao total de números sorteados nessa posição
        
        df_freq = df_freq.sort_values("Frequencia", ascending=False)
        results[step] = df_freq
        
    return results

