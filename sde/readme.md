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

# Setup - Local Setup
1. Install Python 3.9.8 ( if on a windows machine, set path variable pointing to the installation directory)
2. Install pip3 and set path variable
3. Download and extract the repository
4. Open a terminal window and navigate to the extracted repository folder
5. From inside the folder, create a python virtual environment and activate it. ( Refer : https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/ )
6. Once the virtualenv is activated, install flask using 
```
pip3 install flask   
```
7. Install python requests library using
```
pip3 install requests
```
8. Goto the lambda app EC2Schedueler and click the API Gateway on dashboard. 
9. Under Triggers, find the API Function we create and expand details section, and copy the API Endpoint
10. Open the app.py in root the downloaded repo and replace the url assigned to api_url variable under function api_call() with the copied endpoint url
11. Now goto lambda app SchedulerInstances and copy its api endpoint url and replace the value assigned to api_url varible in line 35 under function scheduled_instances() with the copied endpoint url

12. Now Local Machine for development setup is complete. To run the app in the local machine, type
```
python app.py  

or

python3 app.py
```
13. Once the terminal says the app is running, goto any browser and enter the link shown in the terminal window to access the app