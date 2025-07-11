from datetime import datetime

def log_attempt(email, ip):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("attack_logs.txt", "a") as file:
        file.write(f"{now} | Email: {email} | IP: {ip}\n")
