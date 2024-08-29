Is there a Rubber Duck in this Image?

My final project for Harvard's CS50 course! Video demo: https://www.youtube.com/watch?v=7oBrnQxvCRE&t=6s
Try it out here: istherearubberduckinthisimage.se

Description: Allows the user to either upload an image or turn on their web camera and have the application detect if there is a rubber duck present in the picture/camera! :)

This is a project that is rather silly in nature and simply a fun showcase of this detection technology. But it can easily be adjusted for someone more useful in the real world such as identifying products in a store for inventory management, smart surveillance systems, identifying suspicious objects in the streets or ...

I believe I've really got to practice taking imperfect action and fine tuning as I go which is super important when it comes to coding and large projects. Not getting crippled by analysis paralysis and instead being solution oriented. Failing forward!

My complete starting vision now writing on the 5th of Aug 2024: There will be a front-end web application with the title "Is there a Rubber Duck in this Image?" and the option to choose Upload Image or Turn on Camera. If the user uploads an image, the image will display on the screen and one of two things will happen. 1: There is no rubber duck in the image and so there are no bounding boxes applied. There is a text below the image that will say "No rubber duck detected :(". 2: There is a rubber duck in the image and so a bounding box will surround it with a percentage of how sure the model is that it is indeed a rubber duck. Below the image, the text "Rubber duck detected! :))" will be displayed. If the user instead presses Turn on Camera, they will be asked for permission to turn on the camera of their computer. If no rubber duck is visible for the camera as it opens, there will be a text under the camera window saying "No rubber duck detected." As soon as a rubber duck enters the periphery of the camera, the text will be changed to "Rubber duck detected! :)". I don't think bounding boxes will be implemented in this mode but we'll see!

I'm thinking to build the web application in Flask but eventually maybe migrate it to Django. But Flask for now. Enough vision to get me going is that there will be an index route and one route for each option represented by each button? Since I am far from a front-end developer, the style.css is rather shamelessly copied from the Finance problem and modified haha. The camera detection will take heavy inspiration from this video: https://www.youtube.com/watch?v=CeTR_-ALdRw The image recognition takes inspiration from the second project in this video: https://www.youtube.com/watch?v=akeSJBEWr3w I will follow NeuralNine's video pretty closely to set up the camera classifier but as for the Image Recognition using Amazon Rekognition, I will mostly use the help of ChatGPT. I believe the scope of this project is just enough! :)

I hope that istherearubberduckinthisimage.com is available to buy!

Journal: An S3 Bucket was created An IAM User was created that has full access to S3 and AWS Rekognition Since I realized mid-project that AWS Rekognition is not available in the Stockholm region, I decided to re-create the Bucket and use Frankfurt (eu-central-1) since Stockholm and Frankfurt are in the same time zone. A list of service availability by region can be found here: https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/

After succesfully setting up and implementing Rekognition and playing around to see which labels it can and can’t snap up, I found that “Rubber duck” is not a label, but it can detect “Duck” with 98.51734924316406 confidence and “Toy” with 57.209102630615234 confidence. This was my ticket haha; Duck + Toy = Rubber duck

I wrote some code to implement this logic of combining the labels of Duck and Toy, taking the average of their confidence to get Rubber Duck confidence haha!

I then started to code and implement the Flask front end. I made sure that the button on the index front page linked correctly to the image route and that the image route can be reached by clicking the Upload Image button. The biggest lesson to take away from being stuck here for a little while is that the actions in the .html files should link to the routes, not html files

All image validation was added and then instead of saving the image locally to an uploads folder, the image is uploaded to our S3 bucket like we tried out in rekognition.py. Two things of importance:

I had to use s3.upload_fileobj and not s3.upload_file since it's a file uploaded through a Flask form and not stored locally on my filesystem. In a web application, it's more secure to handle files in memory (using file-like objects) rather than saving them to disk, which might expose them to unintended access!
It was important that I added a file.seek(0) before uploading the image. I managed to upload an image to S3 before adding that little piece of code and the image was corrupted and couldn't be opened
Once an image is completely validated and uploaded to the S3 bucket we

Interact with Rekognition to get a rubber duck confidence score
Store the result in an SQLite3 database that I will create shortly
Generate a unique result ID using uuid4
Redirect to the result page where the result will be fetch using the resultID
The SQLite db connection was set up without the CS50 training wheels and a duck_results table was created A things that tripped me up was using TEXT for the primary key ID since we're using a unique uuid string and not a simple auto-incremental integer. I also had to consult with ChatGPT on how to deal with thread safety when using database connections in Flask. The solution is create a separate db connection everytime we insert or update something. Also created a separate script to set up the initial table since the 'before_first_request' decorator is depreciated

