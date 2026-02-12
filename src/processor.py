import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    for record in event.get("Records", []):
        try:
            payload = json.loads(record["body"])

            table.put_item(Item={
                "id_cliente": payload["id_cliente"],
                "data_hora": payload["data_hora"],
                "descricao": payload["descricao"],
                "categoria": payload["categoria"]
            })

            msg = (
                f"Novo feedback/reclamação recebido\n\n"
                f"Cliente: {payload['id_cliente']}\n"
                f"Categoria: {payload['categoria']}\n"
                f"Data/Hora: {payload['data_hora']}\n"
                f"Descrição: {payload['descricao']}\n"
            )

        except Exception as e:
            raise RuntimeError(f"Falha ao processar mensagem SQS: {str(e)}")

    return {"statusCode": 200}

