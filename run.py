import threading
from controller.main import loop
from web.app import app

# ----------------------------------
# Start puzzle controller in background
# ----------------------------------
# The puzzle engine runs in its own thread so it can continuously
# process inputs and state changes without blocking the web server.
#
# Setting daemon=True ensures the thread shuts down cleanly
# when the main application exits.
threading.Thread(target=loop, daemon=True).start()

# ----------------------------------
# Start web operator interface
# ----------------------------------
# This launches the Flask web server used by operators to:
# - Monitor puzzle state
# - Reset or force-solve puzzles
# - Debug issues remotely
#
# The web server runs on the main thread while the puzzle logic
# runs concurrently in the background.
#
# use_reloader=False is required to prevent Flask from spawning
# multiple processes, which would interfere with hardware control.
app.run(
    host="0.0.0.0",   # Expose server to local network
    port=5000,        # Standard control port
    debug=False,      # Disable debug mode for production safety
    use_reloader=False
)