To display the uploaded image I had to enable public read as a Bucket Policy for my S3 bucket. Since this is not in production and just a rather silly project, this is okay. I applied a max width of 400 pixels to the displayed uploaded picture and I also added a custom jinja filter that is used when displaying the confidence score, very similar to the filter used in Finance

After being able to display succesful results where I've uploaded an image of an actual rubber duck came the other scenario when a rubber duck is not in the picture. After some consulting and reflecting, I decided to change the table schema. A new column duck_found was added which will be either 0 or 1 and NOT NULL will be removed from the confidence_score column. This allows for an if statement in the result.html that uses the duck_found variable

Next up is bounding boxes. At this stage I also observed that Rekognition is more confident detecting "Bird" rather than "Duck" when I upload something that clearly is a rubber duck. So I decided to pivot my approac and have Rubber duck confidence be made up of Toy confidence and Bird confidence. Still a rubber duck if you ask me haha! I also changed the name of the function, changed it to have it return a dict and started coding to extract the bounding box data. This is the data that will be used together with matplot lib to draw out the bounding boxes in the images that the use uploads for the final result. I added three columns to the database schema to store all bounding box data: a Boolean bounding_box_available that is NOT NULL, a Text boolean_box_data, and another Text s3_url_bounding_box

To get started with drawing the bounding boxes in matplot lib, ChatGPT provided me with a function that will draw it using matplotlib; both pyplot and another one I've never heard of called patches. A lot of changes were done in both app.py and rekognition.py in order to properly extract bounding box data and use it with the uploaded image. The bounding box data needed to be parsed to json format. In rekognition.py, I decided that I will always use the bounding box data for the 'Toy' label (will often be 98%+) if a rubber duck is detected. I also needed to save the uploaded image locally in order to use it with PIL and matplotlib and therefore another line of app.config was added to configure UPLOAD_FOLDER

Saving the file locally for drawing bounding boxes caused quite the hick ups. But after brute forcing and a lot of consulting with ChatGPT, I saw the light again. We save locally, then upload to S3 and we fetch the image Rekognition uses from S3. The code to upload to S3 was adjusted slightly from just: try: s3.upload_fileobj(file, bucket_name, filename) to: try: with open(file_path, "rb") as data: s3.upload_fileobj(data, bucket_name, filename)

After having fixed this, brute forcing for about an hour, I encountered another smaller problem, more silly in nature: I'm just naïvely adding "-bb" to the entire filename, resulting in this error: "ValueError: unknown file extension: .jpg-bb". This was fixed rather simply by splitting the filename into base name and extension using

For quite a few moments there were problems seeing the bounding boxes. I could see them on the locally saved image but not the one uploaded to S3 that is being displayed on the front end with Flask. The fix for this was to use upload_file instead of upload_fileobj since we're uploading a locally saved image and not a Flask in-memory file

Now that uploading images fully work, I wanted to spend some time fune tuning our model. Maybe see where it doesn't work despite it being a rubber duck, see what labels Rekognition detects and fine tune my algorithm for detecting rubber ducks.

This was an interesting image to upload: https://www.rebeccas.com/rubber-ducks-3-12-inch-12-count.html The 'Toy' label is nowhere to be found, the 'Bird' label is only found with 66.6% confidence and the coin is seemingly interfering a lot. I can't simply look for 'Bird' and call it a rubber duck, I need 'Toy' or something similar.

I tried having these three as the main labels: rubber_duck_labels = ['Toy', 'Bird', 'Duck'], and updated the logic in the code accordinly. But this resulted in scenarios with confidence values like this: Confidence values: [99.88025665283203, 79.40372467041016, 61.668853759765625] That being 'Toy', 'Bird' and 'Duck' in that order. So I went back to only having rubber_duck_labels = ['Toy', 'Bird']

