from flask import Flask, render_template, request, flash
from services.scanner_core import scan_ip
from services.email_service import init_mail, send_report_email
from dotenv import load_dotenv
import os
from services.log_service import save_full_log

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")

init_mail(app)

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

# ✅ Lancement compatible Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
