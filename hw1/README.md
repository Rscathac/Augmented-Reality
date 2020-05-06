# Augmented Reality hw1

###### 資工四 B05902115 陳建丞

### Environment Setup

* Python 3.5

* Required Package

  * numpy
  * cv2 
  * argparse
  * math
  * sympy

* How to run the code

  ``````python
  python tracking.py $input_file_directory$ [-d]
  ``````

  [ -d ] : use partial differential method

### Implementation

1. **Detect the coordinates of points ABC**

   Filter out the **RGB** color $A(255, 0, 0), B(255, 100, 0), C(0, 0, 255)$

   Noted that the input of python image is default in the color channel of **BGR**.

2. **Imaging**

   Use the principle of imaging to estimate the value of Z coordinates.

   $\frac1S+\frac1{S'}=\frac1f$

   Given the values of $f$ as 0.473 cm, $S$ can be derived. If the Z coordinate of the paper is 0, then the Z coordinate of camera O is close to $S$. 

3. **Church's method**

   First we set up the initial coordinate for the camera. It is important to set up a suitable one, otherwise, the church's method might have a chance to lead to a local solution. 

   Since we have estimated the Z coordinate, we can use this Z value as the initial Z coordinates of camera O. For X and Y, they can be estimated using the principle of imaging agian. I use A as a reference point, and with the ratio of $S$ and $S$ to estimate the initial X and Y.

   Next, Church's method can be implemented by numerical method or partial differential method. Both can derive the true answer.

   * **Numerical method**

     For each iteration, calculate $\text{diff} = |\angle aob-\angle AOB|$ of the neighbor pixels of O. Iterate to the neightbor pixel with minimum $\text{diff}$.  

   * **Partial differential method**

     Calculate $\text{diff} = |\angle aob- \angle AOB|$ and parital derivatives $\frac{\partial{\text{diff}}}{\partial{x}}$ $\frac{\partial{\text{diff}}}{\partial{y}}$ $\frac{\partial{\text{diff}}}{\partial{z}}$ as gradient. Revise the coordinates of O with the gradient.

     * I use ```sympy``` package to implement the algebra calculation. This might take a lot more time than the numerical method.

### Result

![Screen Shot 2020-05-06 at 3.41.17 PM](/Users/Ingram/Desktop/Screen Shot 2020-05-06 at 3.41.17 PM.png)