import numpy as np
import face_recognition
import os
import pickle
import uuid
import cv2
import matplotlib.pyplot as plt

import personalData

knownFaceEncodings = []
knownFaceUUIDs = []


def loadKnownFaceEncodings():
    global knownFaceEncodings
    global knownFaceUUIDs
    # Load encodings and UUIDs from pickle file
    # currentDatabase = personalData.getDatabase()
    # tempEncodings = []
    # tempUUIDs = []
    # for person in currentDatabase:
    #     tempEncodings.append(person.faceEncodings)
    #     tempUUIDs.append(person.uuid)
    # knownFaceEncodings = tempEncodings
    # knownFaceUUIDs = tempUUIDs

    knownFaceEncodings, knownFaceUUIDs = personalData.getEncodingsAndUUIDs()

    print('FaceRec.py: Loaded ' +
          str(len(knownFaceEncodings)) + ' face encodings and ' +
          str(len(knownFaceUUIDs)) + ' UUIDs')
    return


def faceRecogniser(image):

    loadKnownFaceEncodings()

    # print(type(image), image.shape)

    # fixed_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    # rgb_fixed_image = cv2.cvtColor(fixed_image, cv2.COLOR_BGR2RGB)

    rgb_fixed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # plt.imshow(image)
    # plt.imshow(rgb_fixed_image)
    # plt.axis('off')
    # plt.show()

    # print(type(rgb_fixed_image), rgb_fixed_image.shape)

    face_encoding = face_recognition.face_encodings(rgb_fixed_image)
    if (face_encoding):
        face_encoding = face_encoding[0]
    else:
        # print('encodings empty')
        return [None, None, True]
    face_id = uuid.uuid4()

    matches = face_recognition.compare_faces(knownFaceEncodings, face_encoding)

    if True in matches:
        # if face encoding matches one from list, return True and UUID
        first_match_index = matches.index(True)
        print('FaceRec.py: Face matches a known face!')
        return [True, knownFaceUUIDs[first_match_index], False]

    # if face encoding doesn't match, save face encoding and new face UUID, return False and new UUID
    personalData.createNewPerson(str(face_id), face_encoding)
    return [False, str(face_id), False]
