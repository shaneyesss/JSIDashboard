from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

def calculate_no_show_risk(prior_no_shows, lead_time_days,
                           insurance_type, appt_time, distance, age_group):
    score = 0
    reasons = []

    # insurance weights
    insurance_weights = {
        "private": 0,
        "public": 1,
        "uninsured": 3,
    }

    # 1. Prior no-shows
    if prior_no_shows >= 2:
        score += 3
        reasons.append("multiple prior missed appointments")
    elif prior_no_shows == 1:
        score += 2
        reasons.append("one prior missed appointment")

    # 2. Lead time
    if lead_time_days > 21:
        score += 2
        reasons.append("long scheduling delay")
    elif lead_time_days >= 7:
        score += 1
        reasons.append("moderate scheduling delay")

    # 3. Insurance type
    score += insurance_weights.get(insurance_type, 0)
    if insurance_type == "uninsured":
        reasons.append("uninsured status")
    elif insurance_type == "public":
        reasons.append("public insurance")
    elif insurance_type == "private":
        reasons.append("private insurance")

    # 4. Appointment time
    if appt_time == "morning":
        score += 1
        reasons.append("morning appointment")

    # 5. Distance from clinic
    if distance == "far":
        score += 2
        reasons.append("far distance from clinic")
    elif distance == "moderate":
        score += 1
        reasons.append("moderate distance from clinic")

    # 6. Age group
    if age_group == "young":
        score += 1
        reasons.append("younger age group")

    # Risk classification
    if score >= 8:
        risk = "High"
    elif score >= 4:
        risk = "Medium"
    else:
        risk = "Low"

    return score, risk, reasons


@app.route("/landing")
def landing():
    landing_template = Path(app.template_folder or "templates") / "landing.html"
    if landing_template.exists():
        return render_template("landing.html")
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        def parse_non_negative_int(value, default=0):
            try:
                return max(0, int(str(value).strip()))
            except (TypeError, ValueError):
                return default

        # Input validation with safe defaults for backward compatibility.
        prior_no_shows = parse_non_negative_int(request.form.get("prior_no_shows"), 0)
        lead_time_days = parse_non_negative_int(request.form.get("lead_time"), 0)
        age_raw = str(request.form.get("age", "0")).strip().lower()

        insurance_type = request.form.get("insurance_type", "private")
        appt_time = request.form.get("appt_time", "afternoon")
        distance = request.form.get("distance", "near")
        if age_raw in {"young", "middle", "older"}:
            # Backward compatibility for older age-group form submissions.
            age_group = age_raw
        else:
            age = parse_non_negative_int(age_raw, 0)
            if age < 35:
                age_group = "young"
            elif age < 65:
                age_group = "middle"
            else:
                age_group = "older"

        score, risk, reasons = calculate_no_show_risk(
            prior_no_shows,
            lead_time_days,
            insurance_type,
            appt_time,
            distance,
            age_group
        )

        insurance_labels = {
            "private": "Private Insurance",
            "public": "Public Insurance",
            "uninsured": "Uninsured",
        }
        appt_time_labels = {
            "morning": "Morning",
            "afternoon": "Afternoon",
            "evening": "Evening",
        }
        distance_labels = {
            "near": "Near (0-5 miles)",
            "moderate": "Moderate (5-15 miles)",
            "far": "Far (15+ miles)",
        }
        age_group_labels = {
            "young": "Young",
            "middle": "Middle",
            "older": "Older",
        }
        selected_choices = {
            "Prior No-Shows": prior_no_shows,
            "Lead Time (days)": lead_time_days,
            "Insurance Type": insurance_type.title(),
            "Appointment Time": appt_time.title(),
            "Distance from Clinic": distance.title(),
            "Age Group": age_group.title()
        }

        return render_template(
            "index.html",
            score=score,
            risk=risk,
            reasons=reasons,
            selected_choices=selected_choices
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)