import yaml
import time
import logging
from controller.puzzle import PuzzleEngine
from controller.inputs import InputManager
from controller.outputs import OutputManager

logging.basicConfig(level=logging.INFO)

with open("controller/config.yaml") as f:
    config = yaml.safe_load(f)

inputs = InputManager()
outputs = OutputManager()
engine = PuzzleEngine(config, inputs, outputs)

def loop():
    while True:
        engine.update()
        time.sleep(0.1)

