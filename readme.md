# No-Show Risk Predictor

## Overview

This is a Flask-based web application that predicts the likelihood of a patient missing a scheduled medical appointment. The model uses a simple weighted scoring system based on commonly identified predictors in healthcare literature.

---

## Features

* Input multiple patient and appointment characteristics
* Calculates a risk score based on weighted factors
* Classifies patients into **Low**, **Medium**, or **High** no-show risk
* Displays:

  * Risk score
  * Risk level
  * Selected inputs
  * Contributing risk factors ("reasons")
* Clean, styled web interface
* Includes an informational landing/about page

---

## Variables Used

The model incorporates the following predictors:

* **Prior No-Shows**
  Captures historical attendance behavior (strongest predictor)

* **Lead Time (days)**
  Time between scheduling and appointment

* **Insurance Type**

  * Private
  * Public
  * Uninsured

* **Appointment Time**

  * Morning
  * Afternoon
  * Evening

* **Distance from Clinic**

  * Near (0–5 miles)
  * Moderate (5–15 miles)
  * Far (15+ miles)

* **Age**
  Automatically categorized into:

  * Young (18–34)
  * Middle (35–64)
  * Older (65+)

---

## Scoring Logic

Each variable contributes to a total risk score using a weighted system:

* Prior no-shows and lead time are the strongest contributors
* Insurance and distance represent access-related factors
* Appointment time and age are secondary predictors

### Risk Classification

* **Low Risk:** 0–4
* **Medium Risk:** 5–7
* **High Risk:** 8+

---

## How to Run

### 1. Install dependencies

```bash
pip install flask
```

### 2. Run the application

```bash
python app.py
```

### 3. Open in browser

```
http://127.0.0.1:5000/
```

---

## Project Structure

```
no-show-predictor/
│
├── app.py
├── templates/
│   ├── index.html
│   └── landing.html (optional)
```

---

## Notes

* This is an **educational prototype**
* The scoring model is **not clinically validated**
* Weights are derived from general trends in literature, not trained on real patient data