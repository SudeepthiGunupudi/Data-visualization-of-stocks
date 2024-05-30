#python3.8
import boto3
import json

ssm = boto3.client('ssm')
ec2_instance_id = 'i-0bf19d93a11877cba'  # Replace with your EC2 instance ID

def lambda_handler(event, context):
    try:
        # Send the command to the EC2 instance to list cron jobs
        response = ssm.send_command(
            InstanceIds=[i-0bf19d93a11877cba],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['crontab -l']}
        )
        
        # Get the command ID
        command_id = response['Command']['CommandId']
        
        # Wait for the command to complete
        waiter = ssm.get_waiter('command_executed')
        waiter.wait(
            CommandId=command_id,
            InstanceId=i-0bf19d93a11877cba
        )
        
        # Get the command output
        output = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=i-0bf19d93a11877cba
        )
        
        # Check if the command succeeded
        if output['Status'] == 'Success':
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'success',
                    'data': output['StandardOutputContent']
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'status': 'error',
                    'message': output['StandardErrorContent']
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        }