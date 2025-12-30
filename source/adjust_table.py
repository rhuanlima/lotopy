import pandas as pd

def adjust_table():
    """Função para ajustar a tabela do banco de dados."""
    df = pd.read_excel("data/D_lotfac.xlsx")
    df = df[
        [
            "Concurso",
            "Data Sorteio",
            "Bola1",
            "Bola2",
            "Bola3",
            "Bola4",
            "Bola5",
            "Bola6",
            "Bola7",
            "Bola8",
            "Bola9",
            "Bola10",
            "Bola11",
            "Bola12",
            "Bola13",
            "Bola14",
            "Bola15",
        ]
    ]
    df = df.drop_duplicates()

    lst_campos = [
        "Bola1",
        "Bola2",
        "Bola3",
        "Bola4",
        "Bola5",
        "Bola6",
        "Bola7",
        "Bola8",
        "Bola9",
        "Bola10",
        "Bola11",
        "Bola12",
        "Bola13",
        "Bola14",
        "Bola15",
    ]
    df[lst_campos] = df[lst_campos].astype("Int64")
    return df
