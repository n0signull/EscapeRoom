import os

SIMULATION = os.getenv("SIMULATION_MODE", "true").lower() == "true"

class InputManager:
    def __init__(self):
        self.simulated_inputs = set()

    def any_active(self):
        return bool(self.simulated_inputs)

    def check(self, input_name, action):
        return input_name in self.simulated_inputs

    # Simulation helper
    def trigger(self, input_name):
        self.simulated_inputs.add(input_name)

    def clear(self):
        self.simulated_inputs.clear()
