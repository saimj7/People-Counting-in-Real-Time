# People-Counting-in-Real-Time
People Counting in Real-Time using live video stream/IP camera in OpenCV.

> This is an improvement/modification to https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/

> Refer to added [Features](#features). Also, added support for an IP camera.

<div align="center">
<img src=https://imgur.com/tZYiOkt.gif" width=600>
<p>Live demo</p>
</div>

- The primary aim is to use the project as a business perspective, ready to scale.
- Use case: counting the number of people in the stores/buildings/shopping malls etc., in real-time.
- Sending an alert to the staff if the people are way over the limit.
- Automating features and optimising the real-time stream for better performance (with threading).
- Acts as a measure towards footfall analysis and in a way to tackle COVID-19.

--- 

## Table of Contents
* [Simple Theory](#simple-theory)
* [Running Inference](#running-inference)
* [Features](#features)
* [References](#references)
* [Next Steps](#next-steps)

## Simple Theory
**SSD detector:**
- We are using a SSD (Single Shot Detector) with a MobileNet architecture. In general, it only takes a single shot to detect whatever is in an image. That is, one for generating region proposals, one for detecting the object of each proposal. 
- Compared to other 2 shot detectors like R-CNN, SSD is quite fast.
- MobileNet, as the name implies, is a DNN designed to run on resource constrained devices. For example, mobiles, ip cameras, scanners etc.
- Thus, SSD seasoned with a MobileNet should theoretically result in a faster, more efficient object detector.
---
**Centroid tracker:**
- Centroid tracker is one of the most reliable trackers out there.
- To be straightforward, the centroid tracker computes the centroid of the bounding boxes.
- That is, the bounding boxes are (x, y) co-ordinates of the objects in an image. 
- Once the co-ordinates are obtained by our SSD, the tracker computes the centroid (center) of the box. In other words, the center of an object.
- Then an unique ID is assigned to every particular object deteced, for tracking over the sequence of frames.

## Running Inference
- Install all the required Python dependencies:
```
pip install -r requirements.txt
```
- To run inference on a test video file, head into the directory/use the command: 
```
python run.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --input videos/example_01.mp4
```
> To run inference on an IP camera:
- Setup your camera url in 'mylib/config.py':

```
# Enter the ip camera url (e.g., url = 'http://191.138.0.100:8040/video')
url = ''
```
- Then run with the command:
```
python run.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel
```

## Features
The following are the added features. Note: You can easily on/off them in the config. options (mylib/config.py):

<img src="https://imgur.com/Lr8mdUW.png" width=500>

***1. Real-Time alert:***
- If selected, we send an email alert in real-time. Use case: If the total number of people (say 30) exceeded in a store/building, we simply alert the staff. 
- This is pretty useful considering the COVID-19 scenario. 
<img src="https://imgur.com/35Yf1SR.png" width=350>

- Note: To setup the sender email, please refer the instructions inside 'mylib/mailer.py'. Setup receiver email in the config.


***2. Threading:***
- Multi-Threading is implemented in 'mylib/thread.py'. If you ever see a lag/delay in your real-time stream, consider using it.
- Threading removes OpenCV's internal buffer (which basically stores the new frames yet to be processed until your system processes the old frames) and thus reduces the lag/increases fps. 
- If your system is not capable of simultaneously processing and outputting the result, you might see a delay in the stream. This is where threading comes into action.
- It is most suitable for solid performance on complex real-time applications. To use threading:

``` set Thread = True in config. ```


***3. Scheduler:***
- Automatic scheduler to start the software. Configure to run at every second, minute, day, or Monday to Friday.
- This is extremely useful in a business scenario, for instance, you can run it only at your desired time (9-5?).
- Variables and memory would be reset == less load on your machine.

```
##Runs at every day (9:00 am). You can change it.
schedule.every().day.at("9:00").do(run)
```

***4. Timer:***
- Configure stopping the software after a certain time, e.g., 30 min or 9 hours from now.
- All you have to do is set your desired time and run the script.

```
if Timer:
	# Automatic timer to stop the live stream. Set to 8 hours (28800s).
	t1 = time.time()
	num_seconds=(t1-t0)
	if num_seconds > 28800:
		break
```

***5. Simple log:***
- Logs all data at end of the day.
- Useful for footfall analysis.
<img src="https://imgur.com/CV2nCjx.png" width=400>

## References
***Main:***
- SSD paper: https://arxiv.org/abs/1512.02325
- MobileNet paper: https://arxiv.org/abs/1704.04861
- Centroid tracker: https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

***Optional:***
- https://towardsdatascience.com/review-ssd-single-shot-detector-object-detection-851a94607d11
- https://pypi.org/project/schedule/

## Next steps
- Train the SSD on human data (with a top-down view).
- Experiment with other detectors and benchmark the results on computationally less expensive embedded hardware. 
- Evaluate the performance on multiple IP cameras.

<p>&nbsp;</p>

---

## Thanks for the read & have fun!

> To get started/contribute quickly (optional) ...

- **Option 1**
    - 🍴 Fork this repo and pull request!

- **Option 2**
    - 👯 Clone this repo:
    ```
    $ git clone https://github.com/saimj7/People-Counting-in-Real-Time.git
    ```

- **Roll it!**

---

saimj7/ 19-08-2020 © <a href="http://saimj7.github.io" target="_blank">Sai_Mj</a>.
