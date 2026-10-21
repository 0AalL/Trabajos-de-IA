from flask import Flask, render_template, jsonify
import run_simulation
from flask import request
app = Flask(__name__)

RESULTS = None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run")
def run():
    global RESULTS

    num_patients = int(request.args.get("num_patients"))
    doctors = int(request.args.get("doctors"))

    RESULTS = run_simulation.main(num_patients, doctors)

    return jsonify({"status": "ok"})


@app.route("/results")
def results():
    return jsonify(RESULTS)


if __name__ == "__main__":
    app.run(debug=False)