import pandas as pd
import random
from collections import Counter

import source.cycle_analysis as ca
import source.cycle_calculator as cc


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


def generate_heat_map_based(df):
    """
    Gera um jogo baseado no mapa de calor - prioriza áreas quentes da cartela.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números das áreas mais quentes
    """
    import source.global_statistics as gstats
    
    heat_map_data = gstats.calculate_heat_map(df)
    
    # Ordenar por intensidade (frequência) e pegar top 15
    heat_map_sorted = sorted(heat_map_data['heat_map'], key=lambda x: x['intensidade'], reverse=True)
    jogo = [item['numero'] for item in heat_map_sorted[:15]]
    
    return sorted(jogo)


def generate_geographic_balanced(df):
    """
    Gera um jogo balanceado geograficamente - equilibra moldura/miolo e linhas.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números balanceados geograficamente
    """
    import source.global_statistics as gstats
    import source.geographic_analysis as ga
    
    # Pegar estatísticas consolidadas
    geo_stats = gstats.calculate_consolidated_geographic_analysis(df)
    
    # Média ideal: ~9 moldura, ~6 miolo
    # Distribuição ideal por linhas baseada nas médias
    target_moldura = 9
    target_miolo = 6
    
    # Pegar números mais frequentes
    frequentes = get_most_frequent_numbers(df, 25)
    
    # Separar por moldura e miolo
    moldura_nums = [n for n in frequentes if ga.is_moldura(n)]
    miolo_nums = [n for n in frequentes if ga.is_miolo(n)]
    
    # Montar jogo balanceado
    jogo = moldura_nums[:target_moldura] + miolo_nums[:target_miolo]
    
    # Se não temos 15, completar com os mais frequentes
    if len(jogo) < 15:
        for n in frequentes:
            if n not in jogo:
                jogo.append(n)
            if len(jogo) == 15:
                break
    
    return sorted(jogo[:15])


    return sorted(jogo[:15])


def generate_quadrant_based(df):
    """
    Gera um jogo priorizando os quadrantes mais quentes.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números dos quadrantes mais frequentes
    """
    import source.global_statistics as gstats
    import source.geographic_analysis as ga
    
    heat_map_data = gstats.calculate_heat_map(df)
    quadrantes = heat_map_data['quadrantes']
    
    # Ordenar quadrantes por percentual
    q_sorted = sorted([
        ('quadrante1', quadrantes['quadrante1']),
        ('quadrante2', quadrantes['quadrante2']),
        ('quadrante3', quadrantes['quadrante3']),
        ('quadrante4', quadrantes['quadrante4']),
        ('cruz', quadrantes['cruz'])
    ], key=lambda x: x[1]['percentual'], reverse=True)
    
    # Pegar números mais frequentes de cada região
    frequentes = get_most_frequent_numbers(df, 25)
    jogo = []
    
    # Distribuir números pelos quadrantes mais quentes
    for q_name, q_data in q_sorted:
        q_nums = [n for n in frequentes if n in q_data['numeros'] and n not in jogo]
        # Pegar proporcionalmente ao percentual
        qtd = max(1, int(15 * q_data['percentual'] / 100))
        jogo.extend(q_nums[:qtd])
        if len(jogo) >= 15:
            break
    
    # Completar se necessário
    if len(jogo) < 15:
        for n in frequentes:
            if n not in jogo:
                jogo.append(n)
            if len(jogo) == 15:
                break
    
    return sorted(jogo[:15])


def generate_moldura_priority(df):
    """
    Gera um jogo priorizando a moldura (bordas da cartela).
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números priorizando moldura
    """
    import source.global_statistics as gstats
    import source.geographic_analysis as ga
    
    # Pegar estatísticas
    geo_stats = gstats.calculate_consolidated_geographic_analysis(df)
    frequentes = get_most_frequent_numbers(df, 25)
    
    # Separar moldura e miolo
    moldura_nums = [n for n in frequentes if ga.is_moldura(n)]
    miolo_nums = [n for n in frequentes if ga.is_miolo(n)]
    
    # Usar média histórica como referência (aproximadamente 9 moldura, 6 miolo)
    target_moldura = int(geo_stats['moldura']['media_por_jogo'])
    target_miolo = 15 - target_moldura
    
    jogo = moldura_nums[:target_moldura] + miolo_nums[:target_miolo]
    
    # Completar se necessário
    if len(jogo) < 15:
        for n in frequentes:
            if n not in jogo:
                jogo.append(n)
            if len(jogo) == 15:
                break
    
    return sorted(jogo[:15])


