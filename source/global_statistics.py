"""
Módulo para análise estatística global dos sorteios da Lotofácil.

Fornece funções para calcular estatísticas agregadas de toda a base de dados.
"""

import pandas as pd
from collections import Counter
import source.geographic_analysis as ga


def calculate_global_line_distribution(df):
    """
    Calcula a distribuição de números por linha em toda a base.
    
    Args:
        df: DataFrame com todos os concursos
        
    Returns:
        dict: Estatísticas de distribuição por linha
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Contadores por linha
    linha1_count = 0
    linha2_count = 0
    linha3_count = 0
    linha4_count = 0
    linha5_count = 0
    total_numeros = 0
    
    # Distribuições (formato "L1-L2-L3-L4-L5")
    distribuicoes = []
    
    for index, row in df.iterrows():
        numeros = [int(row[campo]) for campo in lst_campos if pd.notna(row[campo])]
        geo_dist = ga.analyze_geographic_distribution(numeros)
        
        linha1_count += geo_dist['linha1']
        linha2_count += geo_dist['linha2']
        linha3_count += geo_dist['linha3']
        linha4_count += geo_dist['linha4']
        linha5_count += geo_dist['linha5']
        total_numeros += len(numeros)
        
        distribuicoes.append(geo_dist['distribuicao_linhas'])
    
    # Calcular percentuais
    total_concursos = len(df)
    
    return {
        'linha1': {
            'total': linha1_count,
            'percentual': round((linha1_count / total_numeros) * 100, 2),
            'media_por_jogo': round(linha1_count / total_concursos, 2)
        },
        'linha2': {
            'total': linha2_count,
            'percentual': round((linha2_count / total_numeros) * 100, 2),
            'media_por_jogo': round(linha2_count / total_concursos, 2)
        },
        'linha3': {
            'total': linha3_count,
            'percentual': round((linha3_count / total_numeros) * 100, 2),
            'media_por_jogo': round(linha3_count / total_concursos, 2)
        },
        'linha4': {
            'total': linha4_count,
            'percentual': round((linha4_count / total_numeros) * 100, 2),
            'media_por_jogo': round(linha4_count / total_concursos, 2)
        },
        'linha5': {
            'total': linha5_count,
            'percentual': round((linha5_count / total_numeros) * 100, 2),
            'media_por_jogo': round(linha5_count / total_concursos, 2)
        },
        'distribuicoes_mais_comuns': Counter(distribuicoes).most_common(10)
    }


def calculate_global_pip_distribution(df):
    """
    Calcula a distribuição de Pares-Ímpares-Primos em toda a base.
    
    Args:
        df: DataFrame com todos os concursos
        
    Returns:
        dict: Estatísticas de P-I-NP
    """
    # Contadores
    config_pip_counter = Counter()
    
    for index, row in df.iterrows():
        if pd.notna(row.get('config_pip')):
            config_pip_counter[row['config_pip']] += 1
    
    total = sum(config_pip_counter.values())
    
    # Converter para lista com percentuais
    distribuicao = []
    for config, count in config_pip_counter.most_common(10):
        distribuicao.append({
            'config': config,
            'frequencia': count,
            'percentual': round((count / total) * 100, 2)
        })
    
    return {
        'total_concursos': total,
        'distribuicao': distribuicao
    }


def calculate_global_moldura_miolo(df):
    """
    Calcula a distribuição de Moldura vs Miolo em toda a base.
    
    Args:
        df: DataFrame com todos os concursos
        
    Returns:
        dict: Estatísticas de moldura/miolo
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    moldura_count = 0
    miolo_count = 0
    total_numeros = 0
    
    # Distribuições moldura-miolo
    distribuicoes = []
    
    for index, row in df.iterrows():
        numeros = [int(row[campo]) for campo in lst_campos if pd.notna(row[campo])]
        geo_dist = ga.analyze_geographic_distribution(numeros)
        
        moldura_count += geo_dist['moldura']
        miolo_count += geo_dist['miolo']
        total_numeros += len(numeros)
        
        dist_str = f"{geo_dist['moldura']}M-{geo_dist['miolo']}Mi"
        distribuicoes.append(dist_str)
    
    total_concursos = len(df)
    
    return {
        'moldura': {
            'total': moldura_count,
            'percentual': round((moldura_count / total_numeros) * 100, 2),
            'media_por_jogo': round(moldura_count / total_concursos, 2)
        },
        'miolo': {
            'total': miolo_count,
            'percentual': round((miolo_count / total_numeros) * 100, 2),
            'media_por_jogo': round(miolo_count / total_concursos, 2)
        },
        'distribuicoes_mais_comuns': Counter(distribuicoes).most_common(10)
    }


