# ==============================================================================
# SISTEMA DE PREVISÃO DO CLIMA INTERATIVO
# Versão: 0.9 (Update - Interface Gráfica com Streamlit)
# Status: Totalmente funcional no navegador, sem loops travados e com download.
# ==============================================================================

# importamos as bibliotecas random, requests e o streamlit para a interface de tela
import streamlit as st
import requests
import random

# IMPORTAÇÃO: Buscando o nosso "banco de dados" do arquivo vizinho estados.py
from estados import ESTADOS_BRASIL

# SISTEMA DE STATUS: Centralização de códigos de resposta para exibição em tela
STATUS_SISTEMA = {
    200: "[Status 200 - OK] Conexao estabelecida com sucesso.",
    400: "[Status 400 - Bad Request] O dia informado ja foi consultado nesta sessao.",
    404: "[Status 404 - Not Found] O dia selecionado nao existe para o mes atual.",
    422: "[Status 422 - Unprocessable Entity] Nota invalida detectada."
}

# ESTRUTURA DE CALENDÁRIO: Define o nome e o limite real de dias para cada mês no ano de 2026
MESES_ANO = {
    1: {"nome": "Janeiro", "dias": 31},
    2: {"nome": "Fevereiro", "dias": 28},
    3: {"nome": "Março", "dias": 31},
    4: {"nome": "Abril", "dias": 30},
    5: {"nome": "Maio", "dias": 31},
    6: {"nome": "Junho", "dias": 30},
    7: {"nome": "Julho", "dias": 31},
    8: {"nome": "Agosto", "dias": 31},
    9: {"nome": "Setembro", "dias": 30},
    10: {"nome": "Outubro", "dias": 31},
    11: {"nome": "Novembro", "dias": 30},
    12: {"nome": "Dezembro", "dias": 31}
}

# CONTROLE DE MEMÓRIA (Session State): Como a pagina recarrega a cada clique, usamos a memoria do Streamlit para manter o historico salvo
if "historico" not in st.session_state:
    st.session_state.historico = []
if "dias_consultados" not in st.session_state:
    st.session_state.dias_consultados = []

# Título principal da tela do navegador
st.title("SISTEMA METEOROLÓGICO BRASILEIRO v0.9")
st.markdown("---")

# Painel Lateral para configurações de localidade e tempo
st.sidebar.header("Configuraçoes de Consulta")

# Substituição da digitação de sigla por um menu interativo com os estados disponíveis
opcao_estado = st.sidebar.selectbox("Escolha o Estado (UF):", list(ESTADOS_BRASIL.keys()))
cidade_api = ESTADOS_BRASIL[opcao_estado][0]
nome_estado_completo = ESTADOS_BRASIL[opcao_estado][1]

# Substituição da digitação do mês por um menu interativo
opcao_mes_num = st.sidebar.selectbox(
    "Escolha o Mes da Consulta:", 
    list(MESES_ANO.keys()), 
    format_func=lambda x: MESES_ANO[x]["nome"]
)
nome_mes = MESES_ANO[opcao_mes_num]["nome"]
max_dias = MESES_ANO[opcao_mes_num]["dias"]

st.sidebar.markdown(f"**Info:** {nome_mes} possui ate {max_dias} dias.")

# Botão para disparar a conexão com a API e buscar dados base do estado selecionado
if st.sidebar.button("Conectar e Buscar Clima Base"):
    try:
        url = f"https://wttr.in/{cidade_api}?format=j1"
        req_headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Faz a conexao utilizando a biblioteca requests com timeout de segurança
        resposta = requests.get(url, headers=req_headers, timeout=5)
        dados = resposta.json()
        
        # Guarda na memoria os valores base encontrados
        st.session_state.temp_base = int(dados['current_condition'][0]['temp_C'])
        st.session_state.vento_base = int(dados['current_condition'][0]['windspeedKmph'])
        st.session_state.tempo_resposta = resposta.elapsed.total_seconds()
        
        st.success(f"{STATUS_SISTEMA[200]} Conectado a {cidade_api.replace('_', ' ')}. Latencia: {st.session_state.tempo_resposta:.2f}s")
        
    except Exception as erro:
        st.error(f"Erro ao conectar com a API base: {erro}")

