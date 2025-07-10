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
    # Add shelf mesh
    shelf_config = MeshConfig(
        prim_path="/World/Shelf",
        name="shelf",
        mjcf_path=Path()
        .joinpath(physics_simulator.synthnova_assets_directory)
        .joinpath("synthnova_assets")
        .joinpath("default")
        .joinpath("shelves")
        .joinpath("1")
        .joinpath("model")
        .joinpath("mjcf")
        .joinpath("convex_decomposition.xml"),
        position=[0.55, 0, 0],
        orientation=[0, 0, 0, 1]
    )
    physics_simulator.add_object(shelf_config)
    # Add bottle
    bottle_config = MeshConfig(
    prim_path="/World/Bottle",
    name="bottle",
    mjcf_path=Path()
    .joinpath(physics_simulator.synthnova_assets_directory)
    .joinpath("synthnova_assets")
    .joinpath("default")
    .joinpath("skus")
    .joinpath("1")
    .joinpath("model")
    .joinpath("mjcf")
    .joinpath("convex_decomposition.xml"),
    position=[0.55, 0, 0.1],
    orientation=[0, 0, 0, 1],
    scale=[0.122, 0.122, 0.122]
    )
    physics_simulator.add_object(bottle_config)
    # Initialize and run
    physics_simulator.initialize()
    physics_simulator.loop()
    physics_simulator.close()
main()