from flask import Flask, render_template, redirect, url_for, flash
import pandas as pd
import source.db_update as dbu
import source.adjust_table as at
import source.cycle_calculator as cc
import source.pip_config as pip
import source.number_frequency as nf
import source.game_suggestions as gs
import os
import secrets

app = Flask(__name__)
# Use variável de ambiente para secret_key
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))


def load_data():
    """Carrega e processa os dados da Lotofácil."""
    df = at.adjust_table()
    df = cc.calculate_cycle(df)
    df = pip.calculate_pip_config(df)
    return df


@app.route('/')
def index():
    """Página principal com visualização dos dados."""
    try:
        # Carregar dados
        df = load_data()
        
        # Pegar últimos 15 concursos
        df_ultimos = df.tail(15).copy()
        
        # Preparar dados para o template
        concursos = []
        for index, row in df_ultimos.iterrows():
            numeros = [
                int(row[f"Bola{i}"]) for i in range(1, 16)
                if pd.notna(row[f"Bola{i}"])
            ]
            numeros.sort()
            
            # Formatar data corretamente
            data_sorteio = row['Data Sorteio']
            if pd.notna(data_sorteio):
                if hasattr(data_sorteio, 'strftime'):
                    data_formatada = data_sorteio.strftime('%d/%m/%Y')
                else:
                    data_formatada = str(data_sorteio)
            else:
                data_formatada = ''
            
            concursos.append({
                'concurso': int(row['Concurso']),
                'data': data_formatada,
                'numeros': numeros,
                'ciclo': int(row['ciclo']),
                'config_pip': row['config_pip']
            })

        
        # Reverter para mostrar os mais recentes primeiro
        concursos.reverse()
        
        # Pegar dados dos 25 números
        df_numeros = nf.get_numbers_status_in_cycle(df)
        
        numeros_info = []
        for index, row in df_numeros.iterrows():
            numeros_info.append({
                'numero': int(row['numero']),
                'frequencia': int(row['frequencia']),
                'no_ciclo': row['no_ciclo_atual']
            })
        
        
        # Informações adicionais
        total_concursos = len(df)
        ciclo_atual = int(df['ciclo'].max())
        
        # Gerar sugestões de jogos
        sugestoes = gs.generate_suggestions(df, num_games=6)
        
        return render_template(
            'index.html',
            concursos=concursos,
            numeros_info=numeros_info,
            total_concursos=total_concursos,
            ciclo_atual=ciclo_atual,
            sugestoes=sugestoes
        )
    
    except Exception as e:
        return f"Erro ao carregar dados: {str(e)}", 500


@app.route('/atualizar')
def atualizar_banco():
    """Atualiza o banco de dados com novos concursos."""
    try:
        dbu.update_db(save_path="./data/D_lotfac.xlsx")
        flash('Banco de dados atualizado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar banco de dados: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/api/suggestions')
def api_suggestions():
    """
    API REST para obter sugestões de jogos.
    
    Retorna JSON com 6 estratégias diferentes de sugestões.
    
    Exemplo de uso:
        curl http://localhost:5000/api/suggestions
    
    Retorna:
        {
            "success": true,
            "total_concursos": 3574,
            "ciclo_atual": 759,
            "sugestoes": [
                {
                    "estrategia": "🔥 Números Mais Frequentes",
                    "descricao": "...",
                    "numeros": [1, 2, 3, ...]
                },
                ...
            ]
        }
    """
    try:
        from flask import jsonify

        # Carregar dados
        df = load_data()

        # Gerar sugestões
        sugestoes = gs.generate_suggestions(df, num_games=6)

        # Informações adicionais
        total_concursos = len(df)
        ciclo_atual = int(df['ciclo'].max())

        # Preparar resposta
        response = {
            'success': True,
            'total_concursos': total_concursos,
            'ciclo_atual': ciclo_atual,
            'sugestoes': sugestoes
        }

        return jsonify(response)

    except Exception as e:
        from flask import jsonify
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == "__main__":
    # Configurações de segurança
    port = int(os.environ.get("PORT", 5000))

    # Em produção, usar 0.0.0.0 apenas dentro do container
    # O Docker/proxy reverso controla a exposição externa
    host = "0.0.0.0"

    # Desabilitar debug em produção
    debug = os.environ.get("FLASK_ENV") == "development"

    app.run(host=host, port=port, debug=debug)
