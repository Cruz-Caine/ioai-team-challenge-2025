from physics_simulator import PhysicsSimulator
from synthnova_config import PhysicsSimulatorConfig, RobotConfig
from pathlib import Path
# Create sim config
my_config = PhysicsSimulatorConfig()
physics_simulator = PhysicsSimulator(my_config)
# Add default scene
physics_simulator.add_default_scene()
# Initialize the simulator
physics_simulator.initialize()
# Run the display loop
physics_simulator.loop()
# Close the simulator
physics_simulator.close()