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
    # Instantiate the simulator
    synthnova_physics_simulator = PhysicsSimulator(my_config)
    # Add default ground plane if you need
    synthnova_physics_simulator.add_default_scene()
    # Add robot
    robot_config = RobotConfig(
    prim_path="/World/Galbot",
    name="galbot_one_charlie",
    mjcf_path=Path()
    .joinpath(synthnova_physics_simulator.synthnova_assets_directory)
    .joinpath("synthnova_assets")
    .joinpath("robot")
    .joinpath("galbot_one_charlie_description")
    .joinpath("galbot_one_charlie.xml"),
    position=[0, 0, 0],
    orientation=[0, 0, 0, 1]
    )
    robot_path = synthnova_physics_simulator.add_robot(robot_config)
    # Initialize the simulator
    synthnova_physics_simulator.initialize()
    # Initialize the galbot interface
    galbot_interface_config = GalbotInterfaceConfig()
    # Enable the modules
    galbot_interface_config.modules_manager.enabled_modules.append("left_gripper")
    galbot_interface_config.left_gripper.joint_names = [
    f"{robot_config.name}/left_gripper_robotiq_85_right_knuckle_joint"
    ]
    # Bind the simulation entity prim path to the interface config
    galbot_interface_config.robot.prim_path = robot_path
    galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config,
    simulator=synthnova_physics_simulator,
    )
    galbot_interface.initialize()
    # Set the gripper to close
    galbot_interface.left_gripper.set_gripper_close()
    # Run the display loop
    synthnova_physics_simulator.loop()
    # Close the simulator
    synthnova_physics_simulator.close()
if __name__ == "__main__":
    main()