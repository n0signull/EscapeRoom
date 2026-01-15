import time
import logging

# Defines high-level puzzle states
class PuzzleState:
    LOCKED = "LOCKED"           # Puzzle is inactive / waiting for first interaction
    IN_PROGRESS = "IN_PROGRESS" # Puzzle is currently being solved
    SOLVED = "SOLVED"           # Puzzle has been completed successfully

class PuzzleEngine:
    """
    Core puzzle logic engine.

    This class manages puzzle state, timing, step progression,
    and interaction between physical inputs and outputs.
    It is designed to be hardware-agnostic and driven by configuration.
    """

    def __init__(self, config, inputs, outputs):
        # Puzzle configuration dictionary
        # Expected keys:
        # - sequence: ordered list of steps
        # - timeout: total allowed puzzle time
        self.config = config

        # Input interface (buttons, sensors, switches, etc.)
        # Expected to expose methods like any_active() and check()
        self.inputs = inputs

        # Output interface (relays, LEDs, locks, etc.)
        # Expected to expose update(state)
        self.outputs = outputs

        # Initialize puzzle to safe default state
        self.reset()

    def reset(self):
        """
        Reset the puzzle to its initial locked state.
        Clears progress, timers, and updates outputs to reflect
        that the puzzle is inactive.
        """
        self.state = PuzzleState.LOCKED
        self.current_step = 0
        self.step_start_time = None
        self.puzzle_start_time = None

        # Update physical outputs (e.g. lock door, reset indicators)
        self.outputs.update(self.state)

        logging.info("Puzzle reset")

    def solve(self):
        """
        Force the puzzle into a solved state.

        Used for operator override, accessibility, or emergency bypass.
        """
        self.state = PuzzleState.SOLVED
        self.outputs.update(self.state)
        logging.info("Puzzle force-solved")

    def update(self):
        """
        Main puzzle update loop.

        This method should be called repeatedly (e.g. in a game loop
        or scheduler). It evaluates player input, enforces timeouts,
        and advances puzzle state.
        """

        # No further processing once puzzle is solved
        if self.state == PuzzleState.SOLVED:
            return

        now = time.time()

        # -----------------------------
        # LOCKED STATE
        # -----------------------------
        # Puzzle is waiting for any player interaction
        if self.state == PuzzleState.LOCKED:
            if self.inputs.any_active():
                # First interaction starts the puzzle
                self.state = PuzzleState.IN_PROGRESS
                self.puzzle_start_time = now
                self.step_start_time = now
                logging.info("Puzzle started")

        # -----------------------------
        # IN_PROGRESS STATE
        # -----------------------------
        elif self.state == PuzzleState.IN_PROGRESS:

            # Check overall puzzle timeout
            if now - self.puzzle_start_time > self.config["timeout"]:
                logging.warning("Puzzle timeout")
                self.reset()
                return

            # Get the current step configuration
            step = self.config["sequence"][self.current_step]

            # Check whether the expected input/action for this step occurred
            if self.inputs.check(step["input"], step["action"]):
                logging.info(f"Step {self.current_step + 1} correct")

                # Advance to the next step
                self.current_step += 1
                self.step_start_time = now

                # If all steps are completed, solve the puzzle
                if self.current_step >= len(self.config["sequence"]):
                    self.state = PuzzleState.SOLVED
                    self.outputs.update(self.state)
                    logging.info("Puzzle solved!")

            # If the correct input was not received in time, reset puzzle
            else:
                if now - self.step_start_time > step["max_delay"]:
                    logging.warning("Step timeout")
                    self.reset()
