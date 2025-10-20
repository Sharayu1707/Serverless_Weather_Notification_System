# Serverless_Weather_Notification_System

Overview

The Serverless Weather Notification System is an AWS-based application that fetches weather data from an external API and sends notifications (via email or SMS) using AWS services. It is designed to be fully serverless, leveraging AWS Lambda, SNS, and EventBridge.

Architecture

Components:

AWS Lambda: Executes code to fetch weather data.

Amazon SNS (Simple Notification Service): Sends notifications to subscribers.

Amazon EventBridge (CloudWatch Events): Schedules Lambda functions periodically.

API Service: Provides weather data (like OpenWeatherMap API).

Flow:

EventBridge triggers Lambda on a schedule (e.g., every morning).

Lambda fetches weather data from the API.

Lambda publishes the weather update to an SNS topic.

SNS sends notifications to subscribed users via email or SMS.

Prerequisites

AWS account with proper permissions

Node.js or Python installed (depending on Lambda code)

Weather API key (e.g., OpenWeatherMap)

Step-by-Step Setup
Step 1: Create an SNS Topic

Go to AWS SNS Console.

Click Create Topic → Choose Standard → Enter WeatherAlerts as the topic name.

Note the ARN (e.g., arn:aws:sns:ap-south-1:123456789012:WeatherAlerts).

Step 2: Subscribe to the Topic

In the SNS Topic, click Create Subscription.

Choose protocol:

Email → Enter your email address.

SMS → Enter your phone number.

Confirm the subscription via the link sent to your email or SMS.

Step 3: Create a Lambda Function

Go to AWS Lambda Console → Click Create Function.

Choose Author from scratch → Name: WeatherNotifier.

Runtime: Python 3.11 or Node.js 18.x.

Permissions:

Attach policy: AWSLambdaBasicExecutionRole.

Attach policy: AmazonSNSFullAccess (or least privilege to publish to SNS).

Step 4: Add Lambda Code

Python Example:

import json
import requests
import boto3

SNS_ARN = 'arn:aws:sns:ap-south-1:123456789012:WeatherAlerts'
API_KEY = 'YOUR_API_KEY'
CITY = 'Mumbai'

def lambda_handler(event, context):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    weather_desc = data['weather'][0]['description']
    temp = data['main']['temp']

    message = f"Weather Update for {CITY}:\nTemperature: {temp}°C\nDescription: {weather_desc}"

    sns = boto3.client('sns')
    sns.publish(TopicArn=SNS_ARN, Message=message, Subject='Daily Weather Update')

    return {
        'statusCode': 200,
        'body': json.dumps('Notification Sent!')
    }


⚠️ Update SNS_ARN, API_KEY, and CITY with your values.

Step 5: Configure EventBridge Trigger

Go to Amazon EventBridge → Rules → Create Rule.

Select Schedule → Set cron or rate (e.g., every day at 8 AM).

Choose target: Lambda function (WeatherNotifier).

Save rule.

Step 6: Test Lambda

Go to Lambda → Test → Configure test event.

Use default JSON ({}) → Click Test.

Check your email or SMS for the weather update.

Optional Enhancements

Use DynamoDB to log daily weather notifications.

Add multiple cities support.

Add HTML email formatting.

Troubleshooting

Status: Failed → Check Lambda CloudWatch Logs for errors.

Permission Denied → Ensure Lambda has proper SNS publish permissions.

No notifications → Ensure SNS subscriptions are confirmed.

Conclusion

This system provides automated, serverless weather notifications using AWS. It is scalable, cost-effective, and requires no server management.
