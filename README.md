# People-Counting-in-Real-Time
People Counting in Real-Time using live video stream/IP camera in OpenCV with support for both horizontal and vertical counting modes.

> NOTE: This is an improvement/modification to https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/

<div align="center">
<img src=https://imgur.com/SaF1kk3.gif" width=550>
<p>Live demo</p>
</div>

- The primary aim is to use the project as a business perspective, ready to scale.
- Use case: counting the number of people in the stores/buildings/shopping malls etc., in real-time.
- **NEW**: Supports both horizontal counting (people crossing vertical lines) and vertical counting (people crossing horizontal lines).
- Sending an alert to the staff if the people are way over the limit.
- Automating features and optimising the real-time stream for better performance (with threading).
- Acts as a measure towards footfall analysis and in a way to tackle COVID-19 scenarios.

--- 

## Table of Contents

* [Simple Theory](#simple-theory)
    - [SSD detector](#ssd-detector)
    - [Centroid tracker](#centroid-tracker)
* [Counting Modes](#counting-modes)
    - [Horizontal counting mode](#horizontal-counting-mode)
    - [Vertical counting mode](#vertical-counting-mode)
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

## Counting Modes

The system now supports two different counting modes to accommodate different camera orientations and use cases:

### Horizontal counting mode

- **Default mode** (triggered with `-M h` or `--mode h`)
- People are counted when they cross a **vertical line** in the center of the frame
- Suitable for monitoring doorways, corridors, or passages where people move left-to-right or right-to-left
- The prediction border appears as a vertical red line in the center of the frame
- **Left movement**: People moving from right to left (counted as "up/left") 
- **Right movement**: People moving from left to right (counted as "down/right")

### Vertical counting mode

- Triggered with `-M v` or `--mode v`
- People are counted when they cross a **horizontal line** in the center of the frame  
- Suitable for monitoring stairs, escalators, or passages where people move up-and-down
- The prediction border appears as a horizontal red line in the center of the frame
- **Up movement**: People moving from bottom to top (counted as "up")
- **Down movement**: People moving from top to bottom (counted as "down")

**Usage Examples:**
```bash
# Horizontal counting (default)
python people_counter.py --mode h

# Vertical counting  
python people_counter.py --mode v
```

---

## Running Inference

### Install the dependencies

First up, install all the required Python dependencies by running: ```
pip install -r requirements.txt ```

> NOTE: Supported Python version is 3.11.3 (there can always be version conflicts between the dependencies, OS, hardware etc.).

### Test video file

To run inference on a test video file, head into the root directory and run the command: 

```
python people_counter.py --input utils/data/tests/test_1.mp4
```

> NOTE: The system now uses improved MobileNet models by default (`mobilenet_iter_73000_deploy.prototxt` and `mobilenet_iter_73000.caffemodel`) with higher confidence threshold (0.8) for better accuracy.

**Advanced usage with custom parameters:**
```
python people_counter.py --input utils/data/tests/test_1.mp4 --mode h --confidence 0.8 --width 500 --eps 5
```

### Webcam

To run on a webcam, set ```"url": 0``` in ```utils/config.json``` and run the command:

```
python people_counter.py
```

**With counting mode selection:**
```
python people_counter.py --mode v  # for vertical counting
python people_counter.py --mode h  # for horizontal counting (default)
```

### IP camera

To run on an IP camera, setup your camera url in ```utils/config.json```, e.g., ```"url": 'http://191.138.0.100:8040/video'```.

Then run the command:
```
python people_counter.py
```

**With custom parameters:**
```
python people_counter.py --mode h --width 600 --confidence 0.7
```

### Command Line Arguments

The system supports various command line arguments for customization:

| Argument | Short | Default | Description |
|----------|-------|---------|-------------|
| `--prototxt` | `-p` | `detector/mobilenet_iter_73000_deploy.prototxt` | Path to Caffe deploy prototxt file |
| `--model` | `-m` | `detector/mobilenet_iter_73000.caffemodel` | Path to Caffe pre-trained model |
| `--input` | `-i` | - | Path to optional input video file |
| `--output` | `-o` | - | Path to optional output video file |
| `--confidence` | `-c` | `0.8` | Minimum probability to filter weak detections |
| `--skip-frames` | `-s` | `30` | Number of skip frames between detections |
| `--skip-frames-tracking` | `-st` | `2` | Number of skip frames between tracking |
| `--eps` | `-e` | `5` | Error tolerance for tracking algorithm |
| `--mode` | `-M` | `h` | Counting mode: 'v' for vertical, 'h' for horizontal |
| `--width` | `-w` | `500` | Resize frame to specified width before processing |

---

## Features

The following features can be easily enabled/disabled in ```utils/config.json```:

```json
{
    "Email_Send": "",
    "Email_Receive": "",
    "Email_Password": "",
    "url": "",
    "ALERT": false,
    "Threshold": 10,
    "Thread": false,
    "Log": false,
    "Scheduler": false,
    "Timer": false
}
```

### Enhanced Visualization

The system now includes improved visual feedback for better monitoring:

- **Prediction Border**: A red line (horizontal or vertical) shows the counting boundary
  - Horizontal mode: Vertical red line in the center  
  - Vertical mode: Horizontal red line in the center
- **Bounding Boxes**: Green rectangles are drawn around all detected people in real-time
- **Directional Labels**: Console output shows movement direction ("up/left" or "down/right") 
- **Improved Text Positioning**: Better placement and color contrast for on-screen information
- **Configurable Frame Width**: Resize processing frame for optimal performance (`--width` parameter)

### Real-Time alert

If selected, we send an email alert in real-time. Example use case: If the total number of people (say 10 or 30) are exceeded in a store/building, we simply alert the staff. 

- You can set the max. people limit in config, e.g., ```"Threshold": 10```.
- This is quite useful considering scenarios similar to COVID-19. Below is an example:
<img src="https://imgur.com/35Yf1SR.png" width=350>

> ***1. Setup your emails:***

In the config, setup your sender email ```"Email_Send": ""``` to send the alerts and your receiver email ```"Email_Receive": ""``` to receive the alerts.

> ***2. Setup your password:***

Similarly, setup the sender email password ```"Email_Password": ""```.

Note that the password varies if you have secured 2 step verification turned on, so refer the links below and create an application specific password:

- Google mail has a guide here: https://myaccount.google.com/lesssecureapps
- For 2 step verified accounts: https://support.google.com/accounts/answer/185833

### Threading

- Multi-Threading is implemented in ```utils/thread.py```. If you ever see a lag/delay in your real-time stream, consider using it.
- Threading removes ```OpenCV's internal buffer``` (which basically stores the new frames yet to be processed until your system processes the old frames) and thus reduces the lag/increases fps.
- If your system is not capable of simultaneously processing and outputting the result, you might see a delay in the stream. This is where threading comes into action.
- It is most suitable to get solid performance on complex real-time applications. To use threading: set ```"Thread": true,``` in config.

### Scheduler

- Automatic scheduler to start the software. Configure to run at every second, minute, day, or workdays e.g., Monday to Friday.
- This is extremely useful in a business scenario, for instance, you could run the people counter only at your desired time (maybe 9-5?).
- Variables and any cache/memory would be reset, thus, less load on your machine.

```python
# runs at every day (09:00 am)
schedule.every().day.at("9:00").do(run)
```

### Timer

- Configure stopping the software execution after a certain time, e.g., 30 min or 8 hours (currently set) from now.
- All you have to do is set your desired time and run the script.

```python
# automatic timer to stop the live stream (set to 8 hours/28800s)
end_time = time.time()
num_seconds = (end_time - start_time)
if num_seconds > 28800:
    break
```

### Simple log

- Logs the counting data at end of the day.
- Useful for footfall analysis. Below is an example:
<img src="https://imgur.com/CV2nCjx.png" width=400>

---

## References

***Main:***

- SSD paper: https://arxiv.org/abs/1512.02325
- MobileNets paper: https://arxiv.org/abs/1704.04861
- Centroid tracker: https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

***Optional:***

- Object detection with SSD/MobileNets: https://pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/
- Schedule: https://pypi.org/project/schedule/

---

*saimj7/ 19-08-2020 - © <a href="http://saimj7.github.io" target="_blank">Sai_Mj</a>.*
