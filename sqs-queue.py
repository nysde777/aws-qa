import boto3
import botocore.exceptions
import json

sqs_client = boto3.client(
    'sqs',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

queue_name = 'qa-auto-test-queue'
message_body = {'message':'Prueba QA automatizada para SQS'}

def create_and_verify_queue():
    try: 
        response = sqs_client.create_queue(QueueName=queue_name)
        queue_url = response['QueueUrl']
        response = sqs_client.list_queues()
        queues = response.get('QueueUrls',[])
        if queue_url in queues:
            print(f'Prueba QA Exitosa Cola {queue_name} creada')
            return queue_url
        else:
            print(f'Prueba de QA Fallida cola {queue_name} no encontrada')
            return None
    except botocore.exceptions.ClientError as e:
        print(f'Error al crear o verificar la cola: {e}')
        return None

def send_and_verify_message(queue_url):
    try:
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
        response = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
        message_count = int(response['Attributes']['ApproximateNumberOfMessages'])
        if message_count > 0:
            print('Prueba QA exitosa: Mensaje enviado.')
        else:
            print('Prueba QA fallida: No se detectaron mensajes en la cola.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al enviar el mensaje: {e}')

def receive_and_verify_message(queue_url):
    try:
        response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        messages = response.get('Messages', [])
        if not messages:
            print('Prueba QA fallida: No se recibieron mensajes.')
            return
        message = messages[0]
        received_body = json.loads(message['Body'])
        if received_body == message_body:
            print('Prueba QA exitosa: El contenido del mensaje coincide.')
        else:
            print('Prueba QA fallida: El contenido del mensaje no coincide.')
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        print('Mensaje eliminado de la cola.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al recibir o verificar el mensaje: {e}')

if __name__ == '__main__':
    print("Iniciando las pruebas QA automatizadas para SQS")
    queue_url = create_and_verify_queue()
    if queue_url:
        send_and_verify_message(queue_url)
        receive_and_verify_message(queue_url)