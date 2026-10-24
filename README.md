# API Clima — Sistema Meteorológico Brasileiro

Projeto de estudos em Python que consulta temperatura e velocidade do vento da capital de uma UF brasileira e usa esses valores como base para simular dados meteorológicos. Inclui interface no navegador com Streamlit, versão no terminal e relatórios em texto.

**Os dados dos dias selecionados são simulados:** o mês e o dia não são enviados à API. A aplicação consulta as condições atuais da capital e aplica variações aleatórias para fins de aprendizado.

## Funcionalidades

- Seleção das 27 unidades federativas, incluindo o Distrito Federal.
- Consulta de temperatura e vento pelo serviço wttr.in.
- Simulação de temperatura, vento e condição do tempo.
- Avaliação da utilidade de cada registro com notas de 0 a 5.
- Histórico da sessão e bloqueio de dias repetidos.
- Métricas de quantidade de dias, média das notas, temperaturas máxima e mínima e maior vento.
- Exportação de relatórios `.txt`.
- Na versão Streamlit: escolha do mês, limites de dias conforme o calendário de 2026 e download pelo navegador.

## Estrutura

```text
api-clima/
├── teste.py                            # Interface Streamlit (v0.9)
├── clima.py                            # Aplicação no terminal (v0.6)
├── estados.py                          # UFs, nomes e capitais para consulta
├── relatorio_clima_AC.txt              # Relatório de exemplo
├── relatorio_clima_SC.txt              # Relatório de exemplo
├── relatorio_clima_SP.txt              # Relatório de exemplo
├── relatorio_clima_SP_Fevereiro.txt     # Relatório de exemplo
└── README.md
```

## Instalação

Tenha Python 3, pip e Git instalados, além de conexão com a internet para consultar a API.

Clone o repositório:

```powershell
git clone https://github.com/lucasdossantosxl-cyber/api-clima.git
cd api-clima
```

No Windows PowerShell, crie um ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install streamlit requests
```

Os comandos abaixo usam diretamente o Python do ambiente virtual, dispensando sua ativação. Se você já está na pasta local `estudos_api`, execute os comandos a partir dela, sem clonar novamente.

## Executar no navegador

```powershell
.\.venv\Scripts\python.exe -m streamlit run teste.py
```

Abra o endereço local exibido no terminal.

1. Escolha a UF e o mês na barra lateral.
2. Clique em **Conectar e Buscar Clima Base**.
3. Selecione um dia e uma nota de utilidade.
4. Clique em **Simular e Gravar no Historico**.
5. Confira a tabela e as métricas.
6. Clique em **Fazer Download do Relatorio (.txt)** para salvar os registros.
7. Use **Limpar Dados da Sessao** para iniciar outro histórico.

Ao trocar de UF ou mês, limpe o histórico; ao trocar de UF, clique também em **Conectar e Buscar Clima Base** para atualizar os valores da capital. A troca dos seletores não limpa os registros nem atualiza a consulta automaticamente.

## Executar no terminal

```powershell
.\.venv\Scripts\python.exe clima.py
```

Informe a sigla da UF e siga as perguntas para escolher dias de 1 a 31, avaliar os resultados e encerrar a sessão. Essa versão usa apenas bibliotecas padrão do Python e o módulo local `estados.py`.

Ao terminar uma sessão com registros, o programa salva `relatorio_clima_<UF>.txt` na pasta de execução. Um arquivo existente com o mesmo nome é sobrescrito.

## Como a simulação funciona

A aplicação consulta `https://wttr.in/{cidade}?format=j1` e lê os campos de temperatura em graus Celsius e vento em km/h de `current_condition`. A requisição implementada não usa chave de API.

- **Temperatura:** valor atual acrescido de um número aleatório de −5 a +5 °C.
- **Vento:** valor atual acrescido de um número aleatório de −8 a +8 km/h, com mínimo de zero.
- **Condição do tempo:** definida por faixas de temperatura em `teste.py` e sorteada em `clima.py`.
- **Umidade:** sorteada entre 50% e 90%; exibida somente na versão de terminal e não incluída nos relatórios.

## Relatórios e sessão

Na interface Streamlit, o relatório contém mês, dia, temperatura, vento e nota, e recebe o nome `relatorio_clima_<UF>.txt`. O histórico fica na memória da sessão até ser limpo ou a sessão terminar; o download permite guardar uma cópia.

O controle de duplicidade considera apenas o número do dia, mesmo após mudar o mês ou a UF. O calendário da interface está fixado em 2026, com fevereiro de 28 dias. A versão de terminal aceita dias de 1 a 31 sem selecionar um mês.

## Conceitos praticados

Consumo de API HTTP, leitura de JSON, módulos Python, validação de entradas, tratamento de exceções, listas e dicionários, geração de dados aleatórios, escrita de arquivos e gerenciamento de estado com Streamlit.
