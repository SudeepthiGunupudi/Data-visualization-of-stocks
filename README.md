#Data-visualization-of-stocks

Required website:
https://iexcloud.io/
https://crontab.guru/

Step 1 : 
gather_data.py will collect the data from IEX Cloud and plot Boxplot, Scatter graph and Histogram of JP Morgan, Bank of America, Citigroup, Wells Fargo and Goldman Sachs over the period of 10 years. the output will be bank_data.png which is as below.
		
![Example Image](https://github.com/SudeepthiGunupudi/Data-visualization-of-stocks/blob/main/bank_data.png)

Step 2 :
Create S3 bucket to store the visualisation. Give all the permissions to the bucket. Modify the BUCKET_POLICY.json as below:

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::stock-analysis-of-banks/*"
        }
    ]
}

```
After running gather_data.py the image will be loaded to S3 bucket.

Step 3 :
Create AWS EC2 instance. Configure AWS on local machine.
```sh
aws configure
```

Connect to the EC2 instance from the Command prompt using the following commands and import python libraries:
```sh
#Command to connect to EC2 serever from the Command Prompt:
ssh -i project123.pem ec2-user@ipaddress

#Import python libraries in EC2 instance:
sudo yum install python3-pip
pip3 install pandas
pip3 install boto3
```

Import gather_data.py to EC2 instance:
```sh
#Command to copy the file from local folder to the EC2 instance
scp -i path/to/.pem_file path/to/file   username@host_address.amazonaws.com:/path_to_copy
```

Step 4 :
Create cron jobs to update at regular intervals. We can choose the contents of cron jobs using CRON Guru website.
```sh
#Creating cron jobs
vim bank_stock_data.cron
00 7 * * 7 python3 gather_data.py #add to bank_stock_data.cron by choosing the interval from cron guru website
crontab -l  # listing cron jobs
crontab bank_stock_data.cron  #adding cron jobs
```

Step 5 :
Create a lambda function to read Cron jobs from EC2 instance.
Steps to follow : AWS Management Console > Create function > Author from scratch > Create function

Lambda function:
```python
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

```
Configure the test event (json file as shown below) and test it. Output should be 200. Save the function.

```json
{}
```

Step 6 :

Create API Gateway

Create a REST API:
Go to the API Gateway console.
Click on "Create API" and choose "REST API".
Provide a name for your API (e.g., CronJobsAPI).

Create a Resource and Method:
Create a new resource (e.g., /read-cron).
Create a new GET method under this resource.
Choose "Lambda Function" as the integration type and select your Lambda function (ReadCronJobs).

Deploy the API:
Create a new deployment stage (e.g., dev).
Note the invoke URL for your API.


Step 7 :
Create the Frontend to Display Cron Jobs

Create an S3 Bucket:
Go to the S3 console,Create a new bucket (e.g., cron-jobs-viewer).Enable static website hosting for the bucket.

Upload an HTML File:
Create an HTML file (index.html) with the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cron Jobs Viewer</title>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            fetch('YOUR_API_GATEWAY_URL/read-cron')  // Replace with your API Gateway URL
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('cron-content').textContent = data.data;
                    } else {
                        document.getElementById('cron-content').textContent = 'Error: ' + data.message;
                    }
                })
                .catch(error => {
                    document.getElementById('cron-content').textContent = 'Error fetching cron jobs';
                });
        });
    </script>
</head>
<body>
    <h1>Cron Jobs</h1>
    <pre id="cron-content">Loading...</pre>
</body>
</html>

```
Upload the File to S3:
Upload index.html to your S3 bucket.
Make sure the file is publicly accessible.

Step 8 : 
Test the Setup. Access the S3 URL:
Go to the S3 bucket URL (e.g., http://your-bucket-name.s3-website-region.amazonaws.com).
Verify the Output:
The web page should display the cron jobs fetched from the Lambda function via the API Gateway.


