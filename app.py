from flask import Flask, render_template, request, flash
from services.scanner_core import scan_ip
from services.email_service import init_mail, send_report_email
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")

# Initialisation du service de mail
init_mail(app)

# Route principale : page d’accueil et formulaire
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        ip = request.form.get("ip")
        email = request.form.get("email")

        print(f"[📩] Requête reçue : IP = {ip}, Email = {email or 'non fourni'}")

        if not ip:
            flash("⛔ Adresse IP requise", "error")
        else:
            # Appel au module scanner principal
            result = scan_ip(ip)
            flash("✅ Analyse terminée", "success")

            if email:
                try:
                    send_report_email(email, ip, result)
                    flash(f"📧 Rapport envoyé à {email}", "success")
                except Exception as e:
                    print(f"[ERREUR ENVOI MAIL] {e}")
                    flash("⚠️ Échec de l’envoi du mail", "error")

    return render_template("index.html", result=result)

# Lancement du serveur
if __name__ == "__main__":
    app.run(debug=True)
