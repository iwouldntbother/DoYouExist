import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import random

collagePieces_faces = './collagePieces/faces'
collagePieces_rightEyes = './collagePieces/rightEyes'
collagePieces_leftEyes = './collagePieces/leftEyes'
collagePieces_mouths = './collagePieces/mouths'

noFaces = len(next(os.walk(collagePieces_faces))[2])
noRightEyes = len(next(os.walk(collagePieces_rightEyes))[2])
noLeftEyes = len(next(os.walk(collagePieces_leftEyes))[2])
noMouths = len(next(os.walk(collagePieces_mouths))[2])

print(noFaces, noRightEyes, noLeftEyes, noMouths)


def getRandomPart(part):
    image = None
    no = None
    if part == 'face':
        no = random.randint(0, noFaces)
        image = Image.open(os.path.join(
            collagePieces_faces, 'face_'+f'{no:06}'+'.png'))
        print(no)
    elif part == 'rightEye':
        no = random.randint(0, noRightEyes)
        image = Image.open(os.path.join(
            collagePieces_rightEyes, 'rightEye_'+f'{no:06}'+'.png'))
        print(no)
    elif part == 'leftEye':
        no = random.randint(0, noLeftEyes)
        image = Image.open(os.path.join(
            collagePieces_leftEyes, 'leftEye_'+f'{no:06}'+'.png'))
        print(no)
    elif part == 'mouth':
        no = random.randint(0, noMouths)
        image = Image.open(os.path.join(
            collagePieces_mouths, 'mouth_'+f'{no:06}'+'.png'))
        print(no)

    return [image, no]

import json

def getFaceLandmarks(number):
    with open('./inputFaces/landmarks/landmarks_'+f'{number:06}'+'.json') as f:
        data = json.load(f)
    return data

def loadPoints(data, pointsArr):
    pointsToBeReturned = []
    for point in pointsArr:
        pointsToBeReturned.append(data[int(point)])
    return pointsToBeReturned

rightEyePoints = [362, 398, 384, 385, 386, 387, 388,
                  466, 263, 249, 390, 373, 374, 380, 381, 382]
leftEyePoints = [133, 173, 157, 158, 159, 160,
                 161, 246, 33, 7, 163, 144, 145, 153, 154, 155]
mouthPoints = [61, 185, 40, 39, 37, 0, 267, 269, 270,
               409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
facePoints = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 356, 454,
              323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]

faceImage, faceNo = [None, None]
rightEyeImage, rightEyeNo = [None, None]
leftEyeImage, leftEyeNo = [None, None]
mouthImage, mouthNo = [None, None]

def getAllRandomParts():
    global faceImage, faceNo, rightEyeImage, rightEyeNo, leftEyeImage, leftEyeNo, mouthImage, mouthNo
    faceImage, faceNo = getRandomPart('face')
    rightEyeImage, rightEyeNo = getRandomPart('rightEye')
    leftEyeImage, leftEyeNo = getRandomPart('leftEye')
    mouthImage, mouthNo = getRandomPart('mouth')

    pasteFeature(faceImage, 'mouth', mouthImage)

    return faceImage

def getCoords(points):
    faceLandmarks = getFaceLandmarks(faceNo)
    featurePoints = loadPoints(faceLandmarks, points)
    x, y = zip(*featurePoints)
    xMax = max(x)
    xMin = min(x)
    yMax = max(y)
    yMin = min(y)
    xC = (xMax-xMin)/2
    yC = (yMax-yMin)/2
    return [xMin, yMin, xMax, yMax, xC, yC]

def getFeature(feature):
    if feature == 'rightEye':
        return getCoords(rightEyePoints)
    elif feature == 'leftEye':
        return getCoords(leftEyePoints)
    elif feature == 'mouth':
       return getCoords(mouthPoints)
    else:
        return

def pasteFeature(faceImage, feature, featureImage):
    featureLocation = getFeature(feature)
    print(feature+' location on face: '+str(featureLocation))
    faceImage.paste(featureImage,(round(featureLocation[4]-(featureImage.size[0]/2)),round(featureLocation[5]-(featureImage.size[1]/2))))





plt.imshow(getAllRandomParts())
plt.axis('off')
plt.show()

# Need to get face landmarks for parts locations