def generate_line_balanced(df):
    """
    Gera um jogo balanceado por linhas (L1-L5).
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números balanceados por linhas
    """
    import source.global_statistics as gstats
    import source.geographic_analysis as ga
    
    # Pegar estatísticas de linhas
    geo_stats = gstats.calculate_consolidated_geographic_analysis(df)
    frequentes = get_most_frequent_numbers(df, 25)
    
    # Distribuir por linhas baseado nas médias
    jogo = []
    for linha_data in geo_stats['linhas']:
        linha_num = linha_data['linha']
        target_qtd = int(linha_data['media_por_jogo'])
        
        # Pegar números dessa linha
        linha_range = range((linha_num-1)*5 + 1, linha_num*5 + 1)
        linha_nums = [n for n in frequentes if n in linha_range and n not in jogo]
        
        jogo.extend(linha_nums[:target_qtd])
    
    # Completar se necessário
    if len(jogo) < 15:
        for n in frequentes:
            if n not in jogo:
                jogo.append(n)
            if len(jogo) == 15:
                break
    
    return sorted(jogo[:15])

def generate_smart_cycle_strategy(df):
    """
    Gera um jogo baseado na análise inteligente do ciclo atual.
    Verifica o passo do ciclo e a quantidade provável de números novos.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    if "ciclo" not in df.columns:
        df = cc.calculate_cycle(df)
        
    # Identificar estado atual do ciclo
    faltantes = get_missing_in_cycle(df)
    qtd_faltantes = len(faltantes)
    
    # Se ciclo fechou, inicia novo ciclo (aposta conservadora)
    if qtd_faltantes == 0:
        # Se acabou de fechar, o próximo sorteio é o 1º do próximo ciclo
        # Estratégia: 9 repetidos do último sorteio + 6 ausentes do último sorteio
        # Simulação conservadora
        return generate_recent_hot(df)
        
    # Calcular passo atual (quantos sorteios já ocorreram neste ciclo) + 1 (próximo)
    ultimo_ciclo = df["ciclo"].max()
    passo_atual = len(df[df["ciclo"] == ultimo_ciclo]) + 1
    
    # Consultar distribuição de probabilidade para este passo
    dist_stats = ca.analyze_new_numbers_distribution(df)
    
    qtd_novos_sugerida = 0
    
    if passo_atual in dist_stats:
        # Pegar a quantidade de novos mais frequente para este passo
        # Se houver empate ou múltiplas altas, pega a maior probabilidade
        df_prob = dist_stats[passo_atual]
        if not df_prob.empty:
            qtd_novos_sugerida = int(df_prob.iloc[0]["Qtd_Novos"])
    
    # Se não temos estatística para este passo (ex: passo muito avançado), usamos heurística
    if qtd_novos_sugerida == 0:
        # Se faltam poucos, tenta fechar ou pegar a maioria
        qtd_novos_sugerida = min(qtd_faltantes, 2 if qtd_faltantes > 2 else qtd_faltantes)
        
    # Ajustar se a sugestão for maior que os faltantes disponíveis (impossível)
    qtd_novos_sugerida = min(qtd_novos_sugerida, qtd_faltantes)
    
    # Selecionar os 'novos' (que são os faltantes do ciclo)
    # Priorizar os mais frequentes globalmente dentre os faltantes
    frequentes = get_most_frequent_numbers(df, 25)
    
    # Ordenar faltantes por frequência global
    faltantes_ordenados = sorted(faltantes, key=lambda x: frequentes.index(x) if x in frequentes else 99)
    
    numeros_selecionados = faltantes_ordenados[:qtd_novos_sugerida]
    
    # Completar com números JÁ sorteados no ciclo (repetidos do ciclo)
    # Para completar 15 números
    qtd_restante = 15 - len(numeros_selecionados)
    
    # Pegar números já sorteados no ciclo
    numeros_no_ciclo = list(set(range(1, 26)) - set(faltantes))
    
    # Dentre os já sorteados, preferir os que costumam se repetir (quentes recentes)
    quentes = get_hot_numbers(df, last_n=20, top=25)
    
    # Ordenar por "quentura" recente
    repetidos_ordenados = sorted(numeros_no_ciclo, key=lambda x: quentes.index(x) if x in quentes else 99)
    
    numeros_selecionados.extend(repetidos_ordenados[:qtd_restante])
    
    return sorted(numeros_selecionados[:15])




def generate_cycle_next_step_strategy(df):
    """
    Gera um jogo baseado na frequência dos números na PRÓXIMA rodada do ciclo.
    
    Args:
        df: DataFrame com os concursos
        
    Returns:
        list: Lista com 15 números
    """
    if "ciclo" not in df.columns:
        df = cc.calculate_cycle(df)
        
    # Identificar estado atual do ciclo
    faltantes = get_missing_in_cycle(df)
    qtd_faltantes = len(faltantes)
    
    # Se ciclo fechou, inicia novo (conservador)
    if qtd_faltantes == 0:
        return generate_recent_hot(df)
        
    # Calcular próximo passo (rodada)
    ultimo_ciclo = df["ciclo"].max()
    passo_atual = len(df[df["ciclo"] == ultimo_ciclo])
    proximo_passo = passo_atual + 1
    
    # Obter frequências para o PRÓXIMO passo
    # Analisamos até o passo 10 para garantir cobertura
    freq_data = ca.analyze_frequency_by_cycle_step(df, max_steps=15)
    
    # Se temos dados para o próximo passo
    prioridade_faltantes = []
    if proximo_passo in freq_data:
        df_freq = freq_data[proximo_passo]
        
        # Filtrar apenas os números que estão FALTANDO no ciclo atual
        # Queremos saber: "Dos que faltam, quais costumam sair NESTA rodada?"
        df_freq_missing = df_freq[df_freq['Numero'].isin(faltantes)]
        
        if not df_freq_missing.empty:
            # Ordenar por frequência
            prioridade_faltantes = df_freq_missing['Numero'].tolist()
    
    # Se não temos dados ou lista vazia, usar hot numbers globais para os faltantes
    if not prioridade_faltantes:
        frequentes = get_most_frequent_numbers(df, 25)
        prioridade_faltantes = sorted(faltantes, key=lambda x: frequentes.index(x) if x in frequentes else 99)
    else:
        # Adicionar os faltantes que não estavam na estatística no final da fila
        remaining_missing = [n for n in faltantes if n not in prioridade_faltantes]
        if remaining_missing:
            frequentes = get_most_frequent_numbers(df, 25)
            remaining_sorted = sorted(remaining_missing, key=lambda x: frequentes.index(x) if x in frequentes else 99)
            prioridade_faltantes.extend(remaining_sorted)
            
    # Determinar QUANTOS novos números jogar (Probabilidade)
    dist_stats = ca.analyze_new_numbers_distribution(df)
    qtd_novos_sugerida = 0
    
    # Passo + 1 pois a distribuição é baseada no sorteio futuro (o que vamos jogar)
    passo_jogada = proximo_passo 
    
    if passo_jogada in dist_stats:
        df_prob = dist_stats[passo_jogada]
        if not df_prob.empty:
            qtd_novos_sugerida = int(df_prob.iloc[0]["Qtd_Novos"])
            
    # Fallback ou ajuste
    if qtd_novos_sugerida == 0:
        qtd_novos_sugerida = min(len(faltantes), 2)
        
    qtd_novos_sugerida = min(qtd_novos_sugerida, len(faltantes))
    
    # Selecionar os 'novos'
    numeros_selecionados = prioridade_faltantes[:qtd_novos_sugerida]
    
    # Completar com números JÁ sorteados no ciclo
    qtd_restante = 15 - len(numeros_selecionados)
    numeros_no_ciclo = list(set(range(1, 26)) - set(faltantes))
    quentes = get_hot_numbers(df, last_n=20, top=25)
    repetidos_ordenados = sorted(numeros_no_ciclo, key=lambda x: quentes.index(x) if x in quentes else 99)
    
    numeros_selecionados.extend(repetidos_ordenados[:qtd_restante])
    
    return sorted(numeros_selecionados[:15])


def generate_suggestions(df, num_games=9):
    """
    Gera sugestões de jogos com diferentes estratégias.
    Remove duplicatas e agrupa estratégias que geraram o mesmo jogo.
    
    Args:
        df: DataFrame com os concursos e coluna 'ciclo'
        num_games: Número de sugestões a gerar
        
    Returns:
        list: Lista de dicionários com 'estrategia', 'descricao' e 'numeros'
    """
    todas_sugestoes = [
        {
            'estrategia': '🔥 Áreas Mais Quentes',
            'descricao': 'Baseado no mapa de calor - números das posições mais frequentes',
            'numeros': generate_heat_map_based(df)
        },
        {
            'estrategia': '🎯 Faltantes no Ciclo',
            'descricao': 'Prioriza números que ainda não saíram no ciclo atual',
            'numeros': generate_cycle_priority(df)
        },
        {
            'estrategia': '🗺️ Equilíbrio Geográfico',
            'descricao': 'Balanceia moldura/miolo baseado em padrões históricos',
            'numeros': generate_geographic_balanced(df)
        },
        {
            'estrategia': '🎲 Quadrantes Quentes',
            'descricao': 'Prioriza números dos quadrantes mais frequentes',
            'numeros': generate_quadrant_based(df)
        },
        {
            'estrategia': '🔲 Foco na Moldura',
            'descricao': 'Prioriza números nas bordas da cartela',
            'numeros': generate_moldura_priority(df)
        },
        {
            'estrategia': '📊 Equilíbrio por Linhas',
            'descricao': 'Distribui números balanceadamente pelas 5 linhas',
            'numeros': generate_line_balanced(df)
        },
        {
            'estrategia': '⚖️ Pares-Ímpares-Primos',
            'descricao': 'Mix equilibrado seguindo configurações mais comuns',
            'numeros': generate_balanced_game(df)
        },
        {
            'estrategia': '🔥 Números Quentes Recentes',
            'descricao': 'Números mais frequentes nos últimos 30 concursos',
            'numeros': generate_recent_hot(df)
        },
        {
            'estrategia': '🔄 Ciclo Inteligente (Probabilidade)',
            'descricao': 'Usa estatística de "quantos novos" virão na próxima rodada',
            'numeros': generate_smart_cycle_strategy(df)
        },
        {
            'estrategia': '🔮 Ciclo Próxima Rodada (Frequência)',
            'descricao': 'Prioriza números que historicamente saem nesta rodada específica do ciclo',
            'numeros': generate_cycle_next_step_strategy(df)
        },
        {
            'estrategia': '🧠 Análise Combinada',
            'descricao': 'Algoritmo que pondera múltiplos fatores estatísticos',
            'numeros': generate_combined_analysis(df)
        }
    ]
    
    # Deduplicação
    sugestoes_unicas = {}
    
    for sug in todas_sugestoes:
        # Criar chave única baseada nos números ordenados
        numeros_tuple = tuple(sorted(sug['numeros']))
        
        if numeros_tuple in sugestoes_unicas:
            # Se já existe, adicionar a estratégia à lista (append)
            sugestoes_unicas[numeros_tuple]['estrategia'] += " + " + sug['estrategia']
            # Opcional: manter a descrição da primeira ou concatenar
        else:
            sugestoes_unicas[numeros_tuple] = sug
            
    # Converter de volta para lista
    lista_final = list(sugestoes_unicas.values())
    
    # Limitar quantidade se necessário (mas priorizar unicidade)
    return lista_final[:num_games]

