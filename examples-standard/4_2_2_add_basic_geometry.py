from synthnova_config import PhysicsSimulatorConfig, CuboidConfig
from physics_simulator import PhysicsSimulator
from pathlib import Path
def main():
    # Initialize simulator
    my_config = PhysicsSimulatorConfig()
    physics_simulator = PhysicsSimulator(my_config)
    physics_simulator.add_default_scene()
    # Add cube 1
    cube_1_config = CuboidConfig(
    prim_path=Path(physics_simulator.root_prim_path).joinpath("cube_1"),
    position=[2, 2, 2],
    orientation=[0, 0, 0, 1],
    scale=[1, 1, 1],
    color=[1.0, 0.0, 0.0],
    )
    cube_1_path = physics_simulator.add_object(cube_1_config)
    # Add cube 2
    cube_2_config = CuboidConfig(
    prim_path=Path(physics_simulator.root_prim_path).joinpath("cube_2"),
    position=[0, 0, 2],
    orientation=[0, 0, 0, 1],
    scale=[1, 1, 1],
    color=[0.0, 1.0, 0.0],
    )
    cube_2_path = physics_simulator.add_object(cube_2_config)
    # Add cube 3
    cube_3_config = CuboidConfig(
    prim_path=Path(physics_simulator.root_prim_path).joinpath("cube_3"),
    position=[-2, -2, 2],
    orientation=[0, 0, 0, 1],
    scale=[1, 1, 1],
    color=[0.0, 0.0, 1.0],
    )
    cube_3_path = physics_simulator.add_object(cube_3_config)
    # Initialize and run
    physics_simulator.initialize()
    physics_simulator.get_object_state(cube_1_path)
    physics_simulator.loop()
    physics_simulator.close()

main()