import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageShow
import sys
import os
import re
import json
import matplotlib.pyplot as plt

args = []

for i in range(1, len(sys.argv)):
    args.append(sys.argv[i])

inputFace = args[0]  # dev: 000
processedFacesDirectory = './ProcessedImages/faces'

# Right eye - 16 points
# 362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382

# Left eye - 16 points
# 133, 173, 157, 158, 159, 160, 161, 246, 033, 007, 163, 144, 145, 153, 154, 155

# Mouth Points - 20 points
# 61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146

rightEyePoints = [362, 398, 384, 385, 386, 387, 388,
                  466, 263, 249, 390, 373, 374, 380, 381, 382]
leftEyePoints = [133, 173, 157, 158, 159, 160,
                 161, 246, 33, 7, 163, 144, 145, 153, 154, 155]
mouthPoints = [61, 185, 40, 39, 37, 0, 267, 269, 270,
               409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
facePoints = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 356, 454,
              323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]

print(len(mouthPoints))


def loadPoints(data, pointsArr):
    pointsToBeReturned = []
    for point in pointsArr:
        pointsToBeReturned.append(data[int(point)])
    return pointsToBeReturned


# load image
inputImage = cv2.imread(os.path.join(processedFacesDirectory,
                                     "faceImages/face_"+str(inputFace)+".jpg"))
inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)

inputPoints = []
# Load input landmarks
with open(os.path.join(processedFacesDirectory, "faceLandmarks/landmarks_"+str(inputFace)+".json")) as f:
    data = json.load(f)
    inputPoints = data

inputRightEyePoints = loadPoints(inputPoints, rightEyePoints)
inputLeftEyePoints = loadPoints(inputPoints, leftEyePoints)
inputMouthPoints = loadPoints(inputPoints, mouthPoints)


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


def findCropCoords(points):

    x, y = zip(*points)

    xMax = max(x)
    xMin = min(x)
    yMax = max(y)
    yMin = min(y)

    # xMax = np.amax(points, axis=0)[0]
    # xMin = np.amin(points, axis=0)[0]
    # # yMax = np.maximum(points)[1]
    # yMax = np.amax(points, axis=1)[1]
    # yMin = np.amin(points, axis=1)[1]
    return [xMin, yMin, xMax, yMax]


def croppedImage(image, points):
    x, y = zip(*points)
    xMax = max(x)
    xMin = min(x)
    yMax = max(y)
    yMin = min(y)
    return image.crop((xMin, yMin, xMax, yMax))


print(inputMouthPoints)
print(findCropCoords(inputMouthPoints))

x1, y1, x2, y2 = findCropCoords(inputMouthPoints)
# print(x1, y1, x2, y2)

# mouthImage = cutter(inputImage, inputMouthPoints)
# mouthDraw = ImageDraw.Draw(mouthImage)
# mouthDraw.rectangle([(x1, y1), (x2, y2)], outline='red')

# mouthImage.show()

# plt.imshow(cutter(inputImage, inputMouthPoints).crop((x1, y1, x2, y2)))
plt.imshow(cutter(inputImage, inputRightEyePoints))

# plt.axis('off')
# plt.imshow(cutter(inputImage, inputRightEyePoints))
# plt.imshow(cutter(inputImage, inputLeftEyePoints))
# plt.imshow(cutter(inputImage, inputMouthPoints))
plt.show()

plt.close()
