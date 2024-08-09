Is there a Rubber Duck in this Image?

My final project for Harvard's CS50 course!
Video demo: 

Description:
Allows the user to either upload an image or turn on their web camera and have the application detect if there is a rubber duck present in the picture/camera! :)

My complete starting vision now writing on the 5th of Aug 2024: 
There will be a front-end web application with the title "Is there a Rubber Duck in this Image?" and the option to choose Upload Image or Turn on Camera.
If the user uploads an image, the image will display on the screen and one of two things will happen. 1: There is no rubber duck in the image and so there are no bounding boxes applied. There is a text below the image that will say "No rubber duck detected :(". 2: There is a rubber duck in the image and so a bounding box will surround it with a percentage of how sure the model is that it is indeed a rubber duck. Below the image, the text "Rubber duck detected! :))" will be displayed.
If the user instead presses Turn on Camera, they will be asked for permission to turn on the camera of their computer. If no rubber duck is visible for the camera as it opens, there will be a text under the camera window saying "No rubber duck detected." As soon as a rubber duck enters the periphery of the camera, the text will be changed to "Rubber duck detected! :)". I don't think bounding boxes will be implemented in this mode but we'll see!

I'm thinking to build the web application in Flask but eventually maybe migrate it to Django. But Flask for now. Enough vision to get me going is that there will be an index route and one route for each option represented by each button?
Since I am far from a front-end developer, the style.css is rather shamelessly copied from the Finance problem and modified haha.
The camera detection will take heavy inspiration from this video: https://www.youtube.com/watch?v=CeTR_-ALdRw
The image recognition takes inspiration from the second project in this video: https://www.youtube.com/watch?v=akeSJBEWr3w
I will follow NeuralNine's video pretty closely to set up the camera classifier but as for the Image Recognition using Amazon Rekognition, I will mostly use the help of ChatGPT. I believe the scope of this project is just enough! :)

I hope that istherearubberduckinthisimage.com is available to buy!

Journal:
An S3 Bucket was created
An IAM User was created that has full access to S3 and AWS Rekognition
Since I realized mid-project that AWS Rekognition is not available in the Stockholm region, I decided to re-create the Bucket and use Frankfurt (eu-central-1) since Stockholm and Frankfurt are in the same time zone. A list of service availability by region can be found here:
https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/

After succesfully setting up and implementing Rekognition and playing around to see which labels it can and can’t snap up, I found that “Rubber duck” is not a label, but it can detect “Duck” with 98.51734924316406 confidence and “Toy” with 57.209102630615234 confidence. This was my ticket haha; Duck + Toy = Rubber duck

I wrote some code to implement this logic of combining the labels of Duck and Toy, taking the average of their confidence
to get Rubber Duck confidence haha!


Try it out here: 
