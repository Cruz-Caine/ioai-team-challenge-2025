from physics_simulator import PhysicsSimulator
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils.data_types import JointTrajectory
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
import numpy as np
from pathlib import Path

def main():
    # Create sim config and add robot
    my_config = PhysicsSimulatorConfig()
    physics_simulator = PhysicsSimulator(my_config)
    physics_simulator.add_default_scene()
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
    orientation=[0, 0, 0, 1]
    )
    robot_path = physics_simulator.add_robot(robot_config)
    physics_simulator.initialize()
    # Initialize the galbot interface
    galbot_interface_config = GalbotInterfaceConfig()
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
    galbot_interface_config.robot.prim_path = robot_path
    galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config,
    simulator=physics_simulator
    )
    galbot_interface.initialize()
    # Control arm
    physics_simulator.step()
    current_joint_positions = galbot_interface.left_arm.get_joint_positions()
    target_joint_positions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    # Create and follow trajectory
    positions = np.linspace(current_joint_positions,
    target_joint_positions, 500)
    joint_trajectory = JointTrajectory(positions=positions)
    galbot_interface.left_arm.follow_trajectory(joint_trajectory)
    physics_simulator.loop()
    physics_simulator.close()
main()