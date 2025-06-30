## === services/email_service.py ===
from flask_mail import Mail, Message
import os

mail = Mail()

def init_mail(app):
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
    mail.init_app(app)

def send_report_email(to_email, ipapi, abuseipdb, shodan):
    msg = Message("Rapport de surveillance d'IP", recipients=[to_email])
    msg.body = f"""
Résultats :

[IP-API]
{ipapi}

[AbuseIPDB]
{abuseipdb}

[Shodan]
{shodan}
    """
    mail.send(msg)