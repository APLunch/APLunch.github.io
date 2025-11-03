---
title: "3D Structure Reconstruct from Motion "
excerpt: "A practice on Computer Vision and multi-view geometry <br/><img src='/images/portflio_img_3D_reconstruction_from_motion.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_3D_reconstruction_from_motion.jpg' width=800>"

## Objective
For this project, we used the Tomasi-Kanade algorithm to reconstruct the shape of an object from a sequence of images. Two sets of images were used in the experiment: the first set consisted of 28 consecutive images of a castle taken from a moving camera, and the second set consisted of pictures taken from around a Medusa statue face. The project aimed to demonstrate the Tomasi-Kanade algorithm's ability to approximately reconstruct an object's shape from a series of images.

## Results
From the images and analysis obtained, we conclude that the algorithm is well-performed,
and the 3D reconstruction results give decent recoveries of the original objects in 3D space.
In the castle case, we can tell the windows, roofs, and trees roughly from the point cloud. In
the Medusa statue case, the selected features are roughly around a plane in space, which
corresponds to the face of Medusa's status in the source video.
It takes less than 1 minute (53s) to run 5000 features points, which is an indicator that the
the algorithm is fairly good in terms of time complexity.


## Documentation
Doc and code on this project can be found [here](https://github.com/APLunch/Tomasi-Kanade-Structure-from-Motion).

