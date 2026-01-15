# Import Flask and helper functions
from flask import Flask, jsonify, render_template
# Import the PuzzleEngine instance from your controller
from controller.main import engine

# ------------------------------------------
# Initialize Flask application
# ------------------------------------------
# This creates the web server that will serve the HTML interface
# and handle API endpoints for interacting with the puzzle engine.
app = Flask(__name__)

# ------------------------------------------
# Route: Serve the main dashboard page
# ------------------------------------------
# When a user navigates to "/", this function serves the HTML page
# where operators can monitor puzzle state and interact with it.
@app.route("/")
def index():
    return render_template("dashboard.html")  # looks in the 'templates/' folder by default

# ------------------------------------------
# Route: Get current puzzle status
# ------------------------------------------
# This endpoint is called by the front-end (JavaScript) every second
# to update the puzzle state and the current step number.
@app.route("/status")
def status():
    return jsonify({
        "state": engine.state,          # Current puzzle state: LOCKED, IN_PROGRESS, SOLVED
        "step": engine.current_step     # Index of the current puzzle step
    })

# ------------------------------------------
# Route: Reset the puzzle
# ------------------------------------------
# When this endpoint is called (e.g., by the "Reset" button),
# the puzzle engine resets to its initial locked state.
@app.route("/reset")
def reset():
    engine.reset()  # Reset puzzle state and timers
    return "OK"     # Return simple text response

# ------------------------------------------
# Route: Force-solve the puzzle
# ------------------------------------------
# When called (e.g., by the "Force Solve" button), the puzzle
# immediately transitions to the solved state regardless of progress.
@app.route("/solve")
def solve():
    engine.solve()  # Force puzzle into solved state
    return "OK"     # Return simple text response
