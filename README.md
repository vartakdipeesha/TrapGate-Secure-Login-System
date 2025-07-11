# TrapGate-Secure-Login-System

I built secure login system inspired by real-world platforms like AWS and GitHub, featuring OTP-based authentication, email verification using AWS SNS, blocklist protection, and a custom Flask backend. Designed with cloud security principles and real-time alerts for suspicious activity.

## 1. System Architecture & Tools

### 1.1 Architecture Diagram

<img width="1024" height="1536" alt="flow" src="https://github.com/user-attachments/assets/936b2f12-2a80-43ac-b001-e95b0125ce5b" />

#### Flow Summary:

1. The user initiates a login request.
2. Flask backend verifies credentials from users.json.
3. If valid, it triggers an email verification request using AWS SNS.
4. User approves login via email → OTP is generated and emailed.
5. OTP is validated via session.
6. If incorrect 3 times → user is blocklisted.
7. All events logged + alerts are sent for suspicious activity.

### 1.2 Technologies & Tools Used

| Tool/Tech              | Purpose                                                           |
| ---------------------- | ----------------------------------------------------------------- |
| **Python (Flask)**     | Backend framework for handling routes, sessions, and server logic |
| **AWS SNS**            | Sends real-time OTPs and alert emails                             |
| **HTML + Jinja2**      | Front-end rendering of login, OTP, and dashboard pages            |
| **JSON Files**         | Lightweight storage for credentials, OTP, and denylist            |
| **boto3 (AWS SDK)**    | Python interface to interact with AWS services                    |
| **Session Management** | To handle OTP timeouts and user session tracking                  |
| **Linux/Terminal**     | Local hosting and running the Flask app                           |

## 2. Installation Guide + AWS SNS Setup

This section provides a step-by-step guide to install, configure, and run the TrapGate Secure Login System. 

It includes:

1. Setting up your local environment
2. Installing dependencies
3. Creating and configuring AWS SNS for OTP/alert emails

### 2.1 Environment Setup

#### Pre-Requisites:

1. Python 3.x installed
2. AWS account (with SNS permissions)
3. Email access for receiving OTP/alerts

### 2.2 Install Required Python Libraries

Install Flask and boto3 (AWS SDK for Python):

```ruby
pip install flask boto3
```

### 2.3 AWS SNS Setup (for OTP and Alert Emails)

You’ll be using Amazon SNS (Simple Notification Service) to send OTPs and alerts. 

#### Below are the detailed steps:

##### Step 1: 

1. Go to AWS Console → SNS → Topics
2. Click Create topic
3. Choose Standard
4. Name it: trapgate-alerts
5. Save your Topic ARN

##### Step 2: Create an Email Subscription

1. Go to Subscriptions → Click Create subscription
2. Protocol: Email
3. Endpoint: enter the email where you want to receive OTP/alerts
4. Click Create Subscription

<img width="1440" height="798" alt="AWS_SNS_2" src="https://github.com/user-attachments/assets/78a60d20-b3e0-42b9-b694-dd77b05ebc71" />

<img width="1440" height="789" alt="AWS_SNS_1" src="https://github.com/user-attachments/assets/88b739da-66d1-43a0-a4ff-ec12c20b73d0" />

*I have hide the details in ss for security purposes.*

### 3. Launching the Application

Run the Flask server using:
```ruby
python app.py
```

Server will start at http://127.0.0.1:5000

Navigate to that URL in your browser to see the TrapGate login screen

### 4. Screenshots 

#### 4.1 Successful Login

##### Steps:
1.	User enters correct email and password.
2.	A security email is sent:<br>
    	Shows 2 links: <br>
	     It was me → Approves login <br>
	     Block → Blocks login <br>
3.	User clicks *It was me*: <br>
	       OTP is generated and sent to their email. <br>
         OTP page opens in browser. <br>
4.	User enters correct OTP.
5.	User is redirected to dashboard.html (successful login).


