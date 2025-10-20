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