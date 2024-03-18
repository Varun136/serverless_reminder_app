import json
import logging
import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

SES_CLIENT = "ses"
CLIENT_EMAIL = "varun.learn.aws@gmail.com"
REMINDER_SUBJECT = "Reminder from Reminder App"


def send_email(sender_email, recipient_email, subject, body):
    ses_client = boto3.client(SES_CLIENT)
    email_msg = {"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}}
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={"ToAddresses": [recipient_email]},
            Message=email_msg,
        )
        print("Email sent! Message ID:", response["MessageId"])
        return True
    except ClientError as e:
        print("Error sending email:", e)
        return False


def lambda_handler(event, context):
    data = event["Records"][0]
    event_type = data.get("eventName")
    if not event_type == "REMOVE":
        return {}

    reminder_data = data.get("dynamodb").get("OldImage")
    note = reminder_data.get("note")
    if note:
        note = note.get("S")
    if not note:
        return {}

    email = reminder_data.get("email")
    if email:
        email = email.get("S")
    if not email:
        return {}

    send_email(CLIENT_EMAIL, email, REMINDER_SUBJECT, note)

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
