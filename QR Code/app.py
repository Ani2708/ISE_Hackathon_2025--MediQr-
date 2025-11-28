from flask import Flask, request, render_template

app = Flask(__name__)

# Sample patient data (you can replace with database later)
patients = {
    "PATIENT-8349922": {
        "name": "Rahul Mehta",
        "age": 42,
        "blood": "O+",
        "allergy": "Penicillin",
        "emergency_contact": "+91-9876543210",
        "prescriptions": ["Metformin 500mg daily"]
    }
}

@app.route("/patient")
def patient_page():
    pid = request.args.get("id")
    data = patients.get(pid)
    if data:
        return render_template("patient.html", data=data)
    else:
        return "Patient not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

