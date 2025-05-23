import boto3
import botocore.exceptions

dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)


table_name = 'UsersAutoTest'
item_id = 'user_auto_1'
item = {
    'user_id': {'S': item_id},
    'name': {'S': 'Charlie'},
    'email': {'S': 'charlie@example.com'}
}

# Función para crear una tabla y verificar su existencia.
def create_and_verify_table():
    try:
        # Creamos la tabla con una clave de partición "user_id".
        dynamodb_client.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        response = dynamodb_client.list_tables()
        if table_name in response['TableNames']:
            print(f'Prueba QA exitosa: Tabla {table_name} creada.')
        else:
            print(f'Prueba QA fallida: Tabla {table_name} no encontrada.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al crear o verificar la tabla: {e}')

# Función para crear (Create) un ítem y verificarlo.
def create_item():
    try:
        dynamodb_client.put_item(TableName=table_name, Item=item)
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}}
        )
        if 'Item' in response and response['Item']['user_id']['S'] == item_id:
            print('Prueba QA exitosa: Ítem creado.')
        else:
            print('Prueba QA fallida: Ítem no encontrado.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al crear el ítem: {e}')

# Función para leer (Read) un ítem y validar su contenido.
def read_item():
    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}}
        )
        if 'Item' in response and response['Item']['name']['S'] == item['name']['S']:
            print('Prueba QA exitosa: Ítem leído correctamente.')
        else:
            print('Prueba QA fallida: Contenido del ítem incorrecto.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al leer el ítem: {e}')

# Función para actualizar (Update) un ítem y verificarlo.
def update_item():
    try:
        dynamodb_client.update_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}},
            UpdateExpression='SET email = :val',
            ExpressionAttributeValues={':val': {'S': 'charlie.updated@example.com'}}
        )
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}}
        )
        if 'Item' in response and response['Item']['email']['S'] == 'charlie.updated@example.com':
            print('Prueba QA exitosa: Ítem actualizado.')
        else:
            print('Prueba QA fallida: Ítem no actualizado correctamente.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al actualizar el ítem: {e}')

# Función para eliminar (Delete) un ítem y verificarlo.
def delete_item():
    try:
        dynamodb_client.delete_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}}
        )
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={'user_id': {'S': item_id}}
        )
        if 'Item' not in response:
            print('Prueba QA exitosa: Ítem eliminado.')
        else:
            print('Prueba QA fallida: Ítem aún existe.')
    except botocore.exceptions.ClientError as e:
        print(f'Error al eliminar el ítem: {e}')

# Ejecutamos las pruebas CRUD automatizadas.
if __name__ == '__main__':
    print('Iniciando pruebas QA automatizadas para DynamoDB...')
    create_and_verify_table()
    create_item()
    read_item()
    update_item()
    delete_item()