#  Augmented Reality Hw2

###### 資工四 b05902115 陳建丞

1. **Using the equations given by Chapter 6, page 27 and 28, how to solve the problems given in page 30 (Chapter 6)? Please explain step-by-step of your algorithm, or solutions.**

   

   From the reflection situation on the surface of the light bulb, we can first find out that there are three light sources. 

   ![Screen Shot 2020-04-18 at 2.39.41 PM](/Users/Ingram/Desktop/Screen Shot 2020-04-18 at 2.39.41 PM.png)

   In the blue circle from the picture above, we can see about seven light spots. These are the result of specular reflection, highly centralized and bright. We can separate the surface of the sphere into plenty of pixels, or small pieces. Therefore, we can pick up the small pieces with bright light spots. 

   ![Screen Shot 2020-04-18 at 3.38.36 PM](/Users/Ingram/Desktop/Screen Shot 2020-04-18 at 3.38.36 PM.png)

   The vector from the small piece to the centre of the sphere represents the **reflection vector $\bar R$** according to the specular reflection model. Assume that our eyes or the camera are very close to the direction of $\bar R$, we can trace back to the vector of the **light source $\bar L$**.  And according to the equation of specular reflection, the intensity of the reflection light depends on the **intensity of the light source**, **specular reflection coefficient** of the sphere and the **angle** between of eye and reflection vector. We can compare the three spheres given that they were under the same circumstance with the same intensity of the light source. The light bulb has a higher specular reflection coefficient, which reflects brighter than the others. 

   

   ![Screen Shot 2020-04-18 at 5.50.59 PM](/Users/Ingram/Desktop/Screen Shot 2020-04-18 at 5.50.59 PM.png)

   The reflection on the styrofoam ball and the ping pong ball is not as obvious as that on the light bulb. As metioned above, the specular reflection is week. The reflection is mostly **diffuse reflection**.

   ![Screen Shot 2020-04-18 at 8.17.47 PM](/Users/Ingram/Desktop/Screen Shot 2020-04-18 at 8.17.47 PM.png)

   According to the equation of diffuse reflection, the diffuse reflection depends on **intensity of the light source**, **angle** between of eye and reflection vector, and **diffuse reflection coefficient**. Take the reflection on the styrofoam ball for example, diffuse reflection coefficient and intensity of the light source can be considered as the same for the whole sphere. The only difference is the angle.  

   ![Screen Shot 2020-04-18 at 8.42.24 PM](/Users/Ingram/Desktop/Screen Shot 2020-04-18 at 8.42.24 PM.png)

   If the angle $\theta$ ($0\leq\theta\leq90$) is greater, than $cos(\theta)$ is smaller. Therefore, this creates a light gradient. The reflection in the center is the brightest while the reflection get darker outwards. 

   

2. **Read the paper: An all-in-one solution to geometric and photometric calibration, by Pilet, ISMAR 06. Please explain the solution to page 35 (Chapter 6), That is, A planar tracking target, such as a textured rectangle, can be used as simple light probe to estimate the dominant lighting direction. A virtual object can have realistic shading and cast a shadow.**

   

   To generate a virtual object that has realistic shading and cast a shadow, the main problems are **geometric calibration** and **photometric calibration**. Geometric calibration refers to the process of estimating the parameters required to relate (2-D) points in a camera’s image plane with (3-D) points in the world scene the camera is viewing. On the other hand, photometric calibration refers to the process of estimating the light distribution for rendering specular effects and casting shadows. In this paper, it focused on a robust and convenient method. There are several advantages in this solution, 

   * **Geometric calibration**

     In the system, the calibration pattern can be detected easily in front of the camera. This is an extension from the previous work of pattern recognition from other paper. There are several steps.

     1. Computing and Selecting the best Homographies

        The paper formulates this as a classification problem, which shifts the computational burden to training phase. Interest points from the target objects can be extracted by Harris corner detector to train a set of randomized trees. Next, RANSAC non-linear least-squares estimation is performed to estimated the homography. Last, define a square in the plane attached to the pattern and measure the angle at each corner after warping it by the homography. This can automatedly remove some ambiguous pattern and noise.

        

     2. Initial Estimation of the Internal Parameters

        The internal parameters are first estimated for each camera indi vidually from the homographies. And the papers recovers the external parameteres of each camera by making use of the internal parameters as estimated previously and the homography related to the frame.

        

     3. Refining the Estimation

        Computing displacements by composing pairwise motions is an effective method. However, to be more accurate, the author refines the intrinsic parameters and minimizes with respect to all cameras simultaneously the sum of the reprojection errors for the point correspondences.

     

     The process of geometric calibration includes the online phase and offline phase. Beside the refinement stage, the previous processes are performed in real-time mode. In real-time mode, it's important to be in a synchronous manner for the three cameras. This synchronization is done with a process attached to each camera and form a network. This real-time mode makes the system extremely easy to use.

   * **Phtometric calibration**

     Unlike other researches, this paper's approach relies on the very same set of images of the geometric calibration. Therefore, the pixel intensities within the calibration pattern depend only on its normal. For the illumination model, this paper considers a potentially infinite number of sources. This provides a satisfactory approximation of extended light sources.  The difference in intensity values between images taken at the same time by two different cameras are due to shutter speed or aperture, but not to camera pose. 

     The process of lighting calibration also includes the online phase and offline phase. For the online pre-visualization, the normals can be computed to yield a light map easily done by a short OpenGl shading program with GPU. First, linearize the normals to solve the unknown gains, biases and radiances and use eigenvectors to find the solution.  And if the light change suddnely, locally update the irradiance around the measured normal and keep the old values for other normals.

     However, the fast online pre-visualization might suffer some numerical problems. The offline approach is compuatationally more expensive, but comes with a more sophisticated illumination model that allows for specular highlights, cast shadows, and changing the materials of the virtual objects. This approach starts by estimating the gain and bias of each camera in a way that is independent from lighting effects and normalizing the pixel intensities. Next, apply a regularized deconvolution algorithm on the observed pixel intensities within the calibration object to assign to each individual light the power that best explians the obeservations.

   

   To sum up, this paper presents a system for simultaneous geometric and photometric calibration of multiple cameras. Besides, it's pretty esay to operate and has little constaints on it. The user only  needs to wave a planar calibration pattern in front of the cameras. The system will generate a realistic projection model on to the pattern.

