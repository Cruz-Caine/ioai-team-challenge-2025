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
def deadzone_check(value,deadzone):
    if abs(value) < deadzone:
        return 0.0
    return value

def is_PS_pressed(state : dict):
    if state['PS'] == 0:
        return False
    return True

def is_Options_pressed(state : dict):
    if state['Options'] == 0:
        return False
    return True

def is_R1_pressed(state : dict):
    if state['R1'] == 0:
        return False
    return True

def is_L1_pressed(state : dict):
    if state['L1'] == 0:
        return False
    return True

def is_Circle_pressed(state : dict):
    if state['Circle'] == 0:
        return False
    return True

def is_Cross_pressed(state : dict):
    if state['Cross'] == 0:
        return False
    return True

def get_left_X(state : dict):
    return deadzone_check(state['Left_Stick_X'],LEFT_X_DEADZONE)

def get_left_Y(state : dict):
    return deadzone_check(state['Left_Stick_Y'],LEFT_Y_DEADZONE)

def get_right_X(state : dict):
    return deadzone_check(state['Right_Stick_X'],RIGHT_X_DEADZONE)

def get_right_Y(state : dict):
    return deadzone_check(state['Right_Stick_Y'],RIGHT_Y_DEADZONE)

