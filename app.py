# app.py

from flask import Flask, render_template, request
from services.ipapi_service import get_ipapi_data as scan_ip
from services.abuseipdb_service import get_abuseipdb_data
from services.shodan_service import get_shodan_info
from services.email_service import send_report_email, init_mail
from services.log_service import save_full_log
from dotenv import load_dotenv
import os

# Chargement des variables d’environnement (.env)
load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)
init_mail(app)  # Configuration du mail via Flask-Mail

@app.route("/", methods=["GET", "POST"])
def index():
    ipapi_result = {}
    abuseipdb_result = {}
    shodan_result = {}
    message = ""

    if request.method == "POST":
        ip = request.form.get("ip")
        email = request.form.get("email")
        user_ip = request.remote_addr

        if ip:
            try:
                # 🔍 Appels aux services d’analyse
                ipapi_result = scan_ip(ip)
                abuseipdb_result = get_abuseipdb_data(ip)
                shodan_result = get_shodan_info(ip)

                # 📧 Envoi du rapport par email (si fourni)
                if email:
                    try:
                        send_report_email(email, ipapi_result, abuseipdb_result, shodan_result)
                        message = f"📧 Rapport envoyé avec succès à {email}"
                    except Exception as e:
                        message = f"❌ Erreur lors de l'envoi de l'email : {e}"

                # 🧾 Enregistrement du log complet
                save_full_log(
                    email=email,
                    user_ip=user_ip,
                    scanned_ip=ip,
                    ipapi_data=ipapi_result,
                    abuseipdb_data=abuseipdb_result,
                    shodan_data=shodan_result
                )

            except Exception as e:
                message = f"❌ Une erreur est survenue : {e}"

    return render_template("index.html",
        ipapi_result=ipapi_result,
        abuseipdb_result=abuseipdb_result,
        shodan_result=shodan_result,
        message=message
    )

# 🔁 Démarrage compatible local et Railway (port dynamique)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
