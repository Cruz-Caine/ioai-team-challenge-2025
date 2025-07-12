# Robot Physics Simulation

A collection of robotics simulation examples using a physics simulator with robot control, geometry manipulation, and camera integration.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Verify the installation:

```bash
python examples-given/verify.py
```

## Project Structure

- `examples-given/` - Original example files
- `examples-working/` - Working versions of examples
- `controller/` - Robot controller implementation and documentation
- `requirements.txt` - Project dependencies

## Examples

### Basic Simulation
- `4_1_basic_simulation.py` - Basic physics simulation setup

### Robot Configuration
- `4_2_1_add_robot.py` - Adding a robot to the simulation
- `4_2_2_add_basic_geometry.py` - Adding basic geometric shapes
- `4_2_3_add_mesh_config.py` - Configuring mesh objects

### Robot Control
- `4_3_1_chassis_control.py` - Chassis movement control
- `4_3_2_left_arm_control.py` - Left arm manipulation
- `4_3_3_left_gripper_control.py` - Left gripper control

### Camera Integration
- `4_4_1_front_head_camera.py` - Front head camera setup
- `4_4_2_left_wrist_camera.py` - Left wrist camera configuration

## Robot Control

For detailed robot control mapping and usage instructions, see [Controller Documentation](controller/CONTROLLER.MD).

## Usage

Run any example:

```bash
python examples-working/4_1_basic_simulation.py
```

The simulator will open a display window where you can observe the physics simulation and robot behavior.

## Dependencies

- `physics_simulator` - Core physics simulation engine
- `synthnova_config` - Configuration management
- `Simple-Controller` - Robot control utilities