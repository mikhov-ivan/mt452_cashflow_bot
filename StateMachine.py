import logging
from enum import Enum

global logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

class State(Enum):
    MAIN = 1


class StateMachine:
    def __init__(self):
        self.state = State.MAIN
        self.log_state()
    
    def cmd(self, cmd):
        self.log_state()
    
    def log_state(self):
        logger.info("SM: Current state: {}".format(self.state.name))

