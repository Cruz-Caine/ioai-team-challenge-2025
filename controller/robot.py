from simple_controller import Controller, ControllerSearch,standard_controller_configs
from physics_simulator import PhysicsSimulator
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils.data_types import JointTrajectory
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
import state_checks as scs
import numpy as np
from pathlib import Path
import math

search = ControllerSearch()
count = search.count()

if not count:
    print("Controller Not Connected")
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
galbot_interface_config.modules_manager.enabled_modules.append("left_arm"
)
galbot_interface_config.left_arm.joint_names = [
f"{robot_config.name}/left_arm_joint1",
f"{robot_config.name}/left_arm_joint2",
f"{robot_config.name}/left_arm_joint3",
f"{robot_config.name}/left_arm_joint4",
f"{robot_config.name}/left_arm_joint5",
f"{robot_config.name}/left_arm_joint6",
f"{robot_config.name}/left_arm_joint7",
]
galbot_interface_config.modules_manager.enabled_modules.append("right_gripper")
galbot_interface_config.right_gripper.joint_names = [
f"{robot_config.name}/right_gripper_robotiq_85_right_knuckle_joint"
]
galbot_interface_config.modules_manager.enabled_modules.append("left_gripper")
galbot_interface_config.left_gripper.joint_names = [
f"{robot_config.name}/left_gripper_robotiq_85_right_knuckle_joint"
]
galbot_interface_config.robot.prim_path = robot_path
galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config, simulator=physics_simulator
)
galbot_interface.initialize()

physics_simulator.step()

X_MULTIPLIER=2
Y_MULTIPLIER=2
TURN_MULTIPLIER=0.5
right_gripper_switch =  False
right_gripper_switch_prev = False
left_gripper_switch =  False
left_gripper_switch_prev = False

while physics_simulator.is_running():
    state = controller.state()
    right_arm_mode = scs.is_R1_pressed(state)
    left_arm_mode = scs.is_L1_pressed(state)

    # Chasis and Arm Control
    if right_arm_mode:
        galbot_interface.chassis.set_joint_positions([0,0,0],True)
        pass
    elif left_arm_mode:
        galbot_interface.chassis.set_joint_positions([0,0,0],True)
        pass
    else:
        # Chasis Control
        current_joint_positions = galbot_interface.chassis.get_joint_positions()
        print(current_joint_positions)
        #xy_arr =  [(scs.get_left_Y(state))*Y_MULTIPLIER*-1, (scs.get_left_X(state))*X_MULTIPLIER*-1,current_joint_positions[2]]
        rot_arr = [0,0,(scs.get_right_X(state))*TURN_MULTIPLIER]
        xy_arr =  [(scs.get_left_Y(state))*Y_MULTIPLIER*-1, (scs.get_left_X(state))*X_MULTIPLIER*-1,current_joint_positions[2]]

        target_joint_positions = list(map(lambda x, y: x + y, xy_arr, rot_arr))  
        print(target_joint_positions)
        galbot_interface.chassis.set_joint_positions(target_joint_positions,True)

    # If controller is freshly preshed activate the switch, if its been held down do nothing
    if scs.is_Circle_pressed(state):
        if (not right_gripper_switch_prev):
            right_gripper_switch = True
            right_gripper_switch_prev = True
        else:
            right_gripper_switch = False
    else:
        right_gripper_switch = False
        right_gripper_switch_prev = False

    if right_gripper_switch:
        if galbot_interface.right_gripper.is_open:
            print("Closing")
            galbot_interface.right_gripper.set_gripper_close()
        elif galbot_interface.right_gripper.is_close:
            print("Opening")
            galbot_interface.right_gripper.set_gripper_open()

    # If controller is freshly preshed activate the switch, if its been held down do nothing
    if scs.is_Cross_pressed(state):
        if (not left_gripper_switch_prev):
            left_gripper_switch = True
            left_gripper_switch_prev = True
        else:
            left_gripper_switch = False
    else:
        left_gripper_switch = False
        left_gripper_switch_prev = False

    if left_gripper_switch:
        if galbot_interface.left_gripper.is_open:
            print("Closing")
            galbot_interface.left_gripper.set_gripper_close()
        elif galbot_interface.left_gripper.is_close:
            print("Opening")
            galbot_interface.left_gripper.set_gripper_open()



    physics_simulator.step(7)
    if scs.is_Options_pressed(state):
        physics_simulator.reset()
        physics_simulator.play()
        physics_simulator.step()
    if scs.is_PS_pressed(state):
        physics_simulator.close()
print("Done")
