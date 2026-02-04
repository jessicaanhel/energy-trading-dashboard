from backend.app.api.sync_csv_to_dynamo import sync_csv_to_dynamo


def lambda_handler(event, context):
    sync_csv_to_dynamo()
    return {"statusCode": 200}