Ultimarely I wanted to be able to detect rubber ducks in pictures like these: https://asiantigersgroup.com/news/industry-news/the-quack-tacular-arrival-hong-kong-welcomes-giant-rubber-duckies/ And I was when I set maxLabels as 50 and minConfidence as 50! In pictures like these, Rekognition has to sift through a loooot of labels in order to get to the things we're looking for haha. But they're in there somewhere! In that picture we have these confidence values: Confidence values: [55.149723052978516, 55.149723052978516, 52.95594787597656] And the order is difference this time. These are the filtered labels: Filtered labels: [{'Name': 'Bird', 'Confidence': 55.149723052978516, 'Instances': [], 'Parents': [{'Name': 'Animal'}], 'Aliases': [], 'Categories': [{'Name': 'Animals and Pets'}]}, {'Name': 'Duck', 'Confidence': 55.149723052978516, 'Instances': [], 'Parents': [{'Name': 'Animal'}, {'Name': 'Bird'}], 'Aliases': [], 'Categories': [{'Name': 'Animals and Pets'}]}, {'Name': 'Toy', 'Confidence': 52.95594787597656, 'Instances': [], 'Parents': [], 'Aliases': [], 'Categories': [{'Name': 'Hobbies and Interests'}]}] In going through all of the labels that Rekognition picked up in this picture I also found another useful label: 'Inflatable'! This one was quickly added to the list of accepted labels. I noticed that 'Beak' could also be added but I 'Bird' is enough. I want a bounding box around the big inflatable duck however :( I noticed something really interesting in this picture: https://www.fruugo.se/xianrenge-bath-duck-toys-16-pcs-rubber-ducks-squeak-and-float-duckies-baby-shower-toy-party-decoration-for-toddlers-boys-girls/p-69542347-139677373?language=en A bounding box was available for the label 'Helmet' but it only had a confidence on that label of 57.63%. Hence, I decided to lower my BoundingBox threshold from 80 to 50 and implement a new list of BoundingBox labels as an extension of all rubber duck labels where 'Helmet' was one of the new labels I also noticed with further experimentation that it is possible that it detects only one label ('Toy') and deems it a rubber duck when that is not the case at all hahaha. There needs to be at least 2 labels in filtered_labels I adjusted MinCondifence to 52 but shortly thereafter I decided to keep it at 50 in case it can give us BoundingBox data and instead I added a conditional that any label in filtered_labels need to have a confidence score of at least 52

This picture was very useful and the first one where I got a bounding box for a large inflatable duck! https://www.reuters.com/lifestyle/one-two-giant-rubber-ducks-hong-kong-harbour-deflates-2023-06-10/ These are its filtered labels: Filtered labels: [{'Name': 'Inflatable', 'Confidence': 95.83766174316406, 'Instances': [], 'Parents': [], 'Aliases': [], 'Categories': [{'Name': 'Toys and Gaming'}]}, {'Name': 'Bird', 'Confidence': 81.74077606201172, 'Instances': [{'BoundingBox': {'Width': 0.00635563675314188, 'Height': 0.011960327625274658, 'Left': 0.1470615416765213, 'Top': 0.734575092792511}, 'Confidence': 81.74077606201172}, {'BoundingBox': {'Width': 0.3781373202800751, 'Height': 0.5818305015563965, 'Left': 0.3939252197742462, 'Top': 0.2852320373058319}, 'Confidence': 77.08781433105469}], 'Parents': [{'Name': 'Animal'}], 'Aliases': [], 'Categories': [{'Name': 'Animals and Pets'}]}, {'Name': 'Toy', 'Confidence': 52.23092269897461, 'Instances': [], 'Parents': [], 'Aliases': [], 'Categories': [{'Name': 'Hobbies and Interests'}]}] It picks up 'Inflatable' with a confidence of 95.84! But 'Toy' with a confidence of only 52.23. I could keep changing the label threshold to 53 or I could just change the code so that only one is used. And so I did. We only use either 'Toy' or 'Inflatable', whichever is the largest. So rubber duck is essentially 'Bird' + 'Toy' OR 'Bird' + 'Inflatable'

In order to not be stuck in fine tuning hell forever, I decided that this would be the final test: https://interaksyon.philstar.com/trends-spotlights/2023/06/11/253380/one-of-two-giant-rubber-ducks-in-hong-kong-harbor-deflates/ And this one revealed a very important implementation detail! 'Duck' is in the labels but not 'Bird'. It only has a confidence score of 50.6 but it's in there! So a few changes needed to be done before I called it a project. 'Rubber Duck' as a label is now either a combination of 'Bird' + 'Toy', 'Bird' + 'Inflatable', 'Duck' + 'Toy' or 'Duck' + 'Inflatable'. That's it. That's final :)

The Camera feature might be implemented in the future. The vision there is to enable to laptop camera and detect a rubber duck with added bounding boxes as soon as one enters the frame

