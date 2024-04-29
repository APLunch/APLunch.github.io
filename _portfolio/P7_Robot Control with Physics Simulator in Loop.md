---
title: "Robot Control with Physics Simulator in Loop "
excerpt: "To enhance surgical robot's situation awareness and controls. <br/><img src='/images/portflio_img_Robot Control with Physics Simulator in Loop.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_Robot Control with Physics Simulator in Loop.jpg' width=800>"

## Objective
Surgeries often are operated near the patient’s critical tissue. A surgical robot is not aware of the context hence it cannot provide safety constraints to protect the critical tissue. The object of this project is to construct the robot’s context situation awareness using a simulator and provide haptic feedback to the surgeon based on the context to prevent the tooltip from invading critical tissue.

## Technical Summary
Assuming known patient registration and anatomy. Using AMBF to simulate a Mastoidectomy surgery, we created a virtual world and synced the physical Galen surgical robot to the simulated one via ROS communication. A distance vector from the closest critical anatomy to the tooltip is calculated in the simulator and returned to the robot. We implemented the robot control algorithm to provide haptic feedback to push the tooltip away from the critical anatomy.

## Results
The robot provides haptic feedback to cancel the surgeon’s force when the tooltip is within 15mm of the critical anatomy. Future work and research are ongoing.


## Documentation
Project poster can be found [here](https://drive.google.com/file/d/1laXzu64mKgi6oraNN8cxa3iWm8t6Ho1K/view?usp=sharing).



