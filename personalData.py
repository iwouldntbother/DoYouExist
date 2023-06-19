import numpy as np
import generateData
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import json
import os
import pickle

databaseDirectory = './database/'


class PersonData(object):
    def __init__(self, uuid, faceEncodings):
        self.uuid = uuid
        self.faceEncodings = faceEncodings
        self.name = ''
        self.phone_number = ''
        self.occupation = ''
        self.address = ''
        self.last_location = ()
        self.date_of_birth = ''
        self.bank_card = ''
        self.fingerprints = []
        self.face_image = Image.new(mode='L', size=(512, 512))


currentDatabase = []


def getDatabase():
    global currentDatabase
    with open(os.path.join(databaseDirectory, 'main_db.pkl'), 'rb') as f:
        # newCurrentDatabase = []
        data = pickle.load(f)
        currentDatabase = []
        for dataPoint in data:
            currentDatabase.append(dataPoint)
        # currentDatabase = newCurrentDatabase
    return currentDatabase


def getEncodingsAndUUIDs():
    global currentDatabase
    getDatabase()
    faceEncodings = []
    faceUUIDs = []
    for item in currentDatabase:
        faceEncodings.append(item.faceEncodings)
        faceUUIDs.append(str(item.uuid))
    return [faceEncodings, faceUUIDs]


def writeDatabase():
    global currentDatabase
    with open(os.path.join(databaseDirectory, 'main_db.pkl'), 'wb') as f:
        pickle.dump(currentDatabase, f, pickle.HIGHEST_PROTOCOL)
    return


def pilImageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    buffered.close()
    # image.close()

    return 'data:image/jpeg;base64,' + img_str.decode('utf-8')


def pltImageToBase64(image):
    mat = image[:, :, 0] * 127.5+127.5
    buffered = BytesIO()
    plt.axis('off')
    plt.imshow(mat, cmap='gray')
    plt.savefig(buffered, format='jpg')
    buffered.seek(0)
    plt.close()

    return 'data:image/jpeg;base64,' + base64.b64encode(buffered.read()).decode('utf-8')


def writeJSON():
    global currentDatabase
    getDatabase()
    with open(os.path.join(databaseDirectory, 'json_db.json'), 'w') as f:
        dataToWrite = []
        # print(len(currentDatabase))
        for item in currentDatabase:
            # print(type(item.face_image))
            jsonReady = {
                "uuid": str(item.uuid),
                # "faceEncodings": item.faceEncodings.tolist(),
                "name": item.name,
                "phone_number": item.phone_number,
                "occupation": item.occupation,
                "address": item.address,
                "last_location": item.last_location,
                "date_of_birth": item.date_of_birth,
                "bank_card": item.bank_card,
                "fingerprints": [pltImageToBase64(fingerprint) for fingerprint in item.fingerprints],
                "face_image": pilImageToBase64(item.face_image),
            }
            dataToWrite.append(jsonReady)
        json.dump(dataToWrite, f)


def getPersonData(uuid):
    global currentDatabase
    getDatabase()
    personData = next(
        (item for item in currentDatabase if item.uuid == uuid), None)
    return personData


def updatePersonData(uuid, newPersonData):
    global currentDatabase
    personDataIndex = next((i for i, item in enumerate(
        currentDatabase) if item.uuid == uuid), None)
    currentDatabase[personDataIndex] = newPersonData
    writeDatabase()
    writeJSON()
    return


def createNewPerson(uuid, faceEncoding):
    global currentDatabase
    newPerson = PersonData(uuid, faceEncoding)
    currentDatabase.append(newPerson)
    writeDatabase()
    writeJSON()

    generateData.generateDataFor(uuid)
    return
