import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt
import json

inputFaceDirectory = 'C:/Users/Will_/OneDrive - University of the Arts London/University/CCI/Final Show/completeWorkflows/workflow_0/inputFaces'

processedDirectory_faces = './collagePieces/faces'
processedDirectory_rightEyes = './collagePieces/rightEyes'
processedDirectory_leftEyes = './collagePieces/leftEyes'
processedDirectory_mouths = './collagePieces/mouths'

rightEyePoints = [362, 398, 384, 385, 386, 387, 388,
                  466, 263, 249, 390, 373, 374, 380, 381, 382]
leftEyePoints = [133, 173, 157, 158, 159, 160,
                 161, 246, 33, 7, 163, 144, 145, 153, 154, 155]
mouthPoints = [61, 185, 40, 39, 37, 0, 267, 269, 270,
               409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
facePoints = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 356, 454,
              323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]


inputFacesAndLandmarks = []


def loadImageAndPoints(inputNumber):
    # load image
    inputImage = cv2.imread(
        (inputFaceDirectory+"/faces/face_"+str(inputNumber)+".jpg"))
    inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)

    inputPoints = []
    # Load input landmarks
    with open((inputFaceDirectory+"/landmarks/landmarks_"+str(inputNumber)+".json")) as f:
        data = json.load(f)
        inputPoints = data

    return (inputImage, inputPoints)


def loadPoints(data, pointsArr):
    pointsToBeReturned = []
    for point in pointsArr:
        pointsToBeReturned.append(data[int(point)])
    return pointsToBeReturned


def cutter(image, points, crop=True):
    imageArray = np.asarray(image)
    maskImage = Image.new('L', (image.shape[1], image.shape[0]), 0)

    ImageDraw.Draw(maskImage).polygon(
        np.array(points).astype(np.float32), outline=1, fill=1
    )
    maskArray = np.array(maskImage)

    outputImageArray = np.zeros(
        [image.shape[0], image.shape[1], 3], dtype='uint8')

    outputImageArray[:, :, :3] = imageArray[:, :, :3]
    maskArray = maskArray[:, :, None]
    outputImageArray[:, :, :3] = maskArray * 255

    outputMask = Image.composite(Image.fromarray(imageArray, "RGB"), Image.fromarray(
        outputImageArray, "RGB"), maskImage).convert('L')

    outputImage = Image.fromarray(imageArray, "RGB")
    outputImage.putalpha(outputMask)

    if crop:
        return croppedImage(outputImage, points)
    else:
        return outputImage


def croppedImage(image, points):
    x, y = zip(*points)
    xMax = max(x)
    xMin = min(x)
    yMax = max(y)
    yMin = min(y)
    return image.crop((xMin, yMin, xMax, yMax))


inputImageNumber = 50000

# inputImageNumber = len(
#     next(os.walk(inputFaceDirectory+'/faceImages'))[2])

print('Faces to cut and crop: '+str(inputImageNumber))


def cutAllParts():

    for i in range(inputImageNumber):
        inputFacesAndLandmarks.append(loadImageAndPoints(f'{i:06}'))
        print('Loading face: '+f'{i:06}' + ' Total: ' +
              str(round((i / inputImageNumber) * 100)) + '%', end='\r')
    print('All faces and landmarks loaded')
    print('')

    counter = 0
    for face, landmarks in inputFacesAndLandmarks:

        inputRightEyePoints = loadPoints(landmarks, rightEyePoints)
        inputLeftEyePoints = loadPoints(landmarks, leftEyePoints)
        inputMouthPoints = loadPoints(landmarks, mouthPoints)
        inputFacePoints = loadPoints(landmarks, facePoints)

        # Face
        faceCutout = cutter(face, inputFacePoints, crop=False)
        faceCutout.save(processedDirectory_faces +
                        '/face_'+f'{counter:06}'+'.png')

        # Right eye
        rightEye = cutter(face, inputRightEyePoints)
        rightEye.save(processedDirectory_rightEyes +
                      '/rightEye_'+f'{counter:06}'+'.png')

        # Left eye
        leftEye = cutter(face, inputLeftEyePoints)
        leftEye.save(processedDirectory_leftEyes +
                     '/leftEye_'+f'{counter:06}'+'.png')

        # Mouth
        mouth = cutter(face, inputMouthPoints)
        mouth.save(processedDirectory_mouths+'/mouth_'+f'{counter:06}'+'.png')

        print('Saved parts for: ' + f'{counter:06}', end='\r')
        counter = counter + 1


cutAllParts()

print('Finished processing '+str(inputImageNumber)+' faces!')
