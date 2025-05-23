import boto3
import botocore.exceptions

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

bucket_name = 'qa-s3-auto-bucket'
file_name = 'auto-test.txt'
file_content = b'Contenido de prueba para QA automatizada con S3.'

def create_and_verify_bucket():
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name in buckets:
            print(f'Prueba QA Exitosa: Bucket {bucket_name} creado')
        else:
            print(f'Prueba QA Fallida: Bucket {bucket_name} No encontrado')
    except botocore.exceptions.ClientError as e:
        print(f'Error al crear o verificar el bucket: {e}')

def upload_and_verify_file():
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        objects = [obj['Key'] for obj in response.get('Contents',[])]
        if file_name in objects:
            print(f'Prueba de QA Exitosa Archivo {file_name} subido')
        else:
            print(f'Prueba de QA Fallida Archivo {file_name} no encontrado')
    except botocore.exceptions.ClientError as e:
        print(f'Error al subir o verificar el archivo: {e}')

def download_and_verify_file():
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        downloaded_content = response['Body'].read()
        if downloaded_content == file_content:
            print('Prueba QA Exitosa: El contenido del archivo coincide')
        else:
            print('Prueba de QA Fallida: El contenido del archivo no coincide')
    except botocore.exceptions.ClientError as e:
        print(f'Error al descargar o verificar el archivo: {e}')

if __name__ == '__main__':
    print('Iniciando las pruebas de QA automatizadas para S3 de AWS..')
    create_and_verify_bucket()
    upload_and_verify_file()
    download_and_verify_file()
