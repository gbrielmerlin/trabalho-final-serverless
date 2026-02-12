import json
import os
import boto3

sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]

def handler(event, context):
    try:
        body = event.get("body")
        if body is None:
            return {"statusCode": 400, "body": json.dumps({"erro": "Body ausente"})}

        payload = json.loads(body)

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(payload, ensure_ascii=False)
        )

        return {
            "statusCode": 202,
            "body": json.dumps({"mensagem": "Recebido e enfileirado para processamento."}, ensure_ascii=False)
        }

    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"erro": "JSON inválido"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"erro": "Erro interno", "detalhe": str(e)})}
