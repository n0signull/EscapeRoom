import yaml
import time
import logging

# Core puzzle engine and I/O managers
from controller.puzzle import PuzzleEngine
from controller.inputs import InputManager
from controller.outputs import OutputManager

# Configure global logging level
# In production, this could be redirected to a file for remote debugging
logging.basicConfig(level=logging.INFO)

# ----------------------------------
# Load puzzle configuration
# ----------------------------------
# Configuration defines puzzle sequence, timeouts, and input mapping
with open("controller/config.yaml") as f:
    config = yaml.safe_load(f)

# ----------------------------------
# Initialize hardware interfaces
# ----------------------------------
# InputManager handles buttons, sensors, switches, etc.
inputs = InputManager()

# OutputManager controls LEDs, relays, locks, etc.
outputs = OutputManager()

# Create puzzle engine using config and I/O abstractions
engine = PuzzleEngine(config, inputs, outputs)

def loop():
    """
    Main control loop.

    Continuously polls puzzle state and inputs,
    advancing puzzle logic as conditions are met.
    This loop would typically run as a background service
    on a Raspberry Pi or embedded controller.
    """
    while True:
        # Process puzzle logic and state transitions
        engine.update()

        # Small delay to prevent excessive CPU usage
        time.sleep(0.1)
