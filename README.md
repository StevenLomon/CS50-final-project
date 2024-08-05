Is there a Rubber Duck in this Image?

My final project for Harvard's CS50 course!
Video demo: 

Description:
Allows the user to either upload an image or turn on their web camera and have the application detect if there is a rubber duck present in the picture/camera! :)

My complete starting vision now writing on the 5th of Aug 2024: 
There will be a front-end web application with the title "Is there a Rubber Duck in this Image?" and the option to choose Upload Image or Turn on Camera.
If the user uploads an image, the image will display on the screen and one of two things will happen. 1: There is no rubber duck in the image and so there are no bounding boxes applied. There is a text below the image that will say "No rubber duck detected :(". 2: There is a rubber duck in the image and so a bounding box will surround it with a percentage of how sure the model is that it is indeed a rubber duck. Below the image, the text "Rubber duck detected! :))" will be displayed.
If the user instead presses Turn on Camera, they will be asked for permission to turn on the camera of their computer. As soon as a rubber duck enters the periphery of the camer

I'm thinking to build the web application in Flask but eventually maybe migrate it to Django. But Flask for now. Enough vision to get me going is that there will be an index route and one route for each option represented by each button?
Since I am far from a front-end developer, the style.css is rather shamelessly copied from the Finance problem and modified haha.
The camera detection will take heavy inspiration from this video: https://www.youtube.com/watch?v=CeTR_-ALdRw
The image recognition takes inspiration from the second project in this video: https://www.youtube.com/watch?v=akeSJBEWr3w
I will follow NeuralNine's video pretty closely to set up the camera classifier but as for the Image Recognition using Amazon Rekognition, I will mostly use the help of ChatGPT. I believe the scope of this project is just enough! :)

I hope that istherearubberduckinthisimage.com is available to buy!

Try it out here: 
