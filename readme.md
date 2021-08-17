Assuming the user already has a AWS account and instances set up
# Setup - AWS

1. Goto CloudFormation page under services
2. Click and open create stack near top right corner of the page and select 'With new resources( standard)' option
3. Make sure Template is ready option is selected and Amazon S3 URL under specify template section
4. Paste the below URL into Amazon S3 URL box and click Next
```bash
https://s3.amazonaws.com/solutions-reference/aws-instance-scheduler/latest/aws-instance-scheduler.template
```
5. Enter a stack name, Set Default time zone as your current time zone and leave everything else as default and click next on next window
6. In the next window, leave everything as default and click Next
7. At the bottom of the next screen after step 6, tick the acknowledge box and click Create Stack. it will take few minutes to create the stack ( 10-20 mins )
8. Once the stack is created, go to IAM Page and select roles, there you will find a role similar to EC2Scheduler-SchedulerRole-1S0GL7CYBM2SK if not exactly this, click to open that role.
9. Once that role is opened, under policy section, find policy named SchedulerRoleDefaultPolicy66F774B8 or something very similar to it and expand it.
10. Once its expanded, click edit policy, and change the view to JSON tab and replace the 2nd Action item, ( approx on line 23) with the below, then click review policy and save changes.
```
"Action": [
  "dynamodb:BatchGetItem",
  "dynamodb:GetRecords",
  "dynamodb:GetShardIterator",
  "dynamodb:UpdateItem",
  "dynamodb:DeleteItem",
  "dynamodb:GetItem",
  "dynamodb:PutItem",
  "dynamodb:Query",
  "dynamodb:Scan",
  "dynamodb:BatchWriteItem"
 ],
```
11. Now go to AWS Lambda and click create function, select author from scratch, Enter function name ("EC2Scheduler"), change runtime to python 3.9 and under 'Change default execution role', select 'Use an existing role' select the role we found in step 8 and click create function.
12. Once the function is created, replace the contents of code under lambda_function with the contents of EC2Scheduler in the AWS Directory of the repo. 
13. Now goto DynamoDB and under tables, find a table similar to 'EC2Scheduler-ConfigTable-1HC6CZHH5I2KM' and copy its name
14. In the created lambda function ( EC2Scheduler ), on line 11,  replace the table tablename already present there with the copied table name, Ctrl+S to save and click deploy.
15. Then click '+ Add trigger' in the dashboard and select API Gateway as trigger
16. Then under 'Create a new API or attach an existing one', select 'Create an API', and change the selection to REST API' from HTTP API, select security as OPEN
17. Click Add to create and deploy the API

18. Now again go to AWS Lambda and click create function, select author from scratch, Enter function name ("ScheduledInstances"), change runtime to python 3.9 and under 'Change default execution role', select 'Use an existing role' select the role we found in step 8 and click create function.
19. Once the function is created, replace its contents with the contents of ScheduledInstances.py in the AWS Directory of the repo.
20. Repeat the steps 15 to 17 to create an API for this function also.
21. Now Server side of SDE-I Backend Assignment is complete.


# Docker Installation on AWS EC2
1. create a ubuntu 18.04 t2.micro instance

2. open inboud TCP port TCP 80 and 8000 in the security policy for the instance
[ Tyepe : Custom TCP, Port range : 8000, Source : Anywhere IPv4]
[ Tyepe : Custom TCP, Port range : 80, Source : Anywhere IPv4]
and save rules

4. Connect to the instance via SSH

5. Install docker-compose- 
 Add docker official repo using below command and then run sudo apt-get update
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
6. Once repo is added and repo list udpated, run
```
sudo apt-get install docker-compose
```

7. clone repo to the instance
```
https://github.com/neerajvkn/docker-sde
```
8. Once the cloning is complete, navigate to the cloned folder and open docker-compose.yml and replace the server adress 0.0.0.0 with with the public ipv4 address of the instance on which the app is going to be hosted. Save and exit.

9. Now add docker user necessary permission by running - log out and log back in so the changes take effect

```
sudo groupadd docker
sudo usermod -aG docker $USER
```
10. After logginb back in, to build and run the docker app, run 
```
docker-compose up --build -d
```

Now the app can be accessed using the public ipv4 address of the instance