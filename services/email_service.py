import os
from flask_mail import Mail, Message
from flask import current_app
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    mail.init_app(app)

def send_report_email(recipient, ip, result):
    subject = f"Rapport ThreatTrace AI pour {ip}"
    body = f"""
📊 Rapport de sécurité pour l'IP {ip} :

🌍 IP-API :
{result.get('ipapi', {})}

🛡️ AbuseIPDB :
{result.get('abuseipdb', {})}

📍 Google Maps :
{result.get('ipapi', {}).get('google_maps_link', 'Non disponible')}
    """
    msg = Message(subject=subject, recipients=[recipient], body=body)
    with current_app.app_context():
        mail.send(msg)
