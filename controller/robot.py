from simple_controller import Controller, ControllerSearch,standard_controller_configs
from physics_simulator import PhysicsSimulator
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils.data_types import JointTrajectory
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
import state_checks as scs
import numpy as np
from pathlib import Path

search = ControllerSearch()
count = search.count()

if not count:
    exit()

controller = Controller(0,standard_controller_configs.PLAYSTATION5_CONFIG)


def interpolate_joint_positions(start_positions, end_positions, steps):
    return np.linspace(start_positions, end_positions, steps)


# Create sim config
my_config = PhysicsSimulatorConfig()
physics_simulator = PhysicsSimulator(my_config)
physics_simulator.add_default_scene()
# Add robot
robot_config = RobotConfig(
    prim_path="/World/Galbot",
    name="galbot_one_charlie",
    mjcf_path=Path()
    .joinpath(physics_simulator.synthnova_assets_directory)
    .joinpath("synthnova_assets")
    .joinpath("robot")
    .joinpath("galbot_one_charlie_description")
    .joinpath("galbot_one_charlie.xml"),
    position=[0, 0, 0],
    orientation=[0, 0, 0, 1],
)
robot_path = physics_simulator.add_robot(robot_config)
physics_simulator.initialize()

galbot_interface_config = GalbotInterfaceConfig()
galbot_interface_config.modules_manager.enabled_modules.append("chassis")
galbot_interface_config.chassis.joint_names = [
    f"{robot_config.name}/mobile_forward_joint",
    f"{robot_config.name}/mobile_side_joint",
    f"{robot_config.name}/mobile_yaw_joint",
]
galbot_interface_config.robot.prim_path = robot_path
galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config, simulator=physics_simulator
)
galbot_interface.initialize()

physics_simulator.step()

X_MULTIPLIER=2
Y_MULTIPLIER=2
TURN_MULTIPLIER=2

while physics_simulator.is_running():
    state = controller.state()
    right_arm_mode = scs.is_R1_pressed(state)
    left_arm_mode = scs.is_L1_pressed(state)
    if right_arm_mode:
        galbot_interface.chassis.set_joint_positions([0,0,0],True)
        pass
    elif left_arm_mode:
        galbot_interface.chassis.set_joint_positions([0,0,0],True)
        pass
    else:
        current_joint_positions = galbot_interface.chassis.get_joint_positions()
        print(current_joint_positions)
        target_joint_positions = [(scs.get_left_Y(state))*Y_MULTIPLIER, (scs.get_left_X(state))*X_MULTIPLIER, 0]
        galbot_interface.chassis.set_joint_positions(target_joint_positions,True)


    physics_simulator.step(7)
    if scs.is_PS_pressed(state):
        physics_simulator.close()
print("Done")
