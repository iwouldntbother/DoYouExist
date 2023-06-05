import sys
import time
import cv2
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

import faceRec
import generateData

isRunning = True

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

faceVisible = False
timeFaceLastVisible = time.time()
timeFaceNotVisible = time.time()
faceProcessWaitTime = 5

coolDownStart = time.time() + 30

detecting = True


def processFace(image, bbox):
    if not type(bbox) == None:
        cropped_image = image[bbox.y:bbox.y+bbox.h, bbox.x:bbox.x+bbox.w]
        detectFace(croppedImage=cropped_image)
        # cv2.imshow("Cropped", cropped_image)
        # cv2.waitKey(0)
    return True


def detectFace(croppedImage):
    global coolDownStart

    existed, faceUUID, error = faceRec.faceRecogniser(croppedImage)

    if error:
        print('Error no encoding found in image')
        return

    # print('detectFace.py: Face existed: '+str(existed) +
        #   ' with UUID: ' + faceUUID)

    print('faceUUID: '+faceUUID)
    sys.stdout.flush()

    coolDownStart = time.time()

    if not existed:
        print('!!! I AM STILL RUNNING !!!')
        generateData.generateDataFor(faceUUID)

    return


def faceCapture(trueFalse, image=None, bbox=None):
    global faceVisible
    global timeFaceLastVisible
    global timeFaceNotVisible
    global coolDownStart

    processingReady = True

    if (trueFalse == True and faceVisible == False):
        faceVisible = True
        timeFaceNotVisible = time.time()
        print('DetectFace.py: Face visible.', end='\r')
    elif (trueFalse == False and faceVisible == True and (time.time()-timeFaceLastVisible) >= 5):
        faceVisible = False
        processingReady = True
        print('DetectFace.py: face no longer visible.', end='\r')
    elif (trueFalse == True and faceVisible == True and (time.time()-timeFaceNotVisible) >= faceProcessWaitTime and processingReady == True):
        faceVisible = False
        timeFaceLastVisible = time.time()
        processingReady = False
        processFace(image, bbox)
        print('DetectFace.py: face Processing started!')


class BoundingBox(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if (time.time()-coolDownStart) >= 30:
            print('DetectFace.py: Detecting again', end='\r')
            detecting = True
        else:
            print('DetectFace.py: Cooling down', end='\r')

        if results.detections and detecting:
            for detection in results.detections:
                if float(detection.score[0]) >= 0.75:
                    width_height = _normalized_to_pixel_coordinates(
                        detection.location_data.relative_bounding_box.width,
                        detection.location_data.relative_bounding_box.height,
                        image.shape[1],
                        image.shape[0]
                    )
                    x_y = _normalized_to_pixel_coordinates(
                        detection.location_data.relative_bounding_box.xmin,
                        detection.location_data.relative_bounding_box.ymin,
                        image.shape[1],
                        image.shape[0]
                    )

                    bbox = BoundingBox(
                        x_y[0], x_y[1], width_height[0], width_height[1])

                    if float(width_height[0]) > 100:
                        faceCapture(True, image, bbox)
                        mp_drawing.draw_detection(image, detection)
                        timeFaceLastVisible = time.time()
                    else:
                        faceCapture(False)
                else:
                    faceCapture(False)

        cv2.imshow('Face Detection', image)
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
