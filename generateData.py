import numpy as np
import fingerPrintGAN
import personalData
import json
import random
from PIL import Image
from faker import Faker

fake = Faker('en_GB')


def generate_fake_uk_phone_number():
    number = "07" + "".join(random.choice("0123456789") for _ in range(9))
    return number


def generateDataFor(uuid):
    personData = personalData.getPersonData(uuid)
    personData.name = fake.name()
    personData.phone_number = generate_fake_uk_phone_number()
    personData.occupation = fake.job()
    personData.address = fake.address()
    personData.last_location = fake.location_on_land()
    personData.date_of_birth = fake.date_between(
        start_date='-90y', end_date='-16y').strftime("%d/%m/%Y")
    personData.bank_card = fake.credit_card_full().split('\n')[:-1]
    personData.bank_card[1] = personData.name
    personData.fingerprints = fingerPrintGAN.generateFingerprints(8)
    personData.face_image = Image.open(
        './styleGAN2_faces/resized/'+getNewFace()+'.jpg')

    personalData.updatePersonData(uuid, personData)


def checkFaceUsed():
    with open('./styleGAN2_faces/resized/used.json', 'r') as f:
        used_list = json.load(f)
        return used_list


def updateUsedList(number):
    used_list = []

    with open('./styleGAN2_faces/resized/used.json', 'r') as f:
        used_list = json.load(f)

    if number not in used_list:
        used_list.append(number)

    with open('./styleGAN2_faces/resized/used.json', 'w') as f:
        json.dump(used_list, f)


def getNewFace():
    used_list = checkFaceUsed()
    faceNo = random.randint(0, 4999)

    while str(f'{faceNo:06}') in used_list:
        faceNo = random.randint(0, 4999)

    if str(f'{faceNo:06}') not in used_list:
        updateUsedList(str(f'{faceNo:06}'))
        return str(f'{faceNo:06}')
