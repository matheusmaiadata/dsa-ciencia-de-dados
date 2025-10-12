# <font color='blue'>Data Science Academy</font>
## <font color='blue'>Microsoft Fabric</font>
## <font color='blue'>Projeto 10</font>
### <font color='blue'>Pipeline de Machine Learning com Microsoft Fabric</font>

# Imports
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Definindo as variáveis de acesso ao dataset
blob_account_name = "azureopendatastorage"
blob_container_name = "mlsamples"
blob_relative_path = "diabetes"
blob_sas_token = r"" # Pode deixar em branco pois o acesso aos dados é livre e anônimo

# Essa linha de código abaixo está configurando o caminho de acesso a um Blob Storage do Azure utilizando o protocolo WASBS (Windows Azure Storage Blob Service). Esse código constrói dinamicamente a URL do dataset armazenado no Azure Blob Storage usando placeholders (%s) para os valores que representam diferentes partes da URL.

# Configurando acesso ao Blob Storage
caminho_dataset = f"wasbs://%s@%s.blob.core.windows.net/%s" % (blob_container_name, blob_account_name, blob_relative_path)

# Essa linha abaixo está configurando o acesso ao Azure Blob Storage no Spark usando um SAS Token (Shared Access Signature). Isso permite que o Spark leia e escreva arquivos no Azure Blob Storage sem precisar armazenar credenciais sensíveis diretamente no código.

# Definindo os parâmetros Spark
spark.conf.set("fs.azure.sas.%s.%s.blob.core.windows.net" % (blob_container_name, blob_account_name), blob_sas_token)

print("Caminho do Dataset: " + caminho_dataset)

# Carregando os dados no formato Parquet
df = spark.read.parquet(caminho_dataset)

display(df)

# Converte os dados para o formato do Pandas
df = df.toPandas()
df.head()

# Separando as variáveis X e y
X, y = df[['AGE', 'SEX', 'BMI', 'BP', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']].values, df['Y'].values

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)

# Criando o experimento no MLflow
experiment_name = "dsacloudprojeto10"
mlflow.set_experiment(experiment_name)

# Função para treinar e avaliar modelo
def treinar_avaliar_modelo(modelo, nome_modelo):

    # Inicia o experimento
    with mlflow.start_run():
      
        # Treinamento
        modelo.fit(X_train, y_train)
        
        # Avaliação no conjunto de treino
        y_train_pred = modelo.predict(X_train)
        train_r2 = r2_score(y_train, y_train_pred)
        
        # Avaliação no conjunto de teste
        y_test_pred = modelo.predict(X_test)
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Logging dos parâmetros e métricas
        mlflow.log_param("estimator", nome_modelo)
        mlflow.log_metric("training_r2_score", train_r2)
        mlflow.log_metric("test_r2_score", test_r2)
        
        # Log do modelo treinado
        mlflow.sklearn.log_model(modelo, nome_modelo)

# Treina e avalia a primeira versão do modelo
treinar_avaliar_modelo(LinearRegression(), "LinearRegression")

# Treina e avalia a segunda versão do modelo
treinar_avaliar_modelo(DecisionTreeRegressor(max_depth = 5), "DecisionTreeRegressor")

# Recuperando os resultados do MLflow
exp = mlflow.get_experiment_by_name(experiment_name)

# Listar todas as colunas disponíveis para verificar os nomes corretos das métricas
df_results = mlflow.search_runs(exp.experiment_id, order_by = ["start_time DESC"], max_results = 2)
print("Colunas disponíveis:", df_results.columns)

# Lista os experimentos criados
experiments = mlflow.search_experiments()
for exp in experiments:
   print(exp.name)

# Imprime detalhes do experimento
experiment_name = "dsacloudprojeto10"
exp = mlflow.get_experiment_by_name(experiment_name)
print(exp)

# Lista o que foi executado no experimento
mlflow.search_runs(exp.experiment_id)

# Selecionando métricas corretamente, verificando se o nome está correto
df_results = df_results[["metrics.training_r2_score", "metrics.test_r2_score", "params.estimator"]]

# Plot dos resultados
fig, ax = plt.subplots()
bar_width = 0.4
bar1 = ax.bar(df_results["params.estimator"], df_results["metrics.training_r2_score"], width = bar_width, label = "R2 em Treino")
bar2 = ax.bar(df_results["params.estimator"], df_results["metrics.test_r2_score"], width = bar_width, label = "R2 em Teste", alpha = 0.7)
ax.set_xlabel("Estimador")
ax.set_ylabel("R2 Score")
ax.set_title("DSA R2 Score x Estimador")
ax.legend()
for bars in [bar1, bar2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2f}", ha = 'center', va = 'bottom', fontweight = 'bold')
plt.show()

