import source.db_update as dbu
import source.adjust_table as at
import source.analisys as an

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
