# People-Counting-in-Real-Time
People Counting in Real-Time using live video stream/IP camera in OpenCV.

> NOTE: This is an improvement/modification to https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/

<div align="center">
<img src=https://imgur.com/SaF1kk3.gif" width=550>
<p>Live demo</p>
</div>

- The primary aim is to use the project as a business perspective, ready to scale.
- Use case: counting the number of people in the stores/buildings/shopping malls etc., in real-time.
- Sending an alert to the staff if the people are way over the limit.
- Automating features and optimising the real-time stream for better performance (with threading).
- Acts as a measure towards footfall analysis and in a way to tackle COVID-19 scenarios.

--- 

## Table of Contents

* [Simple Theory](#simple-theory)
    - [SSD detector](#ssd-detector)
    - [Centroid tracker](#centroid-tracker)
* [Running Inference](#running-inference)
    - [Install the dependencies](#install-the-dependencies)
    - [Test video file](#test-video-file)
    - [Webcam](#webcam)
    - [IP camera](#ip-camera)
* [Features](#features)
    - [Real-Time alert](#real-time-alert)
    - [Threading](#threading)
    - [Scheduler](#scheduler)
    - [Timer](#timer)
    - [Simple log](#simple-log)
* [References](#references)

---

## Simple Theory

### SSD detector

- We are using a SSD ```Single Shot Detector``` with a MobileNet architecture. In general, it only takes a single shot to detect whatever is in an image. That is, one for generating region proposals, one for detecting the object of each proposal. 
- Compared to other two shot detectors like R-CNN, SSD is quite fast.
- ```MobileNet```, as the name implies, is a DNN designed to run on resource constrained devices. For e.g., mobiles, ip cameras, scanners etc.
- Thus, SSD seasoned with a MobileNet should theoretically result in a faster, more efficient object detector.

### Centroid tracker

- Centroid tracker is one of the most reliable trackers out there.
- To be straightforward, the centroid tracker computes the ```centroid``` of the bounding boxes.
- That is, the bounding boxes are ```(x, y)``` co-ordinates of the objects in an image. 
- Once the co-ordinates are obtained by our SSD, the tracker computes the centroid (center) of the box. In other words, the center of an object.
- Then an ```unique ID``` is assigned to every particular object deteced, for tracking over the sequence of frames.

---

## Running Inference

### Install the dependencies

First up, install all the required Python dependencies by running: ```
pip install -r requirements.txt ```

> Note that there can always be version conflicts between the dependencies themselves and other factors like OS, hardware etc.

### Test video file

To run inference on a test video file, head into the directory/use the command: 

```
python people_counter.py --prototxt detector/MobileNetSSD_deploy.prototxt --model detector/MobileNetSSD_deploy.caffemodel --input utils/data/tests/test_1.mp4
```

### Webcam

To run inference on a webcam, set ```url = 0``` in ```utils/config.py``` and run the command:

```
python people_counter.py --prototxt detector/MobileNetSSD_deploy.prototxt --model detector/MobileNetSSD_deploy.caffemodel
```

### IP camera

To run inference on an IP camera, setup your camera url in ```utils/config.py```:

```
# Enter the ip camera url (e.g., url = 'http://191.138.0.100:8040/video')
url = ''
```
Then run the command:
```
python people_counter.py --prototxt detector/MobileNetSSD_deploy.prototxt --model detector/MobileNetSSD_deploy.caffemodel
```

---

## Features

The following features can be easily enabled/disabled in ```utils/config.py```:

<img src="https://imgur.com/Lr8mdUW.png" width=500>

### Real-Time alert

- If selected, we send an email alert in real-time. Example use case: If the total number of people (say 10 or 30) are exceeded in a store/building, we simply alert the staff. 
- You can set the max. people limit in config. e.g., ``` Threshold = 10 ```.
- This is quite useful considering scenarios similar to COVID-19. 
<img src="https://imgur.com/35Yf1SR.png" width=350>

- Note: To setup the sender email, please refer the instructions inside ```utils/mailer.py```. Setup receiver email in the config.

### Threading

- Multi-Threading is implemented in ```utils/thread.py```. If you ever see a lag/delay in your real-time stream, consider using it.
- Threading removes ```OpenCV's internal buffer``` (which basically stores the new frames yet to be processed until your system processes the old frames) and thus reduces the lag/increases fps.
- If your system is not capable of simultaneously processing and outputting the result, you might see a delay in the stream. This is where threading comes into action.
- It is most suitable to get solid performance on complex real-time applications. To use threading: set ``` Thread = True ``` in config.

### Scheduler

- Automatic scheduler to start the software. Configure to run at every second, minute, day, or workdays e.g., Monday to Friday.
- This is extremely useful in a business scenario, for instance, you could run the people counter only at your desired time (maybe 9-5?).
- Variables and any cache/memory would be reset, thus, less load on your machine.

```
# runs at every day (09:00 am)
schedule.every().day.at("9:00").do(run)
```

### Timer

- Configure stopping the software execution after a certain time, e.g., 30 min or 8 hours (currently set) from now.
- All you have to do is set your desired time and run the script.

```
if Timer:
	# Automatic timer to stop the live stream. Set to 8 hours (28800s).
	t1 = time.time()
	num_seconds=(t1-t0)
	if num_seconds > 28800:
		break
```

### Simple log

- Logs the counting data at end of the day.
- Useful for footfall analysis.
<img src="https://imgur.com/CV2nCjx.png" width=400>

---

## References

***Main:***

- SSD paper: https://arxiv.org/abs/1512.02325
- MobileNet paper: https://arxiv.org/abs/1704.04861
- Centroid tracker: https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

***Optional:***

- SSD: https://towardsdatascience.com/review-ssd-single-shot-detector-object-detection-851a94607d11
- Schedule: https://pypi.org/project/schedule/

---

saimj7/ 19-08-2020 © <a href="http://saimj7.github.io" target="_blank">Sai_Mj</a>.
