#
#from flask import Flask, render_template, request, session, redirect
#from logger import log_attempt
#from alert import send_alert, send_otp_email, send_intrusion_decision_email
#import random
#import time
#import json
#
#app = Flask(__name__)
#app.secret_key = "trapgate_secret"
#
## Track login attempts
#attempt_tracker = {}
## Track approvals
#approved_users = set()
#
## Load users from JSON
#def load_users():
#    try:
#        with open("users.json", "r") as f:
#            return json.load(f)
#    except:
#        return {}
#
#def log_otp_result(email, status):
#    print(f"[OTP Log] {email}: {status}")
#
## Check blocklist
#def is_denied(email, ip):
#    try:
#        with open("denylist.txt", "r") as f:
#            denied = f.read().splitlines()
#            return email in denied or ip in denied
#    except FileNotFoundError:
#        return False
#
## Add to blocklist
#def add_to_denylist(entry):
#    with open("denylist.txt", "a") as f:
#        f.write(entry + "\n")
#
#@app.route('/')
#def index():
#    email = session.get("email", "")
#    blocked = False
#    try:
#        with open("denylist.txt", "r") as f:
#            if email in f.read():
#                blocked = True
#    except:
#        pass
#    return render_template("login.html", blocked=blocked, email=email)
#
#@app.route('/trap', methods=['POST'])
#def trap():
#    email = request.form['email']
#    password = request.form['password']
#    ip = request.remote_addr
#    users = load_users()
#
#    # 🔒 Check if blocked
#    if is_denied(email, ip):
#        return render_template('login.html', blocked=True, email=email)
#
#    # ✅ CORRECT credentials
#    if email in users and users[email] == password:
#        session["email"] = email
#        session["ip"] = ip
#
#        # ✅ If already approved, send OTP directly
#        if email in approved_users:
#            otp = str(random.randint(100000, 999999))
#            session["otp"] = otp
#            session["otp_time"] = time.time()
#            session["otp_attempts"] = 0
#            print(f"[DEBUG] OTP for {email}: {otp}")
#            send_otp_email(email, otp)
#            return redirect('/otp')
#
#        # ⏳ Else, wait for confirmation
#        send_intrusion_decision_email(email, ip)
#        return render_template("login.html", warning="Confirmation email sent. Please verify if this was you.")
#
#    # ❌ WRONG credentials
#    if email in attempt_tracker:
#        attempt_tracker[email] += 1
#    else:
#        attempt_tracker[email] = 1
#
#    if attempt_tracker[email] > 2:
#        add_to_denylist(email)
#        return render_template("login.html", blocked=True, email=email)
#
#    remaining = 3 - attempt_tracker[email]
#    log_attempt(email, ip)
#    send_alert(email, ip)
#    return render_template("login.html", blocked=False, email=email, warning=f"{remaining} login attempt(s) left!")
#
#@app.route('/approve')
#def approve_login():
#    email = request.args.get('email')
#    session["email"] = email
#    approved_users.add(email)
#    return redirect("/send-otp")
#
#@app.route('/send-otp')
#def send_otp():
#    email = session.get("email")
#    if not email:
#        return redirect("/")
#    otp = str(random.randint(100000, 999999))
#    session["otp"] = otp
#    session["otp_time"] = time.time()
#    session["otp_attempts"] = 0
#    print(f"[DEBUG] OTP for {email}: {otp}")
#    send_otp_email(email, otp)
#    return redirect("/otp")
#
#@app.route('/block')
#def block_login():
#    email = request.args.get('email')
#    add_to_denylist(email)
#    return f"<h3>{email} has been BLOCKED. Added to denylist.</h3>"
#
#@app.route('/otp')
#def otp_page():
#    return render_template('otp_verification.html')
#
#@app.route('/verify-otp', methods=['POST'])
#def verify_otp():
#    email = session.get("email")
#    entered_otp = request.form.get("otp")
#    saved_otp = session.get("otp")
#    otp_time = session.get("otp_time")
#    session["otp_attempts"] = session.get("otp_attempts", 0) + 1
#
#    if session["otp_attempts"] > 2:
#        log_otp_result(email, "Blocked after 2 OTP tries")
#        return render_template("otp_verification.html", error="Too many failed OTP attempts.")
#
#    if not saved_otp or not otp_time:
#        return render_template("otp_verification.html", error="OTP expired. Please request again.")
#
#    if time.time() - otp_time > 120:
#        return render_template("otp_verification.html", error="OTP expired. Please click resend.")
#
#    if entered_otp == saved_otp:
#        log_otp_result(email, "OTP success")
#        return render_template("dashboard.html", email=email)
#    else:
#        log_otp_result(email, "OTP failed")
#        return render_template("otp_verification.html", error="Invalid OTP")
#
#@app.route('/resend-otp', methods=['POST'])
#def resend_otp():
#    email = session.get("email")
#    if not email:
#        return redirect("/")
#
#    otp = str(random.randint(100000, 999999))
#    session["otp"] = otp
#    session["otp_time"] = time.time()
#    session["otp_attempts"] = 0
#
#    print(f"[DEBUG] Resent OTP for {email}: {otp}")
#    send_otp_email(email, otp)
#    return render_template("otp_verification.html", error="A new OTP has been sent to your email.")
#
#if __name__ == '__main__':
#    app.run(debug=True)
from flask import Flask, render_template, request, session, redirect
from logger import log_attempt
from alert import send_alert, send_otp_email, send_intrusion_decision_email
import random
import time
import json

