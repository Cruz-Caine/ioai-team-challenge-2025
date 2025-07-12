from simple_controller import Controller, ControllerSearch, standard_controller_configs
from physics_simulator import PhysicsSimulator
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils.data_types import JointTrajectory
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
import numpy as np
from pathlib import Path
import time

DEADZONE=0.1

RIGHT_Y_DEADZONE = DEADZONE
RIGHT_X_DEADZONE = DEADZONE
LEFT_X_DEADZONE = DEADZONE
LEFT_Y_DEADZONE = DEADZONE

search = ControllerSearch()
count = search.count()

if not count:
    exit()

controller = Controller(0,standard_controller_configs.PLAYSTATION5_CONFIG)

while True:
    print('\033[2J\033[H', end='')  # Clear screen and move cursor to top
    print(controller.state())
    time.sleep(1)