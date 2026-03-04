from flask import Flask, render_template, request

app = Flask(__name__)

EMERGENCY_KEYWORDS = ["chest pain", "breathing", "unconscious", "bleeding", "stroke", "heart"]
MEDIUM_KEYWORDS = ["fever", "vomiting", "headache", "infection", "pain", "cough"]

def calculate_risk(symptoms, age, history):
    score = 0
    symptoms = symptoms.lower()

    for word in EMERGENCY_KEYWORDS:
        if word in symptoms:
            score += 5

    for word in MEDIUM_KEYWORDS:
        if word in symptoms:
            score += 3

    if age >= 60:
        score += 2

    if history == "yes":
        score += 2

    return score

def classify(score):
    if score >= 7:
        return "🚨 HIGH RISK", "Immediate medical attention required."
    elif score >= 4:
        return "⚠️ MEDIUM RISK", "Medical consultation recommended soon."
    else:
        return "✅ LOW RISK", "Condition appears non-urgent."

@app.route("/", methods=["GET", "POST"])
def index():
    result = advice = None

    if request.method == "POST":
        symptoms = request.form["symptoms"]
        age = int(request.form["age"])
        history = request.form["history"]

        score = calculate_risk(symptoms, age, history)
        result, advice = classify(score)

    return render_template("index.html", result=result, advice=advice)

if __name__ == "__main__":
    app.run(debug=True)