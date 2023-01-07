<h1>Azur Lane Auto<h1/>
<h3>Made by cactusoftheday<h3 /><br />
Fun time ≠ grinding time

OH YEAHHHHHHHHHHHHHHHH BABY object detection for auto program soon
or not

Introduction

Problems
<h4>
While performing the object detection transfer learning training, I ran into two problems. <br />

One, I did not have enough energy to create a good dataset for the model to train on. Total losses were extremely low which leads me to think that I might have overfitted the dataset of like 10 pictures. While building a larger dataset with more variety would have been great, I didn't have enough time. <br />

Two, my GPU sucks. I initially thought that a 1060 6GB might have been enough to tackle object detection with a very basic dataset. However, it seems that the object detection training is simply too intensive. 6GB of VRAM were always in use and my CPU had to take over some of the work. Often times, I would run into a resource exhausted error which would mean my hardware just couldn't keep up. This was even after I had reduced the batch size from 64 to 6. Buy me a 4090, please? 
