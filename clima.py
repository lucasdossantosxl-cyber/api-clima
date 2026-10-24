# ==============================================================================
# SISTEMA DE PREVISÃO DO CLIMA INTERATIVO
# Versão: 0.6 (Update - Analytics + Persistência)
# Status: Completo, gerando relatórios físicos e métricas de uso.
# ==============================================================================
# HISTÓRICO DE ALTERAÇÕES (CHANGELOG):
# v0.1 a v0.4 - Evolução de validações, vento e separação de módulos.
# v0.5 - Exibição do nome completo do estado por extenso na interface.
# v0.6 - [ATUAL]
#        - Adicionado Painel de Métricas (Analytics) com médias e picos.
#        - Adicionada geração automática de arquivo de texto (.txt) de relatório.
# ==============================================================================

#importamos as bibliotecas json, random e urlib
import urllib.request
import json
import random

# IMPORTAÇÃO: Buscando o nosso "banco de dados" do arquivo vizinho estados.py
from estados import ESTADOS_BRASIL

#crie uma funçao que vai roda a verificaçao inicial do code e seus dados 
def rodar_sistema_clima():
    print("="*55)
    print("       SISTEMA METEOROLÓGICO BRASILEIRO v0.6       ")
    print("="*55)
    
    # Exibe a lista completa dos 27 estados carregados do outro arquivo
    print("Estados disponíveis para consulta:")
    siglas = list(ESTADOS_BRASIL.keys())
    for i in range(0, len(siglas), 6):
        linha = "  |  ".join(siglas[i:i+6])
        print(f"  {linha}")
        
    print("-" * 55)
    print("ATENÇÃO: Digite APENAS a sigla de 2 letras do estado (ex: SP, RJ, MA).")
    print("-" * 55)
    
    estado_escolhido = input("Digite a sigla desejada: ").strip().upper()
    
    # Validação se a sigla existe dentro do arquivo de estados importado
    if estado_escolhido not in ESTADOS_BRASIL:
        print("\n[Status: Erro 404 - Estado Não Permitido]")
        print(f"Erro: A sigla '{estado_escolhido}' não existe ou não é uma UF válida do Brasil.")
        print("Script encerrado. Muito obrigado!")
        return

    # nossa verificaçao ele vai tentar rodar esses blocos abaixo
    try:
        # url virou a variavel para facilitar guardar o link da api (desembrulhando a tupla)
        cidade_api = ESTADOS_BRASIL[estado_escolhido][0]
        nome_estado_completo = ESTADOS_BRASIL[estado_escolhido][1]
        
        url = f"https://wttr.in/{cidade_api}?format=j1"
        
        # o req cria o pedido de acesso a api e o heades faz um disfarce no codigo
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # o with ele abre a pi para pegar seus dados
        with urllib.request.urlopen(req) as resposta:
            # o dados faz o tratamento e leitura de tudo
            dados = json.loads(resposta.read().decode())
            
        # no temp ele pega os dados da lista e usa o valor inteiro neles
        temp_base = int(dados['current_condition'][0]['temp_C'])
        vento_base = int(dados['current_condition'][0]['windspeedKmph'])
        
    # co de erro ele da um print e return
    except Exception as erro:
        print(f"Ops, erro ao conectar com a API base: {erro}")
        return

    # faz uma pergunta para o usuario se nao ele da um muito obrigado e fecha caso sim ele entra no loop abaixo
    quer_saber = input("\nGostaria de saber a previsão do tempo para este mês? (s/n): ").strip().lower()
    if quer_saber != 's':
        print("Muito obrigado!")
        return

    # Histórico estruturado para salvar os dados da tabela final
    historico_consultas = []
    
    # Lista simples apenas para checar duplicações rapidamente
    dias_consultados = []

    # loop pprimeira coisa que ele faz e pedir um data do dia da previsao que vai ser dada aleatoria apartir disso
    while True:
        dia_input = input("\nDigite um dia do mês (de 1 a 31) para ver a previsão simulada: ").strip()

        # caso voce de um valor errado ele da erro e pede novmente
        if not dia_input.isdigit():
            print("Erro: Por favor, digite um número inteiro válido.")
            continue

        # dia vai ser um valor inteiro
        dia = int(dia_input)

        # Aviso claro de que o dia não existe no calendário (Simulando Erro 404)
        if dia < 1 or dia > 31:
            print("\n[Status: Erro 404 - Not Found]")
            print(f"Erro: O dia {dia} não existe no calendário! Tente um dia válido de 1 a 31.")
            continue

        if dia in dias_consultados:
            print(f"\n[Status: Erro 400 - Bad Request]")
            print(f"O dia {dia} já foi informado! Por favor, utilize outro dia.")
            continue

        dias_consultados.append(dia)

        # Geração dos dados do clima baseados na API real
        variacao_temp = random.randint(-5, 5)
        temp_simulada = temp_base + variacao_temp
        
        variacao_vento = random.randint(-8, 8)
        vento_simulado = max(0, vento_base + variacao_vento) 
        
        umidade_simulada = random.randint(50, 90)
        condicoes = ["Ensolarado", "Chuva Moderada", "Parcialmente Nublado", "Tempo Limpo", "Tempestade Isolada"]
        condicao_simulada = random.choice(condicoes)

        print(f"\n--- PREVISÃO PARA O DIA {dia} EM {nome_estado_completo.upper()} ---")
        print(f"Condição: {condicao_simulada}")
        print(f"Temperatura Média: {temp_simulada}°C")
        print(f"Velocidade do Vento: {vento_simulado} km/h")
        print(f"Umidade do Ar: {umidade_simulada}%")

        while True:
            nota = input("\nQuão útil foi essa informação para você? (Avalie de 0 a 5): ").strip()
            if nota in ['0', '1', '2', '3', '4', '5']:
                break 
            else:
                print("Erro: Entrada inválida! Digite apenas um número de 0 a 5.")

        historico_consultas.append({
            "dia": dia,
            "temperatura": temp_simulada,
            "vento": vento_simulado,
            "nota": nota
        })

        continuar = input("\nVocê quer saber a previsão de mais algum dia? (s/n): ").strip().lower()
        if continuar != 's':
            break

    # Tabela resumo final
    print("\n" + "="*62)
    print(f"   TABELA RESUMO DE FEEDBACKS - ESTADO: {nome_estado_completo.upper()}")
    print("="*62)
    print(f"{'Dia Consultado':<15} | {'Temp. Gerada':<13} | {'Vento Gerado':<13} | {'Nota Feedback':<10}")
    print("-" * 62)
    
    # aqui ele da o hiistorico de avaliaçoes da pessoa todas suas avaliaçoes e climas dias consultados etc..
    for registro in historico_consultas:
        print(f"Dia {registro['dia']:<11} | {registro['temperatura']:<10}°C | {registro['vento']:<9} km/h | Nota: {registro['nota']:<10}")
        
    print("="*62)

    # Painel de métricas (Analytics) - puxa os valores salvos e calcula médias e picos
    if historico_consultas:
        todas_notas = [int(reg['nota']) for reg in historico_consultas]
        todas_temps = [reg['temperatura'] for reg in historico_consultas]
        todos_ventos = [reg['vento'] for reg in historico_consultas]
        
        media_satisfacao = sum(todas_notas) / len(todas_notas)
        max_temperatura = max(todas_temps)
        min_temperatura = min(todas_temps)
        max_vento = max(todos_ventos)
        
        print("\nPAINEL DE MÉTRICAS DA SESSÃO:")
        print(f" -> Total de dias analisados: {len(historico_consultas)}")
        print(f" -> Média de utilidade dos dados: {media_satisfacao:.1f} / 5.0")
        print(f" -> Temperatura máxima registrada: {max_temperatura}°C (Mínima: {min_temperatura}°C)")
        print(f" -> Maior velocidade de vento simulada: {max_vento} km/h")
        print("="*62)

    # Criação automática do arquivo de texto para persistência com tratamento de caracteres
    if historico_consultas:
        nome_arquivo = f"relatorio_clima_{estado_escolhido}.txt"
        
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"=== RELATÓRIO METEOROLÓGICO: {nome_estado_completo.upper()} ===\n\n")
            arquivo.write(f"{'Dia':<6} | {'Temperatura':<12} | {'Vento':<10} | {'Nota':<5}\n")
            arquivo.write("-" * 45 + "\n")
            
            for reg in historico_consultas:
                arquivo.write(f"Dia {reg['dia']:<2} | {reg['temperatura']:<9}°C | {reg['vento']:<6} km/h | Nota: {reg['nota']}\n")
                
        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso no seu computador!")
        print("="*62)

    print("Muito obrigado por utilizar nosso sistema!\n")

#para o  script que esta sendo execuado direto do terminal
if __name__ == "__main__":
    rodar_sistema_clima()