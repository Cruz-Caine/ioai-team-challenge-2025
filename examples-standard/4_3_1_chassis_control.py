from physics_simulator import PhysicsSimulator
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils.data_types import JointTrajectory
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
import numpy as np
from pathlib import Path

def interpolate_joint_positions(start_positions, end_positions, steps):
    return np.linspace(start_positions, end_positions, steps)
def main():
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
    .joinpath("galbot_one_charlie_olympic.xml"),
    position=[0, 0, 0],
    orientation=[0, 0, 0, 1]
    )
    robot_path = physics_simulator.add_robot(robot_config)
    physics_simulator.initialize()
    # Initialize the galbot interface
    galbot_interface_config = GalbotInterfaceConfig()
    galbot_interface_config.modules_manager.enabled_modules.append("chassis")
    galbot_interface_config.chassis.joint_names = [
    f"{robot_config.name}/mobile_forward_joint",
    f"{robot_config.name}/mobile_side_joint",
    f"{robot_config.name}/mobile_yaw_joint",
    ]
    galbot_interface_config.robot.prim_path = robot_path
    galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config,
    simulator=physics_simulator
    )
    galbot_interface.initialize()
    # Start the simulation
    physics_simulator.step()
    # Get current joint positions
    current_joint_positions = galbot_interface.chassis.get_joint_positions()
    target_joint_positions = [1, 6, 1.5]
    # Interpolate joint positions
    positions = interpolate_joint_positions(
    current_joint_positions, target_joint_positions, 5000
    )
    # Create a joint trajectory
    joint_trajectory = JointTrajectory(positions=positions)
    # Follow the trajectory
    galbot_interface.chassis.follow_trajectory(joint_trajectory)
    # Run the display loop
    physics_simulator.loop()
    physics_simulator.close()
main()