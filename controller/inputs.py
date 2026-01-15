import os

# Flag to determine whether the system is running in simulation mode.
# When enabled, inputs are manually triggered in software instead of
# coming from physical hardware (GPIO, sensors, switches, etc.).
SIMULATION = os.getenv("SIMULATION_MODE", "true").lower() == "true"


class InputManager:
    """
    Manages all puzzle input sources.

    In simulation mode, inputs are triggered programmatically.
    In production, this class can be extended to listen to
    real hardware inputs such as buttons, reed switches, or sensors.
    """

    def __init__(self):
        # Stores currently active simulated inputs
        self.simulated_inputs = set()

    def any_active(self):
        """
        Check whether any input is currently active.

        Used to determine when the puzzle should transition
        from LOCKED to IN_PROGRESS.
        """
        return bool(self.simulated_inputs)

    def check(self, input_name, action):
        """
        Check whether a specific input/action condition has been met.

        Parameters:
        - input_name: identifier for the input device
        - action: expected action (press, toggle, hold, etc.)
                 Included for future expansion and hardware parity
        """
        return input_name in self.simulated_inputs

    # -----------------------------
    # Simulation helper methods
    # -----------------------------

    def trigger(self, input_name):
        """
        Simulate activation of an input.

        Useful for testing puzzle logic without physical hardware.
        """
        self.simulated_inputs.add(input_name)

    def clear(self):
        """
        Clear all active simulated inputs.

        Typically called after step completion or puzzle reset.
        """
        self.simulated_inputs.clear()
