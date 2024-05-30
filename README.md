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
Create a lambda function to read Cron jobs from EC2 instance



















The gather_data.py script gather the data of banks. The processing is done using the Pandas and Matplotlib. The data is then loaded to amazon S3 bucked.