def calculate_heat_map(df):
    """
    Calcula o mapa de calor da cartela - frequência de cada número de 1 a 25.
    Inclui análise de quadrantes e cruz.
    
    Args:
        df: DataFrame com todos os concursos
        
    Returns:
        dict: Mapa de calor com análise de quadrantes e cruz
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Contar frequência de cada número
    numero_counter = Counter()
    
    # Definir quadrantes e cruz
    quadrante1 = {1, 2, 6, 7}  # Superior esquerdo
    quadrante2 = {4, 5, 9, 10}  # Superior direito
    quadrante3 = {16, 17, 21, 22}  # Inferior esquerdo
    quadrante4 = {19, 20, 24, 25}  # Inferior direito
    cruz = {3, 8, 11, 12, 13, 14, 15, 18, 23}  # Centro em forma de cruz
    
    # Contadores de quadrantes e cruz
    q1_count = 0
    q2_count = 0
    q3_count = 0
    q4_count = 0
    cruz_count = 0
    total_numeros = 0
    
    for index, row in df.iterrows():
        numeros = [int(row[campo]) for campo in lst_campos if pd.notna(row[campo])]
        for num in numeros:
            numero_counter[num] += 1
            
            # Contar por quadrante/cruz
            if num in quadrante1:
                q1_count += 1
            elif num in quadrante2:
                q2_count += 1
            elif num in quadrante3:
                q3_count += 1
            elif num in quadrante4:
                q4_count += 1
            elif num in cruz:
                cruz_count += 1
            
            total_numeros += 1
    
    # Calcular total e preparar resultado
    total_aparicoes = sum(numero_counter.values())
    max_freq = max(numero_counter.values())
    min_freq = min(numero_counter.values())
    
    # Calcular range para melhor sensibilidade visual
    freq_range = max_freq - min_freq
    
    heat_map = []
    for num in range(1, 26):
        freq = numero_counter.get(num, 0)
        percentual = round((freq / total_aparicoes) * 100, 2)
        
        # Intensidade ajustada para melhor sensibilidade (0-100)
        # Usar o range para amplificar diferenças
        if freq_range > 0:
            intensidade = round(((freq - min_freq) / freq_range) * 100, 1)
        else:
            intensidade = 50.0
        
        # Identificar região
        if num in quadrante1:
            regiao = 'Q1'
        elif num in quadrante2:
            regiao = 'Q2'
        elif num in quadrante3:
            regiao = 'Q3'
        elif num in quadrante4:
            regiao = 'Q4'
        elif num in cruz:
            regiao = 'Cruz'
        else:
            regiao = 'Outro'
        
        heat_map.append({
            'numero': num,
            'frequencia': freq,
            'percentual': percentual,
            'intensidade': intensidade,
            'regiao': regiao
        })
    
    total_concursos = len(df)
    
    # Análise de quadrantes e cruz
    quadrantes_analysis = {
        'quadrante1': {
            'numeros': sorted(list(quadrante1)),
            'total': q1_count,
            'percentual': round((q1_count / total_numeros) * 100, 2),
            'media_por_jogo': round(q1_count / total_concursos, 2)
        },
        'quadrante2': {
            'numeros': sorted(list(quadrante2)),
            'total': q2_count,
            'percentual': round((q2_count / total_numeros) * 100, 2),
            'media_por_jogo': round(q2_count / total_concursos, 2)
        },
        'quadrante3': {
            'numeros': sorted(list(quadrante3)),
            'total': q3_count,
            'percentual': round((q3_count / total_numeros) * 100, 2),
            'media_por_jogo': round(q3_count / total_concursos, 2)
        },
        'quadrante4': {
            'numeros': sorted(list(quadrante4)),
            'total': q4_count,
            'percentual': round((q4_count / total_numeros) * 100, 2),
            'media_por_jogo': round(q4_count / total_concursos, 2)
        },
        'cruz': {
            'numeros': sorted(list(cruz)),
            'total': cruz_count,
            'percentual': round((cruz_count / total_numeros) * 100, 2),
            'media_por_jogo': round(cruz_count / total_concursos, 2)
        }
    }
    
    return {
        'heat_map': heat_map,
        'quadrantes': quadrantes_analysis,
        'min_freq': min_freq,
        'max_freq': max_freq
    }


def calculate_consolidated_geographic_analysis(df):
    """
    Análise geográfica consolidada combinando linhas e moldura/miolo.
    
    Args:
        df: DataFrame com todos os concursos
        
    Returns:
        dict: Estatísticas consolidadas
    """
    lst_campos = [f"Bola{i}" for i in range(1, 16)]
    
    # Contadores
    linha_counts = [0, 0, 0, 0, 0]  # L1 a L5
    moldura_count = 0
    miolo_count = 0
    total_numeros = 0
    
    # Distribuições
    distribuicoes_linhas = []
    distribuicoes_moldura = []
    
    for index, row in df.iterrows():
        numeros = [int(row[campo]) for campo in lst_campos if pd.notna(row[campo])]
        geo_dist = ga.analyze_geographic_distribution(numeros)
        
        # Linhas
        linha_counts[0] += geo_dist['linha1']
        linha_counts[1] += geo_dist['linha2']
        linha_counts[2] += geo_dist['linha3']
        linha_counts[3] += geo_dist['linha4']
        linha_counts[4] += geo_dist['linha5']
        
        # Moldura/Miolo
        moldura_count += geo_dist['moldura']
        miolo_count += geo_dist['miolo']
        
        total_numeros += len(numeros)
        
        distribuicoes_linhas.append(geo_dist['distribuicao_linhas'])
        dist_moldura = f"{geo_dist['moldura']}M-{geo_dist['miolo']}Mi"
        distribuicoes_moldura.append(dist_moldura)
    
    total_concursos = len(df)
    
    # Preparar resultado consolidado
    linhas = []
    for i, count in enumerate(linha_counts, 1):
        linhas.append({
            'linha': i,
            'range': f"{(i-1)*5+1}-{i*5}",
            'total': count,
            'percentual': round((count / total_numeros) * 100, 2),
            'media_por_jogo': round(count / total_concursos, 2)
        })
    
    return {
        'linhas': linhas,
        'moldura': {
            'total': moldura_count,
            'percentual': round((moldura_count / total_numeros) * 100, 2),
            'media_por_jogo': round(moldura_count / total_concursos, 2)
        },
        'miolo': {
            'total': miolo_count,
            'percentual': round((miolo_count / total_numeros) * 100, 2),
            'media_por_jogo': round(miolo_count / total_concursos, 2)
        },
        'distribuicoes_linhas_comuns': Counter(distribuicoes_linhas).most_common(5),
        'distribuicoes_moldura_comuns': Counter(distribuicoes_moldura).most_common(5)
    }