![WhatsApp Image 2025-07-11 at 18 56 10](https://github.com/user-attachments/assets/8fb8bfc4-43b5-4952-b422-1f41747f907f)
![WhatsApp Image 2025-07-11 at 18 56 12](https://github.com/user-attachments/assets/1cf48451-bbb7-47bb-a7bf-dc5d26dbb664)

Apporved:

![WhatsApp Image 2025-07-11 at 18 56 12 (1)](https://github.com/user-attachments/assets/31af0683-76f1-4206-9f2a-c5672ebffa9e)

Blocked:
<img width="1280" height="781" alt="image" src="https://github.com/user-attachments/assets/b60e4df3-8ffb-42a2-8df3-671f067d94a7" />

![WhatsApp Image 2025-07-11 at 18 56 12 (2)](https://github.com/user-attachments/assets/e4da86ea-3d22-49af-80f7-0d316a61af25)
<img width="1600" height="661" alt="image" src="https://github.com/user-attachments/assets/39613a54-941e-4040-89f6-643ae47459b5" />
![WhatsApp Image 2025-07-11 at 18 56 12 (3)](https://github.com/user-attachments/assets/cb64d1a2-26a7-411b-81e6-90a9b8eae81e)

*I have hide the details in ss for security purposes.*

#### 4.1 Suspicious Login Attempt (Wrong Password)

##### Steps:
1.	User enters email but incorrect password.
2.	send_alert() is triggered – alert email/SNS sent.
3.	User tries again with wrong password.
4.	After 3rd wrong attempt: Email is added to denylist.txt
6.	User is blocked permanently.

<img width="1600" height="651" alt="image" src="https://github.com/user-attachments/assets/76f11035-b0c0-4fdc-831e-83e20b00e02d" />

*I have hide the details in denylist.txt for security purpose*


#### 4.2 Login Attempt by Blocked User

##### Steps:
1.	Blocked user (in denylist) tries to log in.
2.	login.html shows: ACCESS DENIED
3.	Login button disabled.
4.	No further actions are allowed.

<img width="1280" height="490" alt="image" src="https://github.com/user-attachments/assets/64958231-9a9b-4b24-9bb6-ad2cfd5d417c" />

<img width="1280" height="503" alt="image" src="https://github.com/user-attachments/assets/31a305a8-05f3-4001-9cbf-ee74c66ea3ea" />

#### 4.3 OTP Timeout or Invalid OTP and Resend OTP

##### Steps:

1.	OTP email received.
2.	User opens OTP page but: <br>
	  Waits more than 2 minutes → “OTP expired” error OR enters wrong OTP → “Invalid OTP” error.
3.	After 3 wrong OTP attempts: Blocked from entering OTP again.
4.	On OTP page, user clicks "Resend OTP"
5.	New OTP sent to email.
6.	Timer resets to 2 minutes.

   <img width="1280" height="214" alt="image" src="https://github.com/user-attachments/assets/84e008e9-0cc8-4c23-9dfd-fd42cb93c8fe" />
   <img width="1280" height="854" alt="image" src="https://github.com/user-attachments/assets/1569a516-a3be-42a9-bb3f-15017e08abdd" />
   <img width="1280" height="646" alt="image" src="https://github.com/user-attachments/assets/523487a0-2e5d-47fc-a49a-1255489e70b6" />
   <img width="1280" height="638" alt="image" src="https://github.com/user-attachments/assets/51c6deaa-bcd4-4caa-9f10-730cb322b7c1" />
   <img width="1280" height="728" alt="image" src="https://github.com/user-attachments/assets/0d7db576-c787-47fb-adec-afc53105d2cd" />

## Final Reflection – A Learning Journey

Working on TrapGate has been a meaningful experience for me. As a student who’s still learning and growing in the field of cybersecurity, I took this project as an opportunity to explore how secure login systems function — beyond just theory, and with a real-world approach.

Throughout the process, I’ve gained hands-on exposure to:

1.Writing authentication logic from scratch.<br>
2.Integrating AWS SNS for real-time alerts.<br>
3.Designing a user flow that balances security with usability.<br>
4.Structuring code with clarity and modularity.<br>
5.Understanding the importance of proactive defense against suspicious behavior.<br>
6.This wasn’t just about building a login system — it was about developing a security mindset, one step at a time.

I know there’s still so much more to learn, and I look forward to improving this project with better practices, deeper integrations, and more advanced features in the future.

**“Every feature I added was a small lesson — and every challenge was a step toward becoming more thoughtful about security.”** <br>

## Thank you for taking the time to go through this project. <br> I hope TrapGate reflects not just my technical effort, but also my dedication and willingness to learn.












