![answer](https://github.com/SanjayM22/PerceptionChallenge/assets/56097922/8428a106-bf5f-46c1-891e-69b186be9a71)

<h3> Methodology </h3>
https://gist.github.com/razimgit/d9c91edfd1be6420f58a74e1837bde18 
<br>Used snippets of code from razimgit to do this project, as I'm not knowledgeable about OpenCV and learned how to detect the traffic cones by walking through this project and translating the comments</br>

Steps: 
<br>First, I used a set color threshold to create a grayscale map resembling the cone's color.</br>
<br>Then I enhanced the grayscale map for clarity and detail.</br>
<br>Then highlighted edges to outline important features.</br>
<br>Next extracted contours to define the cone's shape.</br>
<br>And then simplified and refine the contours for smoother outlines.</br>
<br>Identified contours pointing upwards for orientation assessment.</br>
<br>I divided contours for analysis and computed best-fit lines.</br>
<br>Then adjusted grayscale for cone color approximation.</br>
<br>Also acentuated edges for clearer boundaries.</br>
<br>Finally, streamlined contours and determine upward orientations, finding optimal fit lines.</br>
    
<h3> What did you try and why do you think it did not work. </h3>
<br>Mainly just worked through this challenge step by step from research on google</br>
Had trouble with line of best fit because it was very new code to me and hard to understand line of reasoning behind how to do it

<h3> What libraries are used </h3>
<br>OpenCV, numpy, matplotlib, and scipy</br>
Used Python, not C++

