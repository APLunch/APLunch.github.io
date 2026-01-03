---
title: "Integration of 3D Slicer and Real-Time Simulator via ROS"
excerpt: "My contribution to the bridging of ROS and 3D Slicer for situational aware robotic intervention. <br/><img src='/images/portflio_img_Integration of 3D Slicer and Real-Time Simulator via ROS.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_Integration of 3D Slicer and Real-Time Simulator via ROS.jpg' width=800>

## Objective
One of the most commonly used tools for research and prototyping in medical imaging is 3D Slicer, which is an open-source platform. In the field of robotics, the standard development framework is the open-source middleware suite called the Robot Operating System (ROS). In the past, various attempts have been made to connect these two tools, but they all relied on middleware and custom interfaces. The fact that there is not yet a successful integration of the two tools brings difficulties to research and developments related to robotic intervention. In this project, we proposed to develop a ROS module for 3D Slicer which allows direct usage of ROS packages within the software and builds real-time communication with robotic simulation software like RViz or Asynchronous multi-body framework (AMBF).

## Technical Summary
We proposed to implement a 3D Slicer extension to manage ROS comms within 3D Slicer. The extension parses the URDF from the ROS parameter server, constructs the robot model, and listens to the TF node for rigid transformations of the robot links. On the simulator side, since the framework has ROS integrated, we propose to register the robot URDF to the ROS parameter server, and update the robot link state to the TF node in order to visualize robot dynamics inside 3D Slicer.

## Results
The synchronization of the robot in 3D Slicer via ROS bridge experienced ~13 ms latency which is not visible for the purpose of visualization.

