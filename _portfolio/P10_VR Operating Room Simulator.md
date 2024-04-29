---
title: "VR Operating Room Simulator"
excerpt: "The Virtual Operating Room Team Experience (VORTeX) simulation system. <br/><img src='/images/portflio_img_VR_operating_room_simulator.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_VR_operating_room_simulator.jpg' width=800>"

## Objective
Virtual Operating Room Team Experience (VORTeX) is a research project at RPI’s Center for Modeling, Simulation, & Imaging in Medicine(CeMSIM). The project’s goal is to construct a VR environment for training surgeons and nurses. My objective is to develop a network interface that accommodates the multiplayer feature of the simulator, especially the moving of the objects in the virtual environment.

## Technical Summary
The simulator is built using the Unity3D game engine. I set up TCP and UDP sockets between the game server and the client. When a player grabs an object in the virtual environment using his/her game controller, the client publishes the object’s pose to all other clients via the server. In the meantime, all clients subscribe to the server to acquire the pose information of the objects except for the objects that are controlled by the local player. The TCP connection is used to send important information such as the ownership of an item while UDP is used to update time-efficient messages such as the pose of an item.

## Results
When a player grabs and moves an item in the game, other players can see the updated pose of the item and cannot grab the item directly from the former. However, it only worked if an item is moved by a player using his/her controller. If an item moves due to the game’s physics, then the pose of the item is not synced. Other researchers at the lab took over for further development.
