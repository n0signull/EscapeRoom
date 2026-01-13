from flask import Flask, jsonify, render_template
from controller.main import engine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/status")
def status():
    return jsonify({
        "state": engine.state,
        "step": engine.current_step
    })

@app.route("/reset")
def reset():
    engine.reset()
    return "OK"

@app.route("/solve")
def solve():
    engine.solve()
    return "OK"
