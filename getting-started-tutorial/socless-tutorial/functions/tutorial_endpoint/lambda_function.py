from socless import create_events
import json

def lambda_handler(event, context):
    alert_payload  = json.loads(event['body'])
    event_details = {
        'event_type': alert_payload['alert_name'],
        'playbook': alert_payload['response_plan'],
        'details': alert_payload['details']
    }
    try:
        create_events(event_details, context)
    except Exception as e:
        return {"statusCode": 400, "body": f"{e}"}
    return {"statusCode": 200}
