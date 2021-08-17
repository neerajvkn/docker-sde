import json
import sys
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

region = 'us-east-2'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    table_name = 'EC2Scheduler-ConfigTable-1HC6CZHH5I2KM'
    client = boto3.resource('dynamodb')
    scheduler_table = client.Table(table_name)
    body = json.loads(event['body'])

    action = body["action"]
    instance_id = body["instance_id"]
    schedule = body["schedule"]
    
    scheduler_exists = check_if_scheduler_exists(instance_id, scheduler_table)
    period_exists = check_if_period_exists(instance_id, scheduler_table)

    if action == "enable_scheduler":
        print("enabling scheduler for " + str(instance_id))
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': 'scheduled',
                    'Value': 'True'
                },
                {
                    'Key': 'Schedule',
                    'Value': instance_id
                },
            ]
        )

        if (period_exists == 1):
            response = scheduler_table.update_item(
                TableName = table_name,
                Key= {
                    'name': instance_id,
                    'type': 'period'
                },
                ExpressionAttributeNames = {
                    '#al1':'weekdays'
                },
                UpdateExpression = "set #al1 = :new_schedule",
                ExpressionAttributeValues={
                    ':new_schedule': {schedule}
                }
            )

        if(period_exists == 0):
            response = scheduler_table.put_item(
                Item={
                    'begintime': '00:00',
                    'endtime': '23:59',
                    'description': 'Scheduler for instance',
                    'weekdays': {schedule},
                    'name': instance_id,
                    'type': 'period'
                    }
                )
            response = scheduler_table.put_item(
                Item={
                    'timezone': 'Asia/Bahrain',
                    'description': "Scheduler for instance",
                    'periods': {instance_id},
                    'name': instance_id,
                    'type': 'schedule'
                    }
                )

        return {
            'statusCode' : 200,
            'body' : "Scheduler Enabled for " + str(instance_id)
        }

    elif action == "disable_scheduler":
       
        print("disabling scheduler for " + str(instance_id))
        ec2.delete_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': 'scheduled'
                },
                {
                    'Key': 'Schedule'
                }
            ]
        )
        if(scheduler_exists == 1):
            response = scheduler_table.delete_item(
                TableName = table_name,
                Key= {
                    'name': instance_id,
                    'type': 'schedule'
                }
            )

        if (period_exists == 1):
            response = scheduler_table.delete_item(
                TableName = table_name,
                Key= {
                    'name': instance_id,
                    'type': 'period'
                }
            )

        if (scheduler_exists == 0):
            pass

        if (period_exists == 0):
            pass

        return {
            'statusCode' : 200,
            'body' : "Scheduler Disabled for " + str(instance_id)
        }

def check_if_scheduler_exists(instance_id, scheduler_table):
    response = scheduler_table.get_item(
        Key={
            'name':instance_id,
            'type':'schedule'
        }
    )
    if 'Item' in response:
        return 1
    else:
        return 0

def check_if_period_exists(instance_id, scheduler_table):
    response = scheduler_table.get_item(
        Key={
            'name':instance_id,
            'type':'period'
        }
    )
    if 'Item' in response:
        return 1
    else:
        return 0
        