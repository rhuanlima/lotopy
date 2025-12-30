import source.db_update as dbu
import source.adjust_table as at
import source.analisys as an
import source.cycle_calculator as cc

# atualizando o banco de dados
# ajustando a tabela
if __name__ == "__main__":
    dbu.update_db(save_path="./data/D_lotfac.xlsx")
    df = at.adjust_table()
    print("Banco de dados atualizado e ajustado com sucesso!")

analise = an.fr_pip(df)
print("Análise de frequência concluída com sucesso!")
print("As combinações de (P)ares-(I)mpares-(NP)úmeros Primos mais frequentes são:")
print(analise)
print("================================")

# Calculando os ciclos
df_com_ciclo = cc.calculate_cycle(df)
print("\nCálculo de ciclos concluído!")
print(f"Total de ciclos identificados: {df_com_ciclo['ciclo'].max()}")

# Estatísticas dos ciclos
estatisticas_ciclos = cc.get_cycle_statistics(df_com_ciclo)
print("\nEstatísticas dos ciclos:")
print(estatisticas_ciclos)

# Números sorteados no ciclo atual
numeros_ciclo_atual = cc.get_numbers_in_current_cycle(df_com_ciclo)
print(f"\nNúmeros já sorteados no ciclo atual: {sorted(numeros_ciclo_atual)}")
print(f"Total: {len(numeros_ciclo_atual)} números")

# Números faltantes no ciclo atual
numeros_faltantes = cc.get_missing_numbers_in_current_cycle(df_com_ciclo)
print(f"\nNúmeros que faltam no ciclo atual: {sorted(numeros_faltantes)}")
print(f"Total: {len(numeros_faltantes)} números")
print("================================")
