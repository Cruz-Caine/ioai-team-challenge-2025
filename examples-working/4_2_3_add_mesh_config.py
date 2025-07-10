from synthnova_config import PhysicsSimulatorConfig, MeshConfig, RobotConfig
from physics_simulator import PhysicsSimulator
from pathlib import Path
def main():
    # Initialize simulator
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
    # Add table mesh(was changed from shelf https://github.com/galbot-ioai/physics_sim_edu/commit/c2c149a9a072a772c8cb25ea01ca5b442d05d7ba)
    table_config = MeshConfig(
        prim_path="/World/Table",
        mjcf_path=Path()
        .joinpath(physics_simulator.synthnova_assets_directory)
        .joinpath("synthnova_assets")
        .joinpath("default_assets")
        .joinpath("example")
        .joinpath("ioai")
        .joinpath("table")
        .joinpath("table.xml"),
        position=[0.65, 0, 0],
        orientation=[0, 0, 0.70711, -0.70711],
        scale=[0.5, 0.7, 0.5]
    )
    physics_simulator.add_object(table_config)
    # No bottle so replaced with closet
    closet_config = MeshConfig(
    prim_path="/World/Closet",
    name="bottle",
    mjcf_path=Path()
    .joinpath(physics_simulator.synthnova_assets_directory)
    .joinpath("synthnova_assets")
    .joinpath("default_assets")
    .joinpath("example")
    .joinpath("ioai")
    .joinpath("closet")
    .joinpath("closet.xml"),
    position=[0.55, 0, 1],
    orientation=[0, 0, 0, 1],
    scale=[0.122, 0.122, 0.122]
    )
    physics_simulator.add_object(closet_config)
    # Initialize and run
    physics_simulator.initialize()
    physics_simulator.loop()
    physics_simulator.close()
main()