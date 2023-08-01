import argparse
import json
import logging
import time

import cv2
import imutils
import numpy as np

# execution start time
start_time = time.time()
# setup logger
logging.basicConfig(level=logging.INFO, format="[INFO] %(message)s")
logger = logging.getLogger(__name__)
# initiate features config.
with open("utils/config.json", "r") as file:
    config = json.load(file)

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def parse_arguments():
    # function to parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p", "--prototxt", required=False, help="path to Caffe 'deploy' prototxt file"
    )
    ap.add_argument(
        "-m", "--model", required=True, help="path to Caffe pre-trained model"
    )
    ap.add_argument("-i", "--input", type=str, help="path to optional input video file")
    ap.add_argument(
        "-o", "--output", type=str, help="path to optional output video file"
    )
    # confidence default 0.4
    ap.add_argument(
        "-c",
        "--confidence",
        type=float,
        default=0.5,
        help="minimum probability to filter weak detections",
    )
    ap.add_argument(
        "-s",
        "--skip-frames",
        type=int,
        default=2,
        help="# of skip frames between detections",
    )
    return vars(ap.parse_args())


def people_counter():
    # main function for people_counter.py
    args = parse_arguments()
    logger.info("Starting the video..")
    vs = cv2.VideoCapture(0)
    people_counter_nn(args, vs)
    # close any open windows
    cv2.destroyAllWindows()


def people_counter_nn(args, vs):
    # initialize the list of class labels MobileNet SSD was trained to detect
    CLASSES = [
        "background",
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "pottedplant",
        "sheep",
        "sofa",
        "train",
        "tvmonitor",
    ]

    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # initialize the frame dimensions (we'll set them as soon as we read
    # the first frame from the video)
    frame_width = None
    frame_height = None

    # initialize the total number of frames processed thus far, along
    # with the total number of objects that have moved either up or down
    total_frames = 0

    detections = None

    # loop over frames from the video stream
    while True:

        # grab the next frame and handle if we are reading from either
        # VideoCapture or VideoStream
        ret, frame = vs.read()
        if not ret:
            continue

        # resize the frame to have a maximum width of 500 pixels (the
        # fewer data we have, the faster we can process it)
        frame = imutils.resize(frame, width=500)

        # if the frame dimensions are empty, set them
        if frame_width is None or frame_height is None:
            (frame_height, frame_width) = frame.shape[:2]

        detections = detect_objects_nn(
            args, detections, frame, frame_height, frame_width, net, total_frames
        )

        in_pic = count_people_detected(
            CLASSES, args, detections, frame, frame_height, frame_width
        )

        cv2.putText(
            frame,
            f"People detected: {in_pic}",
            (10, frame_height - (20 + 200)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            2,
        )

        # show the output frame
        cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        # increment the total number of frames processed thus far
        total_frames += 1


def count_people_detected(CLASSES, args, detections, frame, frame_height, frame_width):
    detected = 0
    # loop over the detections
    if detections is not None:
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detections[0, 0, i, 2]

            if confidence <= args["confidence"]:
                continue

            # extract the index of the class label from the
            # detections list
            idx = int(detections[0, 0, i, 1])

            # if the class label is not a person, ignore it
            if CLASSES[idx] != "person":
                continue
            detected += 1
            # compute the (x, y)-coordinates of the bounding box
            # for the object
            box = detections[0, 0, i, 3:7] * np.array(
                [frame_width, frame_height, frame_width, frame_height]
            )
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
    return detected


def detect_objects_nn(
    args, detections, frame, frame_height, frame_width, net, total_frames
):
    # check to see if we should run a more computationally expensive
    # object detection method to aid our tracker
    if total_frames % args["skip_frames"] == 0:
        # set the status and initialize our new set of object trackers
        # convert the frame to a blob and pass the blob through the
        # network and obtain the detections
        blob = cv2.dnn.blobFromImage(
            frame, 0.007843, (frame_width, frame_height), 127.5
        )
        net.setInput(blob)
        detections = net.forward()
    return detections


def simple():
    """Sanity check for OpenCV and camera"""
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if success:
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF in [ord("z"), ord("q")]:
            break

    cap.release()
    cv2.destroyAllWindows()


people_counter()
