---
title: "Vision-Guided Laser Surgical System "
excerpt: "A course project on vision guided robotic surgeries study. <br/><img src='/images/portflio_img_Vision-Guided Laser Surgical System.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_Vision-Guided Laser Surgical System.jpg' width=800>"

## Objective
To implement a vision-guided laser surgical system with a consumer-grade mono-lens camera. The system is expected to be capable of conducting surgical operations on a 2D workspace.

## Technical Summary
Given that the workspace is a 2D surface on the robot’s X-Y plane, the system rectifies the camera image to a top view using homography. The homography transformation matrix is determined using two points set, one in the image pixel frame, and one on the robot X-Y frame. Then the system conducts object detection algorithms on the rectified image to find the desired surgical target or contour. Finally, the coordinates of the target or contour points are commanded to the robot for surgical operations.

## Results
The system is able to conduct two types of surgical operations reliably: Contour Laser Operation and real-time Surgical Target Following.


## Documentation
A short demo video can be found [here](https://www.youtube.com/watch?v=ylswzYXNZJU).



