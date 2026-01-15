from flask import Flask, jsonify, request
from controller.main import engine, inputs  # your PuzzleEngine and InputManager instances

app = Flask(__name__)

@app.route("/status")
def status():
    # Return puzzle state and current step info
    step_info = {}
    if engine.state == "IN_PROGRESS":
        # Get current step config
        step = engine.config["sequence"][engine.current_step]
        step_info["current_step_type"] = step.get("type", "input")
        if step.get("type") == "math":
            step_info["question"] = step["question"]
        else:
            step_info["question"] = ""
    else:
        step_info["current_step_type"] = ""
        step_info["question"] = ""

    return jsonify({
        "state": engine.state,
        "step": engine.current_step,
        **step_info
    })

@app.route("/submit_math", methods=["POST"])
def submit_math():
    data = request.get_json()
    answer = data.get("answer")
    if answer is not None:
        # Pass answer to InputManager for engine to process
        inputs.submit_math_answer(answer)
    return jsonify({"status": "ok"})

@app.route("/reset")
def reset():
    engine.reset()
    return jsonify({"status": "ok"})

@app.route("/solve")
def solve():
    engine.solve()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