After a few post-satisfied experimentation where I inserted a Rubber Duck in photos with vibrant environments, people and lots of other things in the image, the model couldn't recognize a single rubber duck, even with the MaxLabel parameter at its absolute maximum of 1000. I only started being able to detect rubber duck in these Photoshopped images once I lowered the MinConfidence. One of such gave these results: Confidence values: [49.04203796386719, 44.312538146972656] Rubber Duck Label: Bird + Toy These results were from a custom image I deemed Medium difficulty: Confidence values: [38.668697357177734, 42.10551834106445] Rubber Duck Label: Bird + Inflatable. With that I decided that a good parameter value for MinConfidence is 35. It managed to find the rubber duck with 1000 but not with 500 so this parameter would have to lie somewhere in between. Neither with 965 haha. Further experimentation led to the value of 970. It didn't work with 969. But this brought up the importance of speed and user experience. Is it really worth being able to do these really obscure edge cases if the overall user experience is worsened? I don't think so. Having a MaxLabels value of 970 is absolutely not worth it when we can still find the majority of rubber ducks with a value of 100. 320 was the label I landed on. With this value, it passes 4/5 of my Easy difficultly custom images haha

So to recap, after a lot of manual experimentation (this is what you would usually use GridSearchCV or something for haha) and reflection on user experience, I decided to go for 320 for my MaxLabel parameter and 35 for my MinConfidence parameter

And with THAT, the project was a wrap :)

Edit: When I was recording the showcase of the problem, I did do one final change in refactoring the Rekognition code so that we don't have to create a new Rekognition object every time the get_rekognition_data function is called

http://istherearubberduckinthisimage.com/ is available! I'm buying that!! :D

### Web hosting
istherearubberduckinthisimage.com is available! I'm buying that!! :D
Edit: istherearubberduckinthisimage.se is available for 5kr for the fist year using the Swedish site one.com so I'm buying it there with the hope that I can migrate to istherearubberduckinthisimage.com in the future haha!

The domain was bought at one.com and then set up using AWS Route 53 by setting up a new hosted zone. The newly bought domain of istherearubberduckinthisimage.se was entered and "Public Hosted Zone" was selected as Type. Once the hosted zone was created, the name servers that were created for the domain were entered in one.com under DNS settings. Once the settings were saved, a request to change the name servers were sent which can take up to 48 hours. 
An EC2 instance was then set up. The Ubuntu AMI was chosen as well as t3.micro to stay in the free tier of AWS. All settings were left as their defauly values except for the Security group network settings: All HTTP and HTTPS traffic were checked to be allowed and SSH traffic only from my IP address. The instance was then launched.  

Once the instance was up and running, it was connected to using SSH and the newly created keypair login. Once on the Ubuntu virtual machine, the package list was updated and all necessary packages for hosting a Flask web application were installed, most importantly Nginx and Gunicorn. The repository was cloned using 'git clone' and the GitHub repo web URL. Once the virtual environment was set up, an error occured when trying to install all dependencies using the requirements.txt file. The solution to this turned out to be to manually install 'python3-distutils', 'setuptools' and 'wheel' to the EC2 instance. Once these were installed, another dependency issue arised: "AttributeError: module 'pkgutil' has no attribute 'ImpImporter'. Did you mean: 'zipimporter'?
      [end of output]"  
The solution to this turned out to be to first upgrade setuptools and wheel, upgrade to the latest version of pip, remove scipy from requirements (it wasn't even used so I have no idea why it was in there) and use numpy 2.1.0 instead of 1.24.0.  

The Flask app was now supposed to be able to be tested using 'gunicorn --bind 0.0.0.0:8000 wsgi:app' but another problem arised, there was no wsgi.py so it was created. The code block to run the app was also deleted from app.py to avoid redundant execution. For the longest time, the gunicorn bind command wouldn't work but it was fixed by deactivating the current virtual environment, deleting it and creating a new one.  

Once Gunicorn was confirmed to be working, Nginx had to be set up. The following command was used to edit the Nginx file:  
sudo vim /etc/nginx/sites-available/flaskapp  
The following was added:  
server {
    listen 80;
    server_name istherearubberduckinthisimage.se;                                                                                                                                                                                                                                                           location / {                                                                                                                                            proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;                                                                                                                        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }                                                                                                                                                                                                                                                               location /static/ {
    alias /home/ubuntu/CS50-final-project/static/;
    }
}   
The server block was enablind and nginx was restarted using the following:  
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled  
sudo nginx -t  
sudo systemctl restart nginx  
I was greeted with the following:  
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok  
nginx: configuration file /etc/nginx/nginx.conf test is successful  

Once everything was set up on the instance level, an "A" record in Route 53 was created pointing to the EC2 instance’s public IP address, making sure that all domain directs traffic to the Flask application. Except for the Public IP address for Value, all values were left as the default values.  

Once the "A" record was created, the web application was secured with SSL. Certbot was installed on the EC2 instance:  
sudo apt-get install certbot python3-certbot-nginx  
The SSL certificate was obtained and installed using:  
sudo certbot --nginx -d istherearubberduckinthisimage.se -d istherearubberduckinthisimage.se  
Consider donating!  
https://letsencrypt.org/donate/  
https://supporters.eff.org/donate/support-effs-work-lets-encrypt  
I will as soon as I have disposable income hahaha.  

Upon first trying to access the site at istherearubberduckinthisimage.se, I got a 504 Gateway timeout error. And these were to steps taken to try and fix it:
1. Increasing the Gunicorn Timeout:  
gunicorn --bind 0.0.0.0:8000 --timeout 60 wsgi:app  
(No other step was needed since I quickly realized that I earlier killed this very proccess that keeps the web server running hahaha)
Running Gunicorn in the background was enabled using nohup:  
nohup gunicorn --bind 0.0.0.0:8000 wsgi:app &  

The website was now available at the bought domain! But there was one final issue in that the CSS wasn't loading properly. This was fixed by first of all changing the name from style.css to styles.css (convention), creating a subdirectory in static called css and placing it there rather than just in static (once again; convention that I didn't follow haha) and using the correct HTML link tag: Changing  
<link href="/static/styles.css" rel="stylesheet">  
to  
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">  
nginx was also adjusted to be correct (specifically the path to static) and restarted.  

