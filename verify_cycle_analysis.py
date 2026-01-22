
import pandas as pd
import source.adjust_table as at
import source.cycle_calculator as cc
import source.cycle_analysis as ca
import source.game_suggestions as gs
import sys
import os

def verify():
    print("Iniciando verificação...")
    
    # 1. Carregar dados
    print("Carregando dados...")
    try:
        df = at.adjust_table()
        df = cc.calculate_cycle(df)
        print(f"Dados carregados. Total de registros: {len(df)}")
    except Exception as e:
        print(f"ERRO ao carregar dados: {e}")
        return

    # 2. Testar Patterns
    print("\nTestando analyze_cycle_exit_patterns...")
    try:
        patterns = ca.analyze_cycle_exit_patterns(df)
        print("Padrões encontrados (top 5):")
        print(patterns.head())
        if patterns.empty:
            print("AVISO: DataFrame de padrões vazio.")
    except Exception as e:
        print(f"ERRO em analyze_cycle_exit_patterns: {e}")

    # 3. Testar Distribuição de Novos
    print("\nTestando analyze_new_numbers_distribution...")
    try:
        dist = ca.analyze_new_numbers_distribution(df)
        print("Passos encontrados:", list(dist.keys()))
        if 2 in dist:
             print("Distribuição para passo 2 (top 5):")
             print(dist[2].head())
    except Exception as e:
        print(f"ERRO em analyze_new_numbers_distribution: {e}")

    # 4. Testar Sugestão de Jogo
    print("\nTestando generate_smart_cycle_strategy...")
    try:
        game = gs.generate_smart_cycle_strategy(df)
        print(f"Jogo gerado ({len(game)} números): {game}")
        if len(game) != 15:
             print("ERRO: Jogo gerado não tem 15 números!")
    except Exception as e:
        print(f"ERRO em generate_smart_cycle_strategy: {e}")
        import traceback
        traceback.print_exc()

    print("\nVerificação concluída.")

if __name__ == "__main__":
    # Adicionar diretório atual ao path para imports funcionarem
    sys.path.append(os.getcwd())
    verify()
