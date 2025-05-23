## 🎓 Curso: **Pruebas QA en Local con Simulación de AWS (100% Gratis)**

### 🧩 Módulo 1 – Introducción a AWS desde el enfoque QA✅

* ¿Qué es AWS y por qué es clave para QA?✅
* Casos comunes de QA con servicios cloud✅
* Introducción a LocalStack como simulador de AWS✅

---

### 🐳 Módulo 2 – Preparar el entorno local✅

* Instalación de Docker✅
* Instalación de LocalStack con Docker Compose✅
* Configuración inicial de servicios (S3, SQS, Lambda, DynamoDB, API Gateway)✅
    - Amazon S3 (Simple Storage Service)✅
    - Amazon SQS (Simple Queue Service)✅
    - AWS Lambda✅
    - Amazon DynamoDB✅
    - Amazon API Gateway✅

---

### 🔧 Módulo 3 – Herramientas QA para AWS en local✅

* Instalación y configuración de AWS CLI sin cuenta real✅
* Uso de Postman para probar APIs locales✅
* Instalación de Boto3 y configuración para automatizar pruebas✅

---

### 🗃️ Módulo 4 – Pruebas con S3 (Almacenamiento)✅

* Crear buckets desde CLI✅
* Subir y descargar archivos✅
* Validaciones automatizadas con Python y Boto3✅

--endpoint-url http://localhost:4566
---

### 📬 Módulo 5 – Pruebas con SQS (Colas de mensajes)3✅

* Crear colas de mensajes✅
* Enviar y recibir mensajes manualmente✅
* Validar flujos de mensajería con scripts de prueba✅
-------
# Comandos
+ Crear una cola
aws sqs create-queue --queue-name qa-test-queue --endpoint-url http://localhost:4566

"QueueUrl": "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/qa-test-queue"

+ Listar las colas creadas
aws sqs list-queues --endpoint-url http://localhost:4566

+ Enviar un mensaje a una cola
aws sqs send-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/qa-test-queue --message-body '{\"message\": \"Prueba QA para SQS\"}' --endpoint-url http://localhost:4566

+ mensaje enviado (No ejecutar)
{
    "MD5OfMessageBody": "954d17e2b5d8c288d5e87e3c566c204b",
    "MessageId": "27864058-54ed-4229-8ff3-4e8fdba4fc9c"
}

+ recibir el mensaje de la cola 
aws sqs receive-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/qa-test-queue --endpoint-url http://localhost:4566

+ Eliminar el mensaje Recibido
aws sqs delete-message --queue-url QUEUE_URL --receipt-handle RECEIPT_HANDLE --endpoint-url http://localhost:4566

---

### ⚙️ Módulo 6 – Pruebas con DynamoDB (Base de datos NoSQL)✅

* Crear tablas y cargar datos✅
* Validar consultas y estructuras✅
* Automatización de pruebas CRUD✅
    Crear una tabla y un ítem.
    Leer el ítem.
    Actualizar el ítem.
    Eliminar el ítem.
    Verificar cada operación.
-----------------------------
+ Crear una tabla llamada Users
aws dynamodb create-table `
  --table-name Users `
  --attribute-definitions AttributeName=user_id,AttributeType=S `
  --key-schema AttributeName=user_id,KeyType=HASH `
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
  --endpoint-url http://localhost:4566


+ Verficar que la tabla sea creada
aws dynamodb list-tables --endpoint-url http://localhost:4566

+ Insertamos un item en la tabla Users
aws dynamodb put-item `
  --table-name Users `
  --item '{\"user_id\": {\"S\": \"user1\"}, \"name\": {\"S\": \"Alice\"}, \"email\": {\"S\": \"alice@example.com\"}}' `
  --endpoint-url http://localhost:4566


+ Insertamos otro item
aws dynamodb put-item `
  --table-name Users `
  --item '{\"user_id\": {\"S\": \"user2\"}, \"name\": {\"S\": \"Bob\"}, \"email\": {\"S\": \"bob@example.com\"}}' `
  --endpoint-url http://localhost:4566



---

### 🚀 Módulo 7 – Simulación de APIs con API Gateway✅

* Crear endpoints REST simulados✅
* Validar respuestas y status codes✅
* Pruebas de integración locales con Postman✅

----------------------------------------
+Crear la API REST y guardar el ID

# 1. Crear la API REST
$api = aws apigateway create-rest-api `
  --name TestAPI `
  --endpoint-url http://localhost:4566 | ConvertFrom-Json

$api_id = $api.id
Write-Host "API creada con ID: $api_id"

# 2. Obtener el recurso raíz
$root = aws apigateway get-resources `
  --rest-api-id $api_id `
  --endpoint-url http://localhost:4566 | ConvertFrom-Json

$root_id = $root.items[0].id
Write-Host "Recurso raíz ID: $root_id"

# 3. Crear recurso /test
$test = aws apigateway create-resource `
  --rest-api-id $api_id `
  --parent-id $root_id `
  --path-part test `
  --endpoint-url http://localhost:4566 | ConvertFrom-Json

$test_id = $test.id
Write-Host "Recurso /test creado con ID: $test_id"

# 4. Crear método GET
aws apigateway put-method `
  --rest-api-id $api_id `
  --resource-id $test_id `
  --http-method GET `
  --authorization-type NONE `
  --endpoint-url http://localhost:4566

# 5. Configurar integración MOCK usando archivo JSON
aws apigateway put-integration `
  --rest-api-id $api_id `
  --resource-id $test_id `
  --http-method GET `
  --type MOCK `
  --request-templates file://request-template.json `
  --endpoint-url http://localhost:4566

# 6. Configurar respuesta del método
aws apigateway put-method-response `
  --rest-api-id $api_id `
  --resource-id $test_id `
  --http-method GET `
  --status-code 200 `
  --response-models file://response-models.json `
  --endpoint-url http://localhost:4566

# 7. Configurar respuesta de integración
aws apigateway put-integration-response `
  --rest-api-id $api_id `
  --resource-id $test_id `
  --http-method GET `
  --status-code 200 `
  --response-templates file://response-template.json `
  --endpoint-url http://localhost:4566

# 8. Desplegar la API
aws apigateway create-deployment `
  --rest-api-id $api_id `
  --stage-name dev `
  --endpoint-url http://localhost:4566

# 9. Mostrar la URL final
Write-Host ""
Write-Host "Prueba tu API en:"
Write-Host "http://localhost:4566/restapis/$api_id/dev/_user_request_/test"

---

### 🧠 Módulo 8 – Automatización avanzada en QA

* Framework de pruebas con `pytest` + `boto3`✅
* Mocking de servicios con `moto`(Posterior)
* Integración local continua sin cuenta AWS (Posterior)

---

