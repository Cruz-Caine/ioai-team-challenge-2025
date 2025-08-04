"""
Example of using YOLO + pose estimation model in IOAIEnv
"""

import os
from pathlib import Path
from environ import IOAIEnv, YoloPoseEstimationModel

from physics_simulator.utils.state_machine import SimpleStateMachine

def main():
    """Main function to run IOAIEnv with YOLO pose estimation"""
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Configuration paths
    # yolo_model_path = script_dir / ".." / "yolo_seg_examples" / "real_all_class_0730.pt"
    yolo_model_path = script_dir / ".." / "yolo_seg_examples" / "best.pt"
    cad_models_dir = script_dir / ".." / "pose_est_examples" / "models"
    
    # Camera intrinsic parameters (adjust based on your camera)
    camera_matrix = [637.7254326533274, 637.7254326533274, 640.0, 360.0]
    
    # Check if required files exist
    if not yolo_model_path.exists():
        print(f"Error: YOLO model not found at {yolo_model_path}")
        return
    
    if not cad_models_dir.exists():
        print(f"Error: CAD models directory not found at {cad_models_dir}")
        return
    
    # Create YOLO pose estimation model
    pose_estimation_model = YoloPoseEstimationModel(
        yolo_model_path=str(yolo_model_path),
        cad_models_dir=str(cad_models_dir),
        camera_matrix=camera_matrix
    )
    
    # Create environment with pose estimation model
    env = IOAIEnv(
        headless=False,
        pose_estimation_model=pose_estimation_model,
        scenario_type="full"
    )
    
    print("Starting IOAIEnv with YOLO pose estimation...")
    print("Press Ctrl+C to stop")

    state_machine = SimpleStateMachine(max_states=8)
    def complete():
        def nothing():
            pass
        def set_shelf_as_goal():

            env.start_pos = (env.current_pos[0], env.current_pos[1])
            env.goal_pos = (4, 4)
            
            env.path = env.planner.find_path(env.start_pos, env.goal_pos)
            return nothing()
        state_machine.add_state(0, "pcik", env.pick_and_place_callback)
        state_machine.add_state(1, "goal", set_shelf_as_goal)
        state_machine.add_state(2, "path", env.follow_path_callback)
    
        # Execute current state
        if state_machine.trigger():
            state_first_entry = True
            motion_in_progress = False
            print(f"Current state: {env.state_machine.get_state_name()}")
        
        # Execute current state and move to next when complete
        if state_machine.execute_current_state():
            # Check if we can move to next state
            if not state_machine.next():
                # Task completed, reset state machine for next cycle
                print("Pick and place task completed!")
                state_machine.reset()
            state_first_entry = True

    try:
        # Add physics callback and run
        #env.simulator.add_physics_callback("pick_and_place", env.pick_and_place_callback)
        env.simulator.add_physics_callback("pick_and_place", env.pick_callback)
        # env.simulator.loop()
        # env.goal_pos = (4,4)
        # env.simulator.add_physics_callback("move_to_shelf", env.follow_path_callback)
        # env.simulator.add_physics_callback("every", complete)
        env.simulator.loop()
    except KeyboardInterrupt:
        print("\nStopping simulation...")
    finally:
        env.simulator.close()

if __name__ == "__main__":
    main()