Now instead there was a 403 forbidden error!  
The ownership of the static directory was updated with:  
sudo chown -R www-data:www-data /home/ubuntu/CS50-final-project/static/  
And permissions were updated with the following (I don't understand this at all, I had tapped out and just wanted it to work):  
sudo find /home/ubuntu/CS50-final-project/static/ -type d -exec chmod 755 {} \;  
sudo find /home/ubuntu/CS50-final-project/static/ -type f -exec chmod 644 {} \;  

My mind was a jumble mess at this point but running this command: ls -ld /home/ubuntu /home/ubuntu/CS50-final-project  
showed what the problem was:  
`drwxr-x--- 7 ubuntu   ubuntu   4096 Aug 28 12:08 /home/ubuntu`  
`drwxrwxr-x 8 www-data www-data 4096 Aug 28 11:54 /home/ubuntu/CS50-final-project`  
One of the directories was owned by 'ubuntu' and one by 'www-data'. This was fixed by first making sure that the parent directory /home/ubuntu was accessible to the www-data user with the following command:  
sudo chmod 755 /home/ubuntu  
Another things that was causing problems (I think haha) was that the flask_session folder was owned by ubuntu and not www-data.  

AND BY FIXING THIS IS IS ACTUALLY FULLY WORKING WITH THE CSS SHOWING!!!!!! (After 2h in debugging hell together with ChatGPT). 
(The favicon is currently not showing for me but it was showing for a friend so I'm not worried about that at all really for now.)

Another problem was the uploads folder since it was in .gitignore haha. This was simply fixed by adding a directory to the EC2 instance with mkdir and setting the permissions for it. (It was not that easy *sigh* haha)
I tried so much here as well. 

Aaaaand... I gave up on the EC2 instance. I'm so incredibly close. But fuck this. Especially now that I found out that there are other AWS options that are serverless. 

### Web Hosting using AWS Elastic Beanstalk
(This is my first time using Beanstalk!)
After the repository had been cleaned up a bit and it was back to a working version, a Procfile was created with the following content: web: python application.py, and the Elastic Beanstalk CLI was installed using pip install awsebcli. When running pip installed, it displayed that there were dependency issues which were fixed with:  
`pip install --upgrade awscli`  
`pip install --upgrade boto3 botocore s3transfer`  

The Elastic Beanstalk application was suppoed to be initialized by running 'eb init' but this only showed yet another error message saying there was a version conflict between botocore and awsebcli. This was solved by deactivating and deleting the current virtual environment, creating a new one, and pip installing after the following to avoid dependency issues:  
`boto3==1.35.7`  
`botocore==1.35.7`  
`awscli==1.34.7`  
`awsebcli==3.20.10`  
I was not able to resolve this. The CLI is broken!!

Instead, I will use the Console version of Elastic Beanstalk. To prepare the Flask application for deployment a Procfile was created, the static repository was refactored to follow Flask stylistic guidelines (and changes was made in boilerplate.html to match) and a runtime.txt with the version of Python used was created. Everything was zipped and uploaded to Beanstalk. The EB application was set up with most values as default. Once the environment was launched and the application was up and running, I could simply use the earlier created hosted zone in Route 53 (so it was not in vain haha) to create an "A" record as an Alias pointing it directly to the Elastic Beanstalk environment. 
