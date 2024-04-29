---
title: "Monocular Depth Estimation with 'PackNet'"
excerpt: "A study on monocular depth estimation with modern neural network architecture. <br/><img src='/images/portflio_img_Monocular Depth Estimation with PackNet.jpg' width=500>"
collection: portfolio
---

<img src='/images/portflio_img_Monocular Depth Estimation with PackNet.jpg' width=800>"

## Objective
Recent research found that the standard downsampling by max-pooling and upsampling can lead to the loss of the semantic information of the input image and be unable to propagate sufficient information for accurate depth prediction. Thus, Guizilini et al leverage the idea of subpixel-convolutional layers and propose to use of packing and unpacking blocks to replace the upsampling and downsampling within the depth network. In this project, we implement PackNet to replace the U-Net in Monodepth2. 

## Technical Summary
We set up a cloud computing instance and cloned the existing Monodepth model onto it. We made changes to the existing model including replacing the U-Net structure with PackNet. After training the models with different experiments, we recorded the results to study the performance of modified networks.

## Results
When the U-Net within the Monodepth2 is replaced with PackNet, the training loss is lower than that using the original monodepth2 model. However, the one with the PackNet reported a worse evaluation result. One potential issue is overfitting the downsampled dataset using the original PackNet. With the channel-dimension reduced PackNet to reduce overfitting risk, we achieved a better result. It’s biased to conclude the worse result using PackNet since we use a smaller dataset.


## Documentation
A project report can be found [here](https://drive.google.com/file/d/1mcbAUpM7g-hR13-M3-45oEvUgtYAjdYp/view?usp=sharing).



