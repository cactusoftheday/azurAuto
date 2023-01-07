<h1>Azur Lane Auto<h1/>
<h2>Made by cactusoftheday<br />
  <h3>
Fun time ≠ grinding time

object detection for auto program soon <br>
<h5>or not
<h2>
Introduction
<h4>
As a player of Azur Lane, I am constantly on the lookout for new and powerful weapons to help me take on the toughest challenges in the game. These weapons can often be obtained by grinding through certain in-game events or challenges, but doing so can be time-consuming. At the same time, I am a huge fan of the beautiful and unique skins available for each character, and I always want to collect as many as possible. That's why I decided to create a Tensorflow model and an auto playing program to help me maximize my time in the game. With this program, I am able to progress through the game and unlock new skins and weapons more quickly, all while focusing on my other tasks. In this project, I will explain how I used Tensorflow and Python to create a program that can automatically play Azur Lane, allowing me to collect all of the best skins and gear for my shipgirls.
<h2>
  How to use this?
<h4>
  1. Clone the repository <br />
  2. download the checkpoints from this google drive folder: https://drive.google.com/drive/u/0/folders/1L4siJJDkG-b_TKoAR-yAaV256Wp-9fhL  <br />
  3. run main.py <br />
<h3>Conditions to use
  <h4>There are template matching parts in this program and thus you will need to run this on PC and in an emulator that has 1600 x 900 resolution, otherwise some of the template matching stuff won't work. Also you may need to run your IDE as administrator due to the fact that controlling the mouse with the program needs administrator privileges. 
<h2>
Problems
<h4>
While performing the object detection transfer learning training, I ran into two problems. <br />

One, I did not have enough energy to create a good dataset for the model to train on. Total losses were extremely low which leads me to think that I might have overfitted the dataset of like 10 pictures. While building a larger dataset with more variety would have been great, I didn't have enough time. <br />

Two, my GPU sucks. I initially thought that a 1060 6GB might have been enough to tackle object detection with a very basic dataset. However, it seems that the object detection training is simply too intensive. 6GB of VRAM were always in use and my CPU had to take over some of the work. Often times, I would run into a resource exhausted error which would mean my hardware just couldn't keep up. This was even after I had reduced the batch size from 64 to 6. Buy me a 4090, please? 
<br />
  
  literally me
![Essex eating glue](https://user-images.githubusercontent.com/20429572/211165776-311bacd3-2e3b-4912-a3bd-7d46e9118e43.jpg)

