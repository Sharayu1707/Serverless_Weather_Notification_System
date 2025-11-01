# Serverless_Weather_Notification_System

## Overview

The Serverless Weather Notification System is an AWS-based application that fetches weather data from an external API and sends notifications (via email or SMS) using AWS services.

It is fully serverless, leveraging AWS Lambda, SNS, and EventBridge to automate notifications without managing servers.

## Architecture 

EventBridge (Scheduler)
        ↓ 
AWS Lambda (Weather Fetch + Logic)
        ↓
Amazon SNS (Notification)
        ↓
Subscribers (Email / SMS)


## Services used 

IAM Role – Grants Lambda permission to access SNS and other AWS services.

Amazon SNS – Sends notifications.

Amazon EventBridge – Schedules Lambda.

AWS Lambda – Runs code to fetch/process weather data.


## Prerequisites

AWS account with proper permissions

Python installed (depending on Lambda code)

Weather API key (e.g., OpenWeatherMap)


## Step-by-Step Setup

### Step 1: Create IAM Role

Purpose: To give permission for Lambda to publish messages to SNS and write logs.

Go to IAM → Roles → Create Role

Select Trusted Entity: AWS Service

Use Case: Lambda

Attach Policies:

AWSLambdaBasicExecutionRole → allows Lambda to write logs to CloudWatch

AmazonSNSFullAccess → allows Lambda to send messages via SNS

Name Role: LambdaWeatherNotificationRole

Click Create Role

![Architecture](images/img-1.png)

### Step 2: Create an SNS Topic

Go to AWS SNS Console.

Click Create Topic → Choose Standard → Enter WeatherAlerts as the topic name.

Note the ARN (e.g., arn:aws:sns:ap-south-1:123456789012:WeatherAlerts).


![Architecture](images/img-2.png)

### Step 3: Subscribe to the Topic

In the SNS Topic, click Create Subscription.

Choose protocol:

✉️ Email → Enter your email address.

📱 SMS → Enter your phone number.

Confirm the subscription via the link sent to your email or SMS.


![Architecture](images/img-3.png)

### Step 4: Create a Lambda Function

![Architecture](images/img-4.png)

Go to AWS Lambda Console → Click Create Function.

Choose Author from scratch → Name: WeatherNotifier.

Runtime: Python 3.11 or Node.js 18.x.

Permissions:

Attach policy: AWSLambdaBasicExecutionRole

Attach policy: AmazonSNSFullAccess (or least privilege to publish to SNS)

### Step 5: Add Lambda Code

⚠️ Update SNS_ARN, API_KEY, and CITY with your values.

Step 6: Configure EventBridge Rule

Go to Amazon EventBridge → Rules → Create Rule.

Select Schedule → Set a cron expression or rate (e.g., cron(0 8 * * ? *) for every day at 8 AM).

Choose target: Lambda function (WeatherNotifier).

Save the rule.


![Architecture](images/img-5.png)

⏰ EventBridge Role: Automatically triggers Lambda at the scheduled time, ensuring weather notifications are sent daily without manual intervention.

### Step 7: Test Lambda

Go to Lambda → Test → Configure test event.

Use default JSON ({}) → Click Test.

Check your email or SMS for the weather update.

## Advantages

Fully automated – Sends weather updates without manual work.

Low cost – Uses serverless AWS services, so you only pay per use.

Scalable – Can handle thousands of notifications easily.

Reliable – EventBridge and SNS ensure no message is missed.

Easy to maintain – No server or infrastructure to manage.

Real-time alerts – Users get instant updates via email or SMS.

## Disadvantages

Limited message format – SNS messages are text-only (no rich templates).

Cold start delay – Lambda may take a few seconds for the first run.

API dependency – If the weather API fails, no alert will be sent.

Limited free tier – SNS or API calls may cost more with heavy usage.

Difficult to debug – Must check CloudWatch logs for errors.


## Conclusion

This system provides automated, serverless weather notifications using AWS Lambda, SNS, and EventBridge. It is scalable, cost-effective, and requires no server management.
