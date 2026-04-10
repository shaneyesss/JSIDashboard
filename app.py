
from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_no_show_risk(prior_no_shows, lead_time_days,
                           insurance_type, reminder_confirmed, age_group):
    score = 0
    reasons = []
    insurance_weights = {
        "private": 0,
        "public": 1,
        "uninsured": 2,
    }

    if prior_no_shows >= 2:
        score += 3
        reasons.append("multiple prior missed appointments")
    elif prior_no_shows == 1:
        score += 2
        reasons.append("one prior missed appointment")

    if lead_time_days > 21:
        score += 2
        reasons.append("long scheduling delay")
    elif lead_time_days >= 7:
        score += 1
        reasons.append("moderate scheduling delay")

    score += insurance_weights.get(insurance_type, 0)
    if insurance_type == "uninsured":
        reasons.append("uninsured status")
    elif insurance_type == "public":
        reasons.append("public insurance")

    if reminder_confirmed == "no":
        score += 2
        reasons.append("reminder not confirmed")

    if age_group == "young":
        score += 1
        reasons.append("younger age group")

    if score >= 6:
        risk = "High"
    elif score >= 3:
        risk = "Medium"
    else:
        risk = "Low"

    return score, risk, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prior_no_shows = int(request.form["prior_no_shows"])
        lead_time_days = int(request.form["lead_time"])
        insurance_type = request.form["insurance_type"]
        reminder = request.form["reminder"]
        age_group = request.form["age"]

        score, risk, reasons = calculate_no_show_risk(
            prior_no_shows, lead_time_days,
            insurance_type, reminder, age_group
        )

        return render_template("index.html",
                               score=score,
                               risk=risk,
                               reasons=reasons)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)