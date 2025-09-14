# Projeto 3 - Limpeza e Preparação de Dados Para Modelos de Machine Learning com SageMaker, Docker e Python

# Imports
import argparse
import os
import pandas as pd

# Função de processamento dos dados
def dsa_processamento():

    # Argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='/opt/ml/processing/input')
    parser.add_argument('--output', type=str, default='/opt/ml/processing/output')
    args = parser.parse_args()

    # Preenche os argumentos com os nomes dos datasets de entrada e saída
    input_data_path = os.path.join(args.input, 'dados_brutos.csv')
    output_data_path = os.path.join(args.output, 'dados_limpos.csv')

    # Carrega os dados de entrada
    df = pd.read_csv(input_data_path)

    # Remoção de duplicatas
    df = df.drop_duplicates()

    # Tratamento de valores ausentes
    df['nome'] = df['nome'].fillna('Desconhecido')          # Preenche nomes ausentes com "Desconhecido"
    df['idade'] = df['idade'].fillna(df['idade'].median())  # Imputação da mediana para valores ausentes em 'idade'

    # Transformação do tipo de dado
    df['idade'] = df['idade'].astype(int)
    df['salario'] = df['salario'].astype(float)

    # Salva os dados limpos
    df.to_csv(output_data_path, index=False)

    print(f"\nProcessamento concluído. Arquivo salvo em: {output_data_path}\n")

# Bloco principal
if __name__ == '__main__':
    dsa_processamento()





