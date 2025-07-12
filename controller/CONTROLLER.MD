# Galbot G1 Controller Mapping

## Control Scheme

| Input                                | Function           | Description                                                    | Implemented |
| ------------------------------------ | ------------------ | -------------------------------------------------------------- | ----------- |
| **Left Stick**                       | Robot Movement     | Up/Down: Forward/Backward<br>Left/Right: Strafe left/right     | Y            |
| **Right Stick**                      | Robot Rotation     | Left/Right: Turn left/right<br>Up/Down: *Not used*             | Y            |
| **L1 (Hold)**                        | Left Arm Mode      | Must hold to control left arm                                  |             |
| **R1 (Hold)**                        | Right Arm Mode     | Must hold to control right arm                                 |             |
| **Left Stick** *(while L1/R1 held)*  | Arm Position       | Up/Down: Reach forward/back<br>Left/Right: Move arm left/right |             |
| **Right Stick** *(while L1/R1 held)* | Arm Height & Wrist | Up/Down: Raise/lower arm<br>Left/Right: Rotate wrist           |             |
| **X Button**                         | Left Gripper       | Open/close left hand                                           |             |
| **O Button**                         | Right Gripper      | Open/close right hand                                          |             |
| **Triangle**                         | Head Up            | Tilt head upward                                               |             |
| **Square**                           | Head Down          | Tilt head downward                                             |             |
| **D-Pad Left**                       | Head Left          | Turn head left                                                 |             |
| **D-Pad Right**                      | Head Right         | Turn head right                                                |             |
| **D-Pad Up**                         | Center Head        | Return head to neutral                                         |             |
| **D-Pad Down**                       | Speed Toggle       | Switch between normal/slow speed                               |             |
| **L1 + R1 + Triangle**               | Emergency Stop     | Stop all robot movement                                        |             |
| **L1 + R1 + Square**                 | Home Position      | Return robot to default pose                                   |             |

## Quick Start Guide

### Pick Up Object
1. **Navigate**: Use Left Stick to drive near object
2. **Select Arm**: Hold L1 (left arm) or R1 (right arm)  
3. **Position**: Use Left Stick to move arm over object
4. **Lower**: Use Right Stick up/down to lower arm
5. **Grasp**: Press X (left) or O (right) to close gripper
6. **Lift**: Use Right Stick to raise object

### Place Object
1. **Navigate**: Drive to target location with Left Stick
2. **Position**: Use arm controls to move over target
3. **Lower**: Use Right Stick to lower to placement height
4. **Release**: Press X or O to open gripper

### Important Notes
- **Arms only move when L1 or R1 is held down**
- **Release L1/R1 to lock arms in current position**
- **Use D-Pad Down for slow/precise movements**
- **Emergency stop: L1 + R1 + Triangle**