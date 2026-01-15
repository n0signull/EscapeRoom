import logging

class OutputManager:
    """
    Manages all physical puzzle outputs.

    This class translates high-level puzzle states into concrete
    hardware actions such as LEDs, relays, solenoids, or sound cues.
    """

    def update(self, state):
        """
        Update physical outputs based on the current puzzle state.

        In a real installation, this method would control GPIO pins,
        relays, or DMX channels. For now, it logs intended behavior.
        """

        # Puzzle is idle / locked
        if state == "LOCKED":
            # Example: Red LED ON, door locked, reset indicators
            logging.info("Outputs: LOCKED (LED RED)")

        # Puzzle has started and is accepting inputs
        elif state == "IN_PROGRESS":
            # Example: Yellow LED ON, progress indicators active
            logging.info("Outputs: IN PROGRESS (LED YELLOW)")

        # Puzzle completed successfully
        elif state == "SOLVED":
            # Example: Green LED ON, door unlock relay engaged
            logging.info("Outputs: SOLVED (LED GREEN / Relay ON)")
