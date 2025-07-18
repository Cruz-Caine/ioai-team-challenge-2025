from physics_simulator import PhysicsSimulator
from synthnova_config import (
PhysicsSimulatorConfig,
RobotConfig,
RgbCameraConfig,
RealsenseD435RgbSensorConfig,
DepthCameraConfig,
RealsenseD435DepthSensorConfig,
)
from physics_simulator.galbot_interface import GalbotInterface, GalbotInterfaceConfig
from physics_simulator.utils import preprocess_depth
import os
import numpy as np
import cv2
from pathlib import Path
def main():
    """Main function to set up and run the front head camera example."""
    # Instantiate the simulator
    my_config = PhysicsSimulatorConfig()
    physics_simulator = PhysicsSimulator(my_config)
    # Add default scene
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
    robot_path = physics_simulator.add_robot(robot_config)
    # Add front head RGB camera (RealSense D435)
    front_head_rgb_camera_config = RgbCameraConfig(
    name="front_head_rgb_camera",
    prim_path=os.path.join(
    robot_path,
    "head_link2",
    "head_end_effector_mount_link",
    "front_head_rgb_camera",
    ),
    translation=[0.09321, -0.06166, 0.033],
    rotation=[
    0.683012701855461,
    0.1830127020294028,
    0.18301270202940284,
    0.6830127018554611,
    ],
    sensor_config=RealsenseD435RgbSensorConfig(),
    parent_entity_name="galbot_one_charlie/head_end_effector_mount_link"
    )
    front_head_rgb_camera_path =  physics_simulator.add_sensor(front_head_rgb_camera_config)
    # Add front head depth camera (RealSense D435)
    front_head_depth_camera_config = DepthCameraConfig(
    name="front_head_depth_camera",
    prim_path=os.path.join(
    robot_path,
    "head_link2",
    "head_end_effector_mount_link",
    "front_head_depth_camera",
    ),
    translation=[0.09321, -0.06166, 0.033],
    rotation=[
    0.683012701855461,
    0.1830127020294028,
    0.18301270202940284,
    0.6830127018554611,
    ],
    sensor_config=RealsenseD435DepthSensorConfig(),
    parent_entity_name="galbot_one_charlie/head_end_effector_mount_link"
    )
    front_head_depth_camera_path = physics_simulator.add_sensor(
    front_head_depth_camera_config
    )
    # Initialize the galbot interface
    galbot_interface_config = GalbotInterfaceConfig()
    # Enable the modules
    galbot_interface_config.modules_manager.enabled_modules.append("front_head_camera")
    # Bind the simulation entity prim path to the interface config
    galbot_interface_config.robot.prim_path = robot_path
    galbot_interface_config.front_head_camera.prim_path_rgb = front_head_rgb_camera_path
    galbot_interface_config.front_head_camera.prim_path_depth = (
    front_head_depth_camera_path
    )
    galbot_interface = GalbotInterface(
    galbot_interface_config=galbot_interface_config,
    simulator=physics_simulator
    )
    galbot_interface.initialize()
    # Start the simulation
    physics_simulator.play()
    # Initial steps to stabilize the simulation
    physics_simulator.step(10)
    while True:
        physics_simulator.step(7)
        # Get rgb data
        rgb_data = galbot_interface.front_head_camera.get_rgb()
        # Get depth data
        depth_data = galbot_interface.front_head_camera.get_depth()
        # Preprocess depth data for visualization
        # You can also use this function to preprocess the depth data for other purposes
        depth_data = preprocess_depth(
        depth_data,
        scale=1000, # m to mm
        min_value=0.0,
        max_value=3 * 1000, # 3m to mm
        data_type=np.uint16,
        )
        # Display images in non-blocking way
        cv2.imshow("RGB Camera", cv2.cvtColor(rgb_data,
        cv2.COLOR_RGB2BGR))
        cv2.imshow("Depth Camera", depth_data)
        # Wait for 1ms and check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
    # Get camera parameters
    params = galbot_interface.front_head_camera.get_parameters()
    intrinsic_matrix = params["rgb"]["intrinsic_matrix"]
    print(params)
    print("intrinsic_matrix: ", intrinsic_matrix)
    # Close the simulator
    physics_simulator.close()
if __name__ == "__main__":
    main()