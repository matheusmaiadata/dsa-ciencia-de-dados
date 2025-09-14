# Projeto 3 - Limpeza e Preparação de Dados Para Modelos de Machine Learning com SageMaker, Docker e Python

# Imports
import os
import time  # Para medir o tempo de execução
import boto3
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput

# Faz o download do arquivo de saída (opcional)
def dsa_download_dados_limpos(bucket, output_prefix, local_output_path):
    s3_output_file = f"{output_prefix}/dados_limpos.csv"
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_output_file, local_output_path)
    print(f"Arquivo 'dados_limpos.csv' baixado para {local_output_path}")

# Bloco principal
def main():

    # Inicia a medição de tempo
    start_time = time.time()
    
    print("\nIniciando o Processamento! Seja Paciente e Aguarde...")
    
    # Cria a sessão AWS
    session = boto3.Session()

    # Cria a sessão SageMaker
    sagemaker_session = sagemaker.Session(boto_session=session)

    # Extrai da sessão o nome da região
    region = session.region_name

    # Configurações do bucket e IAM Role
    role_arn = 'arn:aws:iam::890582101704:role/SageMakerExecutionRole-DSA-P3'  # Atualize com seu AWS ID
    bucket = 'dsa-sagemaker-p3-890582101704'                                   # Atualize com seu AWS ID
    input_prefix = 'dados/input'
    output_prefix = 'dados/output'

    # Caminhos S3 (URI)
    s3_input_path = f's3://{bucket}/{input_prefix}'
    s3_output_path = f's3://{bucket}/{output_prefix}'

    # Upload dos dados de entrada para o S3
    sagemaker_session.upload_data(
        path='dados_brutos.csv',
        bucket=bucket,
        key_prefix=input_prefix
    )

    # Configura o ScriptProcessor
    script_processor = ScriptProcessor(
        image_uri=sagemaker.image_uris.retrieve(framework='sklearn', region=region, version='0.23-1'),
        command=["python3"],
        role=role_arn,
        instance_count=1,
        instance_type='ml.t3.medium',
        sagemaker_session=sagemaker_session
    )

    print("\nExecutando o Processamento...\n")

    # Executa o job de processamento
    script_processor.run(
        code='dsa_limpa_dados.py',
        inputs=[
            ProcessingInput(
                source=s3_input_path,
                destination='/opt/ml/processing/input'
            )
        ],
        outputs=[
            ProcessingOutput(
                source='/opt/ml/processing/output',
                destination=s3_output_path
            )
        ]
    )

    # Faz o download do arquivo de saída
    local_output_path = 'dados_limpos.csv'
    dsa_download_dados_limpos(bucket, output_prefix, local_output_path)

    print("\nProcessamento Concluído com Sucesso!")

    # Finaliza a medição de tempo
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTempo total de execução: {total_time:.2f} segundos.\n")

# Bloco de execução
if __name__ == '__main__':
    main()
