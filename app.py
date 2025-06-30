## === app.py ===
from flask import Flask, render_template, request
from services.ipapi_service import get_ipapi_data as scan_ip
from services.abuseipdb_service import get_abuseipdb_data
from services.shodan_service import get_shodan_data
from services.email_service import send_report_email, init_mail
from services.log_service import save_full_log
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
init_mail(app)

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
                ipapi_result = scan_ip(ip)
                abuseipdb_result = get_abuseipdb_data(ip)
                shodan_result = get_shodan_data(ip)

                if email:
                    try:
                        send_report_email(email, ipapi_result, abuseipdb_result, shodan_result)
                        message = f"📧 Rapport envoyé à {email}"
                    except Exception as e:
                        message = f"❌ Erreur email : {e}"

                save_full_log(
                    email=email,
                    user_ip=user_ip,
                    scanned_ip=ip,
                    ipapi_data=ipapi_result,
                    abuseipdb_data=abuseipdb_result,
                    shodan_data=shodan_result
                )

            except Exception as e:
                message = f"❌ Erreur lors du scan : {e}"

    return render_template("index.html",
        ipapi_result=ipapi_result,
        abuseipdb_result=abuseipdb_result,
        shodan_result=shodan_result,
        message=message
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)