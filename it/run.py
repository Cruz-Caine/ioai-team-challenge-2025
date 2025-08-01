from environ import IOAIEnv

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

    #env.simulator.add_physics_callback("demo_callback", demo_callback)

    env.simulator.add_physics_callback("follow_path_callback", follow_path_callback)
    env.run()