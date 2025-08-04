from environ import IOAIEnv
import numpy as np
import time

if __name__ == "__main__":
    env = IOAIEnv(headless=False)
    #TODO: Define your callbacks here
    def demo_callback():
        print("demo callback")
    
    def follow_path_callback():
        """Basic path following callback"""
        if env.simulator.get_step_count() < 3000:
            return

        # Check if path is complete
        if env.current_target_index >= len(env.path):
            env.interface.chassis.set_joint_velocities([0.0, 0.0, 0.0])
            env.simulator.remove_physics_callback("follow_path_callback")
            print("Navigation completed!")
            return

        # Get current state from interface
        current_pos, current_heading = env._get_current_state()
        
        # Update target waypoint
        env._update_target_index(current_pos)
        
        # Get current target position
        if env.current_target_index < len(env.path):
            target_pos = env.path[env.current_target_index]
        else:
            target_pos = env.path[-1]
        
        # Calculate control commands using basic PID
        forward_vel, side_vel, yaw_vel = env.path_follower.calculate_control(
            current_pos, current_heading, target_pos
        )
        
        # Apply velocities
        env.interface.chassis.set_joint_velocities([forward_vel, side_vel, yaw_vel])
        
        # Debug info every 1000 steps
        if env.simulator.get_step_count() % 1000 == 0:
            print(f"Current: ({current_pos[0]:.1f}, {current_pos[1]:.1f}), "
                  f"Target: ({target_pos[0]:.1f}, {target_pos[1]:.1f}), "
                  f"Waypoint: {env.current_target_index}/{len(env.path)}")

    # def pick_and_place_callback():
    #     """Callback function for pick and place task using state machine"""

    #     def init_state():
    #         """Move to initial pose"""
    #         # Convert world frame pose to robot frame
    #         base_position = env.robot.get_position()
    #         base_orientation = env.robot.get_orientation()
    #         #current_pos, current_heading = env.robot_to_world_frame()
    #         # world_pos = np.array([0.5, 0.3, 0.7])
    #         # world_ori = np.array([0, 0.7071, 0, 0.7071])
    #         world_pos = base_position
    #         world_ori =base_orientation  
    #         robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
    #         return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
    #     def move_to_pre_pick_state():
    #         """Move to pre-pick position"""
    #         if env.state_first_entry:
    #             # Use vision model to detect object pose instead of ground truth
    #             vision_result = env.get_object_pose_from_vision("cube")
    #             if vision_result is not None:
    #                 world_pos, world_ori = vision_result
    #                 env.cube_position = world_pos.copy()
    #                 env.cube_orientation = world_ori.copy()
    #                 print(f"Vision detected cube at position: {world_pos}")
    #             else:
    #                 # Fallback to ground truth if vision fails
    #                 cube_state = env.simulator.get_object_state("/World/Cube")
    #                 env.cube_position = cube_state["position"].copy()
    #                 env.cube_orientation = cube_state["orientation"].copy()
    #                 print("Using ground truth fallback for cube position")
    #             env.state_first_entry = False
            
    #         # Convert world frame pose to robot frame
    #         world_pos = env.cube_position + np.array([0, 0, 0.15])
    #         world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for grasping
    #         robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
    #         return env._move_left_arm_to_pose(robot_pos, robot_ori)

    #     def move_to_pick_state():
    #         """Move to pick position"""
    #         # Re-detect object position for more accurate pick
    #         vision_result = env.get_object_pose_from_vision("cube")
    #         if vision_result is not None:
    #             world_pos, world_ori = vision_result
    #             # Use detected position for more accurate pick
    #             pick_pos = world_pos + np.array([0, 0, 0.03])
    #         else:
    #             # Fallback to stored position
    #             pick_pos = env.cube_position + np.array([0, 0, 0.03])
            
    #         # Convert world frame pose to robot frame
    #         world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for grasping
    #         robot_pos, robot_ori = env.world_to_robot_frame(pick_pos, world_ori)
    #         return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
    #     def grasp_state():
    #         """Grasp the object"""
    #         if env.state_first_entry:
    #             env.interface.left_gripper.set_gripper_close()
    #             env.grasp_start_time = time.time()
    #             env.state_first_entry = False
            
    #         # Stay in grasp state for 2 seconds
    #         if time.time() - env.grasp_start_time >= 2.0:
    #             return True
    #         return False

    #     def move_to_pre_place_state():
    #         """Move to pre-place position"""
    #         # Convert world frame pose to robot frame
    #         world_pos = env.cube_position + np.array([-0.1, 0, 0.4])
    #         world_ori = np.array([0, 0.7071, 0, 0.7071])
    #         robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
    #         return env._move_left_arm_to_pose(robot_pos, robot_ori)

    #     def move_to_place_state():
    #         """Move to place position"""
    #         if env.state_first_entry:
    #             # Use vision model to detect bin pose instead of ground truth
    #             vision_result = env.get_object_pose_from_vision("bin")
    #             if vision_result is not None:
    #                 world_pos, world_ori = vision_result
    #                 env.bin_position = world_pos.copy()
    #                 env.bin_orientation = world_ori.copy()
    #                 print(f"Vision detected bin at position: {world_pos}")
    #             else:
    #                 # Fallback to ground truth if vision fails
    #                 bin_state = env.simulator.get_object_state("/World/Bin")
    #                 env.bin_position = bin_state["position"].copy()
    #                 env.bin_orientation = bin_state["orientation"].copy()
    #                 print("Using ground truth fallback for bin position")
    #             env.state_first_entry = False

    #         # Convert world frame pose to robot frame
    #         world_pos = env.bin_position + np.array([0, 0, 0.3])
    #         world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for placing
    #         robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
    #         return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
    #     def release_state():
    #         """Release the object"""
    #         if env.state_first_entry:
    #             env.interface.left_gripper.set_gripper_open()
    #             env.grasp_start_time = time.time()
    #             env.state_first_entry = False
            
    #         # Stay in release state for 1 second
    #         if time.time() - env.grasp_start_time >= 1.0:
    #             return True
    #         return False
        
    #     def return_to_init_state():
    #         """Return to initial pose"""
    #         return init_state()

    #     # Add states to state machine
    #     env.state_machine.add_state(0, "Init", init_state)
    #     env.state_machine.add_state(1, "MoveToPrePick", move_to_pre_pick_state)
    #     env.state_machine.add_state(2, "MoveToPick", move_to_pick_state)
    #     env.state_machine.add_state(3, "Grasp", grasp_state)
    #     env.state_machine.add_state(4, "MoveToPrePlace", move_to_pre_place_state)
    #     env.state_machine.add_state(5, "MoveToPlace", move_to_place_state)
    #     env.state_machine.add_state(6, "Release", release_state)
    #     env.state_machine.add_state(7, "ReturnToInit", return_to_init_state)

    #     # Execute current state
    #     if env.state_machine.trigger():
    #         env.state_first_entry = True
    #         env.motion_in_progress = False
    #         print(f"Current state: {env.state_machine.get_state_name()}")
        
    #     # Execute current state and move to next when complete
    #     if env.state_machine.execute_current_state():
    #         env.state_machine.next()
    #         env.state_first_entry = True


    def pick_and_place_callback():
        """Callback function for pick and place task using state machine"""

        def init_state():
            """Move to initial pose"""
            # Convert world frame pose to robot frame
            world_pos = np.array([0.5, 0.3, 0.7])
            world_ori = np.array([0, 0.7071, 0, 0.7071])
            robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
            return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
        def move_to_pre_pick_state():
            """Move to pre-pick position"""
            if env.state_first_entry:
                # Use vision model to detect object pose instead of ground truth
                vision_result = env.get_object_pose_from_vision("cube")
                if vision_result is not None:
                    world_pos, world_ori = vision_result
                    env.cube_position = world_pos.copy()
                    env.cube_orientation = world_ori.copy()
                    print(f"Vision detected cube at position: {world_pos}")
                else:
                    # Fallback to ground truth if vision fails
                    cube_state = env.simulator.get_object_state("/World/Cube")
                    env.cube_position = cube_state["position"].copy()
                    env.cube_orientation = cube_state["orientation"].copy()
                    print("Using ground truth fallback for cube position")
                env.state_first_entry = False
            
            # Convert world frame pose to robot frame
            world_pos = env.cube_position + np.array([0, 0, 0.15])
            world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for grasping
            robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
            return env._move_left_arm_to_pose(robot_pos, robot_ori)

        def move_to_pick_state():
            """Move to pick position"""
            # Re-detect object position for more accurate pick
            vision_result = env.get_object_pose_from_vision("cube")
            if vision_result is not None:
                world_pos, world_ori = vision_result
                # Use detected position for more accurate pick
                pick_pos = world_pos + np.array([0, 0, 0.03])
            else:
                # Fallback to stored position
                pick_pos = env.cube_position + np.array([0, 0, 0.03])
            
            # Convert world frame pose to robot frame
            world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for grasping
            robot_pos, robot_ori = env.world_to_robot_frame(pick_pos, world_ori)
            return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
        def grasp_state():
            """Grasp the object"""
            if env.state_first_entry:
                env.interface.left_gripper.set_gripper_close()
                env.grasp_start_time = time.time()
                env.state_first_entry = False
            
            # Stay in grasp state for 2 seconds
            if time.time() - env.grasp_start_time >= 2.0:
                return True
            return False

        def move_to_pre_place_state():
            """Move to pre-place position"""
            # Convert world frame pose to robot frame
            world_pos = env.cube_position + np.array([-0.1, 0, 0.4])
            world_ori = np.array([0, 0.7071, 0, 0.7071])
            robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
            return env._move_left_arm_to_pose(robot_pos, robot_ori)

        def move_to_place_state():
            """Move to place position"""
            if env.state_first_entry:
                # Use vision model to detect bin pose instead of ground truth
                vision_result = env.get_object_pose_from_vision("bin")
                if vision_result is not None:
                    world_pos, world_ori = vision_result
                    env.bin_position = world_pos.copy()
                    env.bin_orientation = world_ori.copy()
                    print(f"Vision detected bin at position: {world_pos}")
                else:
                    # Fallback to ground truth if vision fails
                    bin_state = env.simulator.get_object_state("/World/Bin")
                    env.bin_position = bin_state["position"].copy()
                    env.bin_orientation = bin_state["orientation"].copy()
                    print("Using ground truth fallback for bin position")
                env.state_first_entry = False

            # Convert world frame pose to robot frame
            world_pos = env.bin_position + np.array([0, 0, 0.3])
            world_ori = np.array([0, 0.7071, 0, 0.7071])  # Fixed orientation for placing
            robot_pos, robot_ori = env.world_to_robot_frame(world_pos, world_ori)
            return env._move_left_arm_to_pose(robot_pos, robot_ori)
        
        def release_state():
            """Release the object"""
            if env.state_first_entry:
                env.interface.left_gripper.set_gripper_open()
                env.grasp_start_time = time.time()
                env.state_first_entry = False
            
            # Stay in release state for 1 second
            if time.time() - env.grasp_start_time >= 1.0:
                return True
            return False
        
        def return_to_init_state():
            """Return to initial pose"""
            return init_state()

        # Add states to state machine
        env.state_machine.add_state(0, "Init", init_state)
        env.state_machine.add_state(1, "MoveToPrePick", move_to_pre_pick_state)
        env.state_machine.add_state(2, "MoveToPick", move_to_pick_state)
        env.state_machine.add_state(3, "Grasp", grasp_state)
        env.state_machine.add_state(4, "MoveToPrePlace", move_to_pre_place_state)
        env.state_machine.add_state(5, "MoveToPlace", move_to_place_state)
        env.state_machine.add_state(6, "Release", release_state)
        env.state_machine.add_state(7, "ReturnToInit", return_to_init_state)

        # Execute current state
        if env.state_machine.trigger():
            env.state_first_entry = True
            env.motion_in_progress = False
            print(f"Current state: {env.state_machine.get_state_name()}")
        
        # Execute current state and move to next when complete
        if env.state_machine.execute_current_state():
            env.state_machine.next()
            env.state_first_entry = True

    #env.simulator.add_physics_callback("demo_callback", demo_callback)

    # env.goal_pos = (4,2)
    # env.simulator.add_physics_callback("follow_path_callback", follow_path_callback)
    # env.goal_pos = (4,4)
    env.simulator.add_physics_callback("pick and place", pick_and_place_callback)
    env.run()