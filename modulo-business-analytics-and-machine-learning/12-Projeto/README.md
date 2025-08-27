# Day Trade Analytics em Tempo Real com Agentes de IA 📈

## Resumo da Solução
Este projeto é uma ferramenta inteligente criada para simplificar a análise de ações do mercado financeiro. Imagine ter um consultor de investimentos disponível 24/7 que, ao invés de levar horas para analisar gráficos e notícias, entrega em segundos uma recomendação clara e visualizações essenciais sobre qualquer ativo que você desejar.

A aplicação web analisa em tempo real o ticker de uma ação e, com o uso de Inteligência Artificial, gera um resumo executivo com uma recomendação direta: comprar, vender ou manter. Além disso, ela exibe quatro gráficos interativos que apresentam o histórico de preços, o comportamento do mercado, as principais tendências e o volume de negociação, tudo para auxiliar em uma tomada de decisão mais rápida e bem-informada.

🎯 O Problema Solucionado
No dinâmico mercado financeiro, investidores e analistas enfrentam o desafio de processar um volume massivo de informações dispersas — notícias, relatórios, cotações e análises de mercado. Essa sobrecarga de dados pode levar a decisões tardias ou mal fundamentadas.

Nossa solução ataca diretamente essa dor, centralizando a coleta de dados e aplicando uma camada de IA para "traduzir" a complexidade do mercado em insights acionáveis, economizando tempo e reduzindo o risco de erro humano.

## Funcionalidades Principais
✅ Resumo com Inteligência Artificial: Um sistema de agentes de IA lê as notícias mais recentes e as recomendações de analistas para gerar um parecer conciso sobre o ativo.

📊 Visualizações de Dados Abrangentes: Quatro gráficos essenciais para uma análise completa nos últimos 6 meses:

Gráfico de Preço: A evolução do valor da ação.

Gráfico Candlestick: Uma visão detalhada da variação diária de preços (abertura, fechamento, máxima e mínima).

Médias Móveis (SMA & EMA): Indicadores cruciais para identificar tendências de curto e longo prazo.

Volume de Negociação: A quantidade de ações negociadas ao longo do tempo, indicando a força de uma tendência.

## Detalhes Técnicos e Arquitetura
A aplicação foi construída com uma arquitetura moderna, combinando extração de dados em tempo real, um sistema de IA multiagente e uma interface de usuário interativa.

Arquitetura dos Agentes de IA
O núcleo da inteligência da aplicação é um sistema composto por três agentes autônomos, orquestrados para fornecer a melhor recomendação possível:

Agente Pesquisador (Web Search Agent): Utiliza o DuckDuckGo para varrer a internet em busca das notícias mais recentes e relevantes sobre o ticker informado, focando em fatos que possam impactar o preço da ação.

Agente Analista Financeiro (Financial Analyst Agent): Especializado em extrair e interpretar os dados e as recomendações de analistas publicadas no Yahoo Finance, uma fonte consolidada de informações de mercado.

Agente Orquestrador (Master Agent): Recebe as informações dos outros dois agentes, as consolida, analisa o sentimento geral e a força das evidências, e então elabora o resumo final com a recomendação de "Comprar", "Vender" ou "Manter".

Este sistema foi implementado utilizando a biblioteca Phi para a estruturação dos agentes e o poder de processamento de LLMs de alta velocidade da Groq via API.

## Tecnologias Utilizadas
Interface e Frontend: Streamlit

Extração de Dados Financeiros: yfinance

Visualização de Dados: Plotly

Orquestração de IA: Phi

Motor de IA (LLM): Groq API

Hospedagem e Deploy: AWS (EC2)

Gerenciador de Pacotes: uv

## Como Executar o Projeto
Siga as instruções abaixo para executar a aplicação em seu ambiente local ou em nuvem.

### Ambiente Local
Pré-requisitos: Ter o uv instalado.

1. Clone este repositório:

```bash
git clone https://github.com/matheusmaiadata/dsa-ciencia-de-dados.git
cd modulo-business-analytics-and-machine-learning/12-Projeto
```

2. Instale as dependências com o uv:

```bash
uv add -r requirements.txt
```

3. Crie um arquivo .env na raiz do projeto e adicione sua chave da API da Groq:

```
GROQ_API_KEY="sua-chave-aqui"
```

4. Execute a aplicação:

```bash
uv run streamlit run dsa_app.py
```

### Em Nuvem (AWS)
Configuração da Instância:

1. Crie uma instância EC2 na camada gratuita da AWS (ex: t2.micro).

2. Habilite um IP público para a instância.

3. No Security Group, permita tráfego de entrada nas portas:

- SSH (porta 22) para acesso ao terminal.

- HTTP (porta 80).

4. Adicione uma regra customizada (Custom TCP) para a porta 8501 (padrão do Streamlit), permitindo acesso de qualquer IP (0.0.0.0/0).

5. Setup do Ambiente na Instância:

    1. Acesse o terminal da sua instância via SSH.

    2. Baixe e instale o Miniconda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
Miniconda3-latest-Linux-x86_64.sh
```

    3. Crie uma pasta para o projeto e envie os arquivos dsa_app.py, requirements.txt e o .env (com a chave da API) para dentro dela.

6. Execução:

    1. Navegue até a pasta do projeto e instale as dependências:

```bash
pip install -r requirements.txt
```

    2. Execute a aplicação em segundo plano usando nohup:

```bash
nohup streamlit run dsa_app.py --server.port=8501 --server.address=0.0.0.0 &
```

    3. Agora você pode acessar a aplicação através do navegador usando: http://[IP-PUBLICO-DA-SUA-INSTANCIA]:8501