app = Flask(__name__)
app.secret_key = "trapgate_secret"

# Track login attempts
attempt_tracker = {}
# Track approvals
approved_users = set()

# Load users from JSON
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def log_otp_result(email, status):
    print(f"[OTP Log] {email}: {status}")

# Check blocklist
def is_denied(email, ip):
    try:
        with open("denylist.txt", "r") as f:
            denied = f.read().splitlines()
            return email in denied or ip in denied
    except FileNotFoundError:
        return False

# Add to blocklist
def add_to_denylist(entry):
    with open("denylist.txt", "a") as f:
        f.write(entry + "\n")

@app.route('/')
def index():
    session.clear()  # 💥 Clear old session so login always shows
    return render_template("login.html", blocked=False, email="")

@app.route('/trap', methods=['POST'])
def trap():
    email = request.form['email']
    password = request.form['password']
    ip = request.remote_addr
    users = load_users()

    # 🔒 Check if blocked
    if is_denied(email, ip):
        return render_template('login.html', blocked=True, email=email)

    # ✅ CORRECT credentials
    if email in users and users[email] == password:
        session["email"] = email
        session["ip"] = ip

        # ✅ Already approved: send OTP
        if email in approved_users:
            otp = str(random.randint(100000, 999999))
            session["otp"] = otp
            session["otp_time"] = time.time()
            session["otp_attempts"] = 0
            print(f"[DEBUG] OTP for {email}: {otp}")
            send_otp_email(email, otp)
            return redirect('/otp')

        # ⏳ Not approved yet: ask for confirmation
        send_intrusion_decision_email(email, ip)
        return render_template("login.html", warning="Confirmation email sent. Please verify if this was you.")

    # ❌ WRONG credentials
    attempt_tracker[email] = attempt_tracker.get(email, 0) + 1

    if attempt_tracker[email] > 2:
        add_to_denylist(email)
        return render_template("login.html", blocked=True, email=email)

    remaining = 3 - attempt_tracker[email]
    log_attempt(email, ip)
    send_alert(email, ip)
    return render_template("login.html", blocked=False, email=email, warning=f"{remaining} login attempt(s) left!")

@app.route('/approve')
def approve_login():
    email = request.args.get('email')
    session["email"] = email
    approved_users.add(email)
    return redirect("/send-otp")

@app.route('/send-otp')
def send_otp():
    email = session.get("email")
    if not email:
        return redirect("/")
    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    session["otp_time"] = time.time()
    session["otp_attempts"] = 0
    print(f"[DEBUG] OTP for {email}: {otp}")
    send_otp_email(email, otp)
    return redirect("/otp")

@app.route('/block')
def block_login():
    email = request.args.get('email')
    add_to_denylist(email)
    return f"<h3>{email} has been BLOCKED. Added to denylist.</h3>"

@app.route('/otp')
def otp_page():
    return render_template('otp_verification.html')

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = session.get("email")
    entered_otp = request.form.get("otp")
    saved_otp = session.get("otp")
    otp_time = session.get("otp_time")
    session["otp_attempts"] = session.get("otp_attempts", 0) + 1

    if session["otp_attempts"] > 2:
        log_otp_result(email, "Blocked after 2 OTP tries")
        return render_template("otp_verification.html", error="Too many failed OTP attempts.")

    if not saved_otp or not otp_time:
        return render_template("otp_verification.html", error="OTP expired. Please request again.")

    if time.time() - otp_time > 120:
        return render_template("otp_verification.html", error="OTP expired. Please click resend.")

    if entered_otp == saved_otp:
        log_otp_result(email, "OTP success")
        return render_template("dashboard.html", email=email)
    else:
        log_otp_result(email, "OTP failed")
        return render_template("otp_verification.html", error="Invalid OTP")

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    email = session.get("email")
    if not email:
        return redirect("/")

    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    session["otp_time"] = time.time()
    session["otp_attempts"] = 0

    print(f"[DEBUG] Resent OTP for {email}: {otp}")
    send_otp_email(email, otp)
    return render_template("otp_verification.html", error="A new OTP has been sent to your email.")

if __name__ == '__main__':
    app.run(debug=True)
