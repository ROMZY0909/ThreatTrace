from flask import Flask, request, render_template
from flask_mail import Mail, Message
from report_gen import generate_summary
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement (.env)
load_dotenv()

app = Flask(__name__)

# Configuration de Flask-Mail via .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message_sent = False

    if request.method == 'POST':
        ip = request.form.get('ip')
        email = request.form.get('email')

        try:
            result = generate_summary(ip)

            # Envoi de l’email si une adresse est fournie
            if email:
                body = f"""
                Rapport ThreatTrace AI pour l'adresse IP : {ip}

                -- Résumé de l'analyse --

                ▸ IP-API:
                {result.get('ipapi', {})}

                ▸ AbuseIPDB:
                {result.get('abuseipdb', {})}

                ▸ Shodan:
                {result.get('shodan', {})}

                ▸ Résumé IA:
                {result.get('summary', '')}
                """

                msg = Message(
                    subject=f"[ThreatTrace AI] Rapport d’analyse IP - {ip}",
                    recipients=[email],
                    body=body
                )
                mail.send(msg)
                message_sent = True

        except Exception as e:
            result = {'error': f"Erreur lors de l’analyse : {str(e)}"}

    return render_template('index.html', result=result, message_sent=message_sent)

if __name__ == '__main__':
    app.run(debug=True)
