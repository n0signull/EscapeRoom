import time
import logging

class PuzzleState:
    LOCKED = "LOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    SOLVED = "SOLVED"

class PuzzleEngine:
    def __init__(self, config, inputs, outputs):
        self.config = config
        self.inputs = inputs
        self.outputs = outputs
        self.reset()

    def reset(self):
        self.state = PuzzleState.LOCKED
        self.current_step = 0
        self.step_start_time = None
        self.puzzle_start_time = None
        self.outputs.update(self.state)
        logging.info("Puzzle reset")

    def solve(self):
        self.state = PuzzleState.SOLVED
        self.outputs.update(self.state)
        logging.info("Puzzle force-solved")

    def update(self):
        if self.state == PuzzleState.SOLVED:
            return

        now = time.time()

        if self.state == PuzzleState.LOCKED:
            if self.inputs.any_active():
                self.state = PuzzleState.IN_PROGRESS
                self.puzzle_start_time = now
                self.step_start_time = now
                logging.info("Puzzle started")

        elif self.state == PuzzleState.IN_PROGRESS:
            if now - self.puzzle_start_time > self.config["timeout"]:
                logging.warning("Puzzle timeout")
                self.reset()
                return

            step = self.config["sequence"][self.current_step]

            if self.inputs.check(step["input"], step["action"]):
                logging.info(f"Step {self.current_step + 1} correct")
                self.current_step += 1
                self.step_start_time = now

                if self.current_step >= len(self.config["sequence"]):
                    self.state = PuzzleState.SOLVED
                    self.outputs.update(self.state)
                    logging.info("Puzzle solved!")
            else:
                if now - self.step_start_time > step["max_delay"]:
                    logging.warning("Step timeout")
                    self.reset()
