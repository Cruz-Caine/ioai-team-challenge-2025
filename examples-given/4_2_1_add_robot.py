from physics_simulator import PhysicsSimulator
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
from pathlib import Path
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
    .joinpath("galbot_one_charlie.xml"),
    position=[0, 0, 0],
    orientation=[0, 0, 0, 1]
    )
    physics_simulator.add_robot(robot_config)
    physics_simulator.initialize()
    # Get robot state
    robot_state = physics_simulator.get_robot_state(robot_config.prim_path)
    print(robot_state)
    physics_simulator.loop()
    physics_simulator.close()
main()