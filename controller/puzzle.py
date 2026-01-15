import time
import logging

# High-level puzzle states
class PuzzleState:
    LOCKED = "LOCKED"           # puzzle inactive
    IN_PROGRESS = "IN_PROGRESS" # puzzle being solved
    SOLVED = "SOLVED"           # puzzle completed

class PuzzleEngine:
    """
    Core puzzle logic engine.

    Manages puzzle state, step progression, timeouts, and special game logic.
    This version adds support for math steps.
    """

    def __init__(self, config, inputs, outputs):
        self.config = config
        self.inputs = inputs
        self.outputs = outputs
        self.reset()

    def reset(self):
        """
        Reset puzzle to initial state.

        Clears progress, timers, and updates outputs to reflect a locked puzzle.
        """
        self.state = PuzzleState.LOCKED
        self.current_step = 0
        self.step_start_time = None
        self.puzzle_start_time = None
        self.outputs.update(self.state)
        logging.info("Puzzle reset")

    def solve(self):
        """
        Force puzzle into solved state.

        Useful for operator override or emergency.
        """
        self.state = PuzzleState.SOLVED
        self.outputs.update(self.state)
        logging.info("Puzzle force-solved")

    def update(self):
        """
        Main puzzle loop logic.

        Called repeatedly to:
        - Advance puzzle state
        - Handle timeouts
        - Check inputs or math answers
        """
        if self.state == PuzzleState.SOLVED:
            return  # nothing to do if puzzle already solved

        now = time.time()

        # -----------------------------
        # Transition from LOCKED to IN_PROGRESS
        # -----------------------------
        if self.state == PuzzleState.LOCKED:
            if self.inputs.any_active():
                self.state = PuzzleState.IN_PROGRESS
                self.puzzle_start_time = now
                self.step_start_time = now
                logging.info("Puzzle started")

        # -----------------------------
        # Puzzle is active
        # -----------------------------
        elif self.state == PuzzleState.IN_PROGRESS:

            # Check overall puzzle timeout
            if now - self.puzzle_start_time > self.config["timeout"]:
                logging.warning("Puzzle timeout")
                self.reset()
                return

            # Get current step config
            step = self.config["sequence"][self.current_step]

            # -----------------------------
            # Input step
            # -----------------------------
            if step.get("type", "input") == "input":
                if self.inputs.check(step["input"], step["action"]):
                    # Step completed successfully
                    logging.info(f"Step {self.current_step + 1} correct")
                    self.current_step += 1
                    self.step_start_time = now

                    # Check if puzzle is solved
                    if self.current_step >= len(self.config["sequence"]):
                        self.state = PuzzleState.SOLVED
                        self.outputs.update(self.state)
                        logging.info("Puzzle solved!")
                else:
                    # Step timeout
                    if now - self.step_start_time > step["max_delay"]:
                        logging.warning("Step timeout")
                        self.reset()

            # -----------------------------
            # Math step
            # -----------------------------
            elif step.get("type") == "math":
                # Retrieve answer from InputManager (simulated or real)
                math_answer = self.inputs.get_math_answer()

                if math_answer is not None:
                    if math_answer == step["answer"]:
                        # Correct math answer
                        logging.info(f"Math step {self.current_step + 1} correct")
                        self.current_step += 1
                        self.step_start_time = now

                        # Check if puzzle is solved
                        if self.current_step >= len(self.config["sequence"]):
                            self.state = PuzzleState.SOLVED
                            self.outputs.update(self.state)
                            logging.info("Puzzle solved!")
                    else:
                        # Wrong answer resets puzzle
                        logging.warning("Math answer incorrect")
                        self.reset()
                else:
                    # Step timeout if no answer is given
                    if now - self.step_start_time > step["max_delay"]:
                        logging.warning("Math step timeout")
                        self.reset()