# Painel Central: Simulação de dias (Só aparece se os dados base existirem na memória)
if "temp_base" in st.session_state:
    st.header(f"Previsoes para {nome_estado_completo} em {nome_mes}")
    
    # Validação dinamica do calendário por meio de um seletor numérico limitado aos dias do mês
    dia_escolhido = st.number_input(f"Selecione o dia do mes (1 a {max_dias}):", min_value=1, max_value=max_dias, value=1)
    
    # Controle de feedbacks via formulário integrado na página
    st.subheader("Gerar Dados e Avaliar")
    nota_feedback = st.slider("Quao util e essa informaçao para voce? (Nota de 0 a 5):", min_value=0, max_value=5, value=5)
    
    if st.button("Simular e Gravar no Historico"):
        if dia_escolhido in st.session_state.dias_consultados:
            st.warning(f"{STATUS_SISTEMA[400]} O dia {dia_escolhido} ja possui registros.")
        else:
            # Geração automatica e amarrada com a regra de clima inteligente
            variacao_temp = random.randint(-5, 5)
            temp_simulada = st.session_state.temp_base + variacao_temp
            
            variacao_vento = random.randint(-8, 8)
            vento_simulado = max(0, st.session_state.vento_base + variacao_vento)
            umidade_simulada = random.randint(50, 90)
            
            if temp_simulada >= 28:
                condicao_simulada = "Ensolarado com Ceu Limpo"
            elif temp_simulada >= 22:
                condicao_simulada = "Parcialmente Nublado"
            elif temp_simulada >= 15:
                condicao_simulada = "Chuva Moderada"
            else:
                condicao_simulada = "Frio Intenso com Nevoa"
                
            # Grava no histórico na memória local da sessão
            st.session_state.dias_consultados.append(dia_escolhido)
            st.session_state.historico.append({
                "dia": dia_escolhido,
                "mes": nome_mes,
                "temperatura": temp_simulada,
                "vento": vento_simulado,
                "condicao": condicao_simulada,
                "nota": nota_feedback
            })
            st.success(f"Dados gerados para o dia {dia_escolhido}: {temp_simulada}°C, {condicao_simulada}, {vento_simulado} km/h.")

# Bloco de Resultados: Tabelas, Painel de métricas e Download de arquivos
if st.session_state.historico:
    st.markdown("---")
    st.header("Resultados e Analises Consolidadas")
    
    # Converte os dados salvos em uma tabela visual limpa na tela do navegador
    st.subheader(f"Tabela Resumo de Feedbacks - {nome_estado_completo.upper()}")
    st.table(st.session_state.historico)
    
    # Painel de Metricas (Analytics) calculando picos e médias em tempo real
    todas_notas = [int(reg['nota']) for reg in st.session_state.historico]
    todas_temps = [reg['temperatura'] for reg in st.session_state.historico]
    todos_ventos = [reg['vento'] for reg in st.session_state.historico]
    
    media_satisfacao = sum(todas_notas) / len(todas_notas)
    max_temperatura = max(todas_temps)
    min_temperatura = min(todas_temps)
    max_vento = max(todos_ventos)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dias Analisados", len(st.session_state.historico))
    col2.metric("Media Utilidade", f"{media_satisfacao:.1f} / 5.0")
    col3.metric("Temp. Max / Min", f"{max_temperatura}°C / {min_temperatura}°C")
    col4.metric("Maior Vento", f"{max_vento} km/h")
    
    # Montagem do arquivo de texto para a transferencia automatica para o computador do usuario
    conteudo_txt = f"=== RELATORIO METEOROLOGICO: {nome_estado_completo.upper()} ===\n\n"
    conteudo_txt += f"{'Mes':<10} | {'Dia':<4} | {'Temperatura':<12} | {'Vento':<10} | {'Nota':<5}\n"
    conteudo_txt += "-" * 55 + "\n"
    for reg in st.session_state.historico:
        conteudo_txt += f"{reg['mes']:<10} | Dia {reg['dia']:<2} | {reg['temperatura']:<9}°C | {reg['vento']:<6} km/h | Nota: {reg['nota']}\n"
        
    st.markdown(" ")
    st.download_button(
        label="Fazer Download do Relatorio (.txt)",
        data=conteudo_txt,
        file_name=f"relatorio_clima_{opcao_estado}.txt",
        mime="text/plain"
    )
    
    # Botão para resetar os registros e limpar a tela caso o usuario queira recomeçar
    if st.button("Limpar Dados da Sessao"):
        st.session_state.historico = []
        st.session_state.dias_consultados = []
        st.rerun()