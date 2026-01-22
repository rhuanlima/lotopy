from flask import Flask, render_template, redirect, url_for, flash, request
import pandas as pd
import source.db_update as dbu
import source.adjust_table as at
import source.cycle_calculator as cc
import source.pip_config as pip
import source.number_frequency as nf
import source.game_suggestions as gs
import source.geographic_analysis as ga

import source.global_statistics as gstats
import source.cycle_analysis as ca
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
        
        # Pegar parâmetro de limite (padrão: 15)
        limit = request.args.get('limit', default=15, type=int)
        
        # Validar limite
        if limit not in [5, 10, 15, 20, 25]:
            limit = 15
        
        # Pegar últimos N concursos
        df_ultimos = df.tail(limit).copy()
        
        # Preparar dados para o template
        concursos = []
        for index, row in df_ultimos.iterrows():
            numeros = [
                int(row[f"Bola{i}"]) for i in range(1, 16)
                if pd.notna(row[f"Bola{i}"])
            ]
            numeros.sort()
            
            # Calcular distribuição geográfica
            geo_dist = ga.analyze_geographic_distribution(numeros)
            
            # Análise de quadrantes e cruz
            quadrante1 = {1, 2, 6, 7}
            quadrante2 = {4, 5, 9, 10}
            quadrante3 = {16, 17, 21, 22}
            quadrante4 = {19, 20, 24, 25}
            cruz = {3, 8, 11, 12, 13, 14, 15, 18, 23}
            
            q1 = sum(1 for n in numeros if n in quadrante1)
            q2 = sum(1 for n in numeros if n in quadrante2)
            q3 = sum(1 for n in numeros if n in quadrante3)
            q4 = sum(1 for n in numeros if n in quadrante4)

            cruz_count = sum(1 for n in numeros if n in cruz)
            
            # Análise de Novos vs Repetidos no Ciclo
            ciclo_atual_row = int(row['ciclo'])
            concurso_atual_row = int(row['Concurso'])
            
            # Pegar todos os sorteios ANTERIORES do MESMO ciclo
            df_ciclo_ant = df[(df['ciclo'] == ciclo_atual_row) & (df['Concurso'] < concurso_atual_row)]
            
            numeros_acumulados_ciclo = set()
            lst_campos = [f"Bola{i}" for i in range(1, 16)]
            
            for _, r_ant in df_ciclo_ant.iterrows():
                for campo in lst_campos:
                    if pd.notna(r_ant[campo]):
                        numeros_acumulados_ciclo.add(int(r_ant[campo]))
            
            # Calcular quantos dos números atuais são novos (não estavam nos acumulados)
            numeros_novos_ciclo = 0
            numeros_repetidos_ciclo = 0
            
            # Se não tem acumulados, todos são novos (primeiro do ciclo)
            # Mas o problema pede "novos" vs "já saíram".
            # No primeiro sorteio, todos são "novos" no ciclo.
            
            for n in numeros:
                if n in numeros_acumulados_ciclo:
                    numeros_repetidos_ciclo += 1
                else:
                    numeros_novos_ciclo += 1

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
                'config_pip': row['config_pip'],
                'moldura': geo_dist['moldura'],
                'miolo': geo_dist['miolo'],
                'linha1': geo_dist['linha1'],
                'linha2': geo_dist['linha2'],
                'linha3': geo_dist['linha3'],
                'linha4': geo_dist['linha4'],
                'linha5': geo_dist['linha5'],
                'distribuicao_linhas': geo_dist['distribuicao_linhas'],
                'q1': q1,
                'q2': q2,
                'q3': q3,
                'q4': q4,
                'q4': q4,
                'cruz': cruz_count,
                'q4': q4,
                'cruz': cruz_count,
                'novos_ciclo': numeros_novos_ciclo,
                'repetidos_ciclo': numeros_repetidos_ciclo,
                'novos_set': list(numeros_acumulados_ciclo.symmetric_difference(set(numeros) | numeros_acumulados_ciclo)) # Números que NÃO estavam nos acumulados (são novos)
            })

        
        # Reverter para mostrar os mais recentes primeiro
        concursos.reverse()
        
        # Pegar dados dos 25 números
        df_numeros = nf.get_numbers_status_in_cycle(df)
        
        # Calcular total de aparições para percentuais
        total_aparicoes = df_numeros['frequencia'].sum()
        
        numeros_info = []
        for index, row in df_numeros.iterrows():
            numeros_info.append({
                'numero': int(row['numero']),
                'frequencia': int(row['frequencia']),
                'percentual': round((int(row['frequencia']) / total_aparicoes) * 100, 2),
                'no_ciclo': row['no_ciclo_atual']
            })
        
        
        # Informações adicionais
        total_concursos = len(df)
        ciclo_atual = int(df['ciclo'].max())
        
        # Calcular estatísticas globais
        consolidated_geo = gstats.calculate_consolidated_geographic_analysis(df)
        global_pip_dist = gstats.calculate_global_pip_distribution(df)
        global_pip_dist = gstats.calculate_global_pip_distribution(df)
        heat_map = gstats.calculate_heat_map(df)
        
        # Análise de Ciclos (Novas implementações)
        # Padrões de saída (ex: 15-5-3-2)
        df_cycle_patterns = ca.analyze_cycle_exit_patterns(df)
        cycle_patterns = df_cycle_patterns.head(10).to_dict('records')
        
        # Distribuição de Novos Números por Passo do Ciclo
        dist_novos_stats = ca.analyze_new_numbers_distribution(df)
        
        # Converter para formato amigável para o template (lista de objetos)
        dist_novos_display = []
        for passo, df_dist in dist_novos_stats.items():
            dist_novos_display.append({
                'passo': passo,
                'dados': df_dist.to_dict('records')
            })
            
        # Ordenar por passo
        dist_novos_display.sort(key=lambda x: x['passo'])
        
        # Análise de Frequência por Rodada do Ciclo
        freq_by_step = ca.analyze_frequency_by_cycle_step(df, max_steps=4)
        freq_by_step_display = []
        for step, df_freq in freq_by_step.items():
            freq_by_step_display.append({
                'step': step,
                'dados': df_freq.head(10).to_dict('records') # Top 10 por rodada
            })
        freq_by_step_display.sort(key=lambda x: x['step'])
        
        # Gerar sugestões de jogos

        sugestoes = gs.generate_suggestions(df, num_games=9)
        
        # Adicionar análise completa para cada sugestão
        for sugestao in sugestoes:
            numeros = sugestao['numeros']
            
            # Análise geográfica
            geo_dist = ga.analyze_geographic_distribution(numeros)
            sugestao['moldura'] = geo_dist['moldura']
            sugestao['miolo'] = geo_dist['miolo']
            sugestao['distribuicao_linhas'] = geo_dist['distribuicao_linhas']
            
            # Análise de ciclo
            lst_campos = [f"Bola{i}" for i in range(1, 16)]
            numeros_no_ciclo = sum(1 for n in numeros if n in df[df['ciclo'] == ciclo_atual][lst_campos].values.flatten())
            sugestao['ciclo_count'] = numeros_no_ciclo
            
            # Análise P-I-NP
            pares = sum(1 for n in numeros if n % 2 == 0)
            impares = sum(1 for n in numeros if n % 2 != 0)
            primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23}
            primos = sum(1 for n in numeros if n in primos_set)
            sugestao['config_pip'] = f"{pares}P-{impares}I-{primos}NP"
            
            # Análise de quadrantes e cruz
            quadrante1 = {1, 2, 6, 7}
            quadrante2 = {4, 5, 9, 10}
            quadrante3 = {16, 17, 21, 22}
            quadrante4 = {19, 20, 24, 25}
            cruz = {3, 8, 11, 12, 13, 14, 15, 18, 23}
            
            sugestao['q1'] = sum(1 for n in numeros if n in quadrante1)
            sugestao['q2'] = sum(1 for n in numeros if n in quadrante2)
            sugestao['q3'] = sum(1 for n in numeros if n in quadrante3)
            sugestao['q4'] = sum(1 for n in numeros if n in quadrante4)
            sugestao['cruz'] = sum(1 for n in numeros if n in cruz)
        
        return render_template(
            'index.html',
            concursos=concursos,
            numeros_info=numeros_info,
            total_concursos=total_concursos,
            ciclo_atual=ciclo_atual,
            sugestoes=sugestoes,

            limit=limit,
            consolidated_geo=consolidated_geo,
            global_pip_dist=global_pip_dist,
            heat_map=heat_map,
            cycle_patterns=cycle_patterns,
            dist_novos_display=dist_novos_display,
            freq_by_step_display=freq_by_step_display
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
