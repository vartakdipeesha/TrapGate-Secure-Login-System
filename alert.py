import boto3

# Alert for suspicious login attempt
def send_alert(email, ip):
    client = boto3.client('sns', region_name='YOUR REGION NAME') # Initialize AWS SNS client. Replace 'YOUR REGION NAME' with your AWS region (e.g., 'us-east-1')

    message = f"""
 TrapGate Alert!

Unauthorized login attempt detected:
Email: {email}
IP Address: {ip}
"""

    try:
        response = client.publish(
            TopicArn='YOUR TOPIC ARN',
            Message=message,
            Subject='[TrapGate] Unauthorized Login Alert'
        )
        print("Alert sent:", response['MessageId'])
    except Exception as e:
        print("Error sending alert:", e)


#  Send OTP to user
def send_otp_email(email, otp):
    client = boto3.client('sns', region_name='YOUR REGION NAME')

    message = f"""
Your TrapGate OTP: {otp}

This OTP is valid for 2 minutes. Do not share it.
"""

    try:
        response = client.publish(
            TopicArn='YOUR TOPIC ARN',# Replace 'YOUR TOPIC ARN' with the actual ARN of your AWS SNS topic (found in the AWS SNS dashboard)
            Message=message,
            Subject='TrapGate OTP Verification Code'
        )
        print(" OTP sent:", response['MessageId'])
    except Exception as e:
        print(" Error sending OTP:", e)


#  Let user decide: was it them or not?
def send_intrusion_decision_email(email, ip):
    client = boto3.client('sns', region_name='YOUR REGION NAME')

    message = f"""
 Suspicious Login Detected!!!

Email: {email}
IP: {ip}

If this was YOU:
👉 http://127.0.0.1:5000/approve?email={email}

If NOT you:
🛑 http://127.0.0.1:5000/block?email={email}
"""

    try:
        response = client.publish(
            TopicArn='YOUR TOPIC ARN',
            Message=message,
            Subject='[TrapGate] Approve or Block Login'
        )
        print(" Decision alert sent:", response['MessageId'])
    except Exception as e:
        print("Error sending decision email:", e)
