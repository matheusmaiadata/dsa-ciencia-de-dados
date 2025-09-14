# Projeto 3 - Limpeza e Preparação de Dados Para Modelos de Machine Learning com SageMaker, Docker e Python

# Imports
import pandas as pd
import numpy as np

# Gera dados sintéticos com problemas
def dsa_gera_amostra_dados():

    data = {
        'id': range(1, 101),
        'nome': ['Nome_' + str(i) if i % 10 != 0 else None for i in range(1, 101)],            # Valores faltantes em 'nome'
        'idade': [np.random.randint(18, 70) if i % 15 != 0 else None for i in range(1, 101)],  # Valores faltantes em 'idade'
        'salario': [np.random.randint(30000, 100000) for _ in range(100)],
    }
    
    df = pd.DataFrame(data)

    # Introduzir duplicatas
    df = pd.concat([df, df.sample(5)])

    # Embaralhar o DataFrame
    df = df.sample(frac=1).reset_index(drop=True)

    # Salvar em um arquivo CSV
    df.to_csv('dados_brutos.csv', index=False)

    print("\nDados gerados com sucesso!\n")

# Bloco de execução
if __name__ == '__main__':
    dsa_gera_amostra_dados()


