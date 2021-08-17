import json
import boto3

client = boto3.client('ec2')

def lambda_handler(event, context):
    scheduled_instances = []
    custom_filter = [{
        'Name':'tag:scheduled', 
        'Values': ['True']
    }]
        
    response = client.describe_instances(Filters=custom_filter)
    
    for r in response['Reservations']:
        for i in r['Instances']:
            print (i['InstanceId'])
            scheduled_instances.append(i['InstanceId'])

    return {
        'statusCode': 200,
        'body': json.dumps(scheduled_instances)
    }

