## ETL de dados climáticos usando Airflow

Este projeto de estudos demonstra um processo de **ETL (Extract, Transform, Load)** de dados climáticos utilizando o **Apache Airflow**. A pipeline foi projetada para coletar informações meteorológicas de diversas cidades brasileiras, processá-las e armazená-las em um banco de dados.

### Visão Geral do Projeto

O fluxo de trabalho, orquestrado por uma **DAG (Directed Acyclic Graph)** no Airflow, é dividido nas seguintes etapas:

  * **Extração (Extract):** Utiliza a **API OpenWeather** para extrair dados climáticos atualizados de cidades específicas do Brasil.
  * **Transformação (Transform):** Os dados brutos são processados e formatados para garantir a consistência e a qualidade antes de serem carregados.
  * **Carga (Load):** As informações transformadas são carregadas e persistidas em um banco de dados.

### Como Executar o Projeto

Siga os passos abaixo para rodar o projeto localmente:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```
2.  **Inicialize o Airflow e o banco de dados:**
    ```bash
    docker compose up airflow-init
    ```
3.  **Inicie os serviços do Airflow:**
    ```bash
    docker compose up
    ```
4.  **Acesse a interface web do Airflow:**
    Abra seu navegador e navegue para:
    ```
    http://localhost:8080/login
    ```
5.  **Faça login:**
    Use as credenciais padrão para acessar o painel do Airflow:
      * **User:** `airflow`
      * **Senha:** `airflow`

Após o login, a DAG do projeto estará visível e pronta para ser executada na interface do Airflow.