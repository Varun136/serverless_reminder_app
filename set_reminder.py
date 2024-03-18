from datetime import datetime
import boto3

CLIENT = "dynamodb"
TABLE_NAME = "reminder_table"


def get_epoch_from_datetime(datetime_str):
    epoch = str(int(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timestamp()))
    return epoch


def lambda_handler(event, context):

    # Data extraction.
    user_id = event.get("user_id")

    date = event.get("datetime")
    data_epoch = get_epoch_from_datetime(date)

    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    added_on_epoch = get_epoch_from_datetime(added_on)

    note = event.get("note")
    email = event.get("email") if event.get("email") else ""
    sms = event.get("sms") if event.get("sms") else ""

    # Adding to db.
    client = boto3.client(CLIENT)

    try:
        response = client.put_item(
            TableName=TABLE_NAME,
            Item={
                "user_id": {"S": user_id},
                "ttl": {"S": data_epoch},
                "added_on": {"S": added_on_epoch},
                "note": {"S": note},
                "email": {"S": email},
                "sms": {"S": sms},
            },
        )
    except Exception as e:
        print(e)
        return {}

    return {"statusCode": 200, "body": "Succesfully set reminder"}
