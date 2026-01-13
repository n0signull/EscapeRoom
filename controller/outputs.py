import logging

class OutputManager:
    def update(self, state):
        if state == "LOCKED":
            logging.info("Outputs: LOCKED (LED RED)")
        elif state == "IN_PROGRESS":
            logging.info("Outputs: IN PROGRESS (LED YELLOW)")
        elif state == "SOLVED":
            logging.info("Outputs: SOLVED (LED GREEN / Relay ON)")
