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

I then started to code and implement the Flask front end. I made sure that the button on the index front page linked
correctly to the image route and that the image route can be reached by clicking the Upload Image button. The biggest
lesson to take away from being stuck here for a little while is that the actions in the .html files should link to the
routes, not html files

All image validation was added and then instead of saving the image locally to an uploads folder, the image is uploaded to 
our S3 bucket like we tried out in rekognition.py. Two things of importance:
1. I had to use s3.upload_fileobj and not s3.upload_file since it's a file uploaded through a Flask form and not stored
locally on my filesystem. In a web application, it's more secure to handle files in memory (using file-like objects) rather than saving them to disk, which might expose them to unintended access!
2. It was important that I added a file.seek(0) before uploading the image. I managed to upload an image to S3 before adding
that little piece of code and the image was corrupted and couldn't be opened

Once an image is completely validated and uploaded to the S3 bucket we
1. Interact with Rekognition to get a rubber duck confidence score
2. Store the result in an SQLite3 database that I will create shortly
3. Generate a unique result ID using uuid4
4. Redirect to the result page where the result will be fetch using the resultID

The SQLite db connection was set up without the CS50 training wheels and a duck_results table was created
A things that tripped me up was using TEXT for the primary key ID since we're using a unique uuid string and not a simple
auto-incremental integer. I also had to consult with ChatGPT on how to deal with thread safety when using database connections in Flask. The solution is create a separate db connection everytime we insert or update something. Also created a separate script to set up the initial table since the 'before_first_request' decorator is depreciated

To display the uploaded image I had to enable public read as a Bucket Policy for my S3 bucket. Since this is not in production and just a rather silly project, this is okay. I applied a max width of 400 pixels to the displayed uploaded picture and I also added a custom jinja filter that is used when displaying the confidence score, very similar to the filter used in Finance

After being able to display succesful results where I've uploaded an image of an actual rubber duck came the other scenario when a rubber duck is not in the picture. After some consulting and reflecting, I decided to change the table schema. A new column duck_found was added which will be either 0 or 1 and NOT NULL will be removed from the confidence_score column. This allows for an if statement in the result.html that uses the duck_found variable

Next up is bounding boxes. At this stage I also observed that Rekognition is more confident detecting "Bird" rather than "Duck" when I upload something that clearly is a rubber duck. So I decided to pivot my approac and have Rubber duck confidence be made up of Toy confidence and Bird confidence. Still a rubber duck if you ask me haha! I also changed the name of the function, changed it to have it return a dict and started coding to extract the bounding box data. This is the data that will be used together with matplot lib to draw out the bounding boxes in the images that the use uploads for the final result

To get started with drawing the bounding boxes in matplot lib...


Try it out here: 
