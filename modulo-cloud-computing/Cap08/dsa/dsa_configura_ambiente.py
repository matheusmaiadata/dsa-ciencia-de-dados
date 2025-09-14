# Projeto 3 - Limpeza e Preparação de Dados Para Modelos de Machine Learning com SageMaker, Docker e Python

# Imports
import boto3

# Verifica se a IAM Role existe e a cria, se necessário.
def dsa_iam_role(role_name, trust_policy, policies):

    # Cria cliente para o IAM
    iam = boto3.client('iam')

    # Bloco try/except
    try:
        response = iam.get_role(RoleName=role_name)
        print(f"IAM Role '{role_name}' já existe.")
        return response['Role']['Arn']
    except iam.exceptions.NoSuchEntityException:
        print(f"IAM Role '{role_name}' não encontrada. Criando...")
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=trust_policy
        )

        role_arn = response['Role']['Arn']
        print(f"IAM Role '{role_name}' criada com sucesso: {role_arn}")

        for policy in policies:
            iam.attach_role_policy(RoleName=role_name, PolicyArn=policy)
            print(f"Política '{policy}' anexada à IAM Role '{role_name}'.")
        
        return role_arn

# Verifica se o bucket S3 existe e o cria, se necessário.
def dsa_s3_bucket(bucket_name, region):

    # Cria conexão cliente ao S3
    s3 = boto3.client('s3', region_name=region)

    # Verifica os buckets existentes
    existing_buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
    
    # Verifica se o bucket que iremos usar não existe não lista de buckets e então o cria
    if bucket_name not in existing_buckets:
        print(f"Bucket '{bucket_name}' não encontrado. Criando...")
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Bucket '{bucket_name}' criado com sucesso.")
    else:
        print(f"Bucket '{bucket_name}' já existe.")

# Bloco principal
def main():

    # Cria a sessão AWS
    session = boto3.Session()

    # Extrai a região
    region = session.region_name

    # Configurações da IAM Role
    role_name = 'SageMakerExecutionRole-DSA-P3'

    # Trust Policy
    trust_policy = """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "sagemaker.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }"""

    # Define as políticas
    policies = [
        "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
    ]

    # Garantir que a IAM Role e o bucket existam
    print("\nConfigurando a IAM Role e o Bucket S3...\n")
    role_arn = dsa_iam_role(role_name, trust_policy, policies)
    bucket = 'dsa-sagemaker-p3-890582101704'  # Ajustar para o seu AWS ID
    dsa_s3_bucket(bucket, region)

    print("\nConfiguração concluída!")
    print(f"IAM Role ARN: {role_arn}")
    print(f"Bucket S3: {bucket}")

# Bloco de execução
if __name__ == '__main__':
    main()
