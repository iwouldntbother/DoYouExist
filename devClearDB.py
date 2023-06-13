import json
import pickle
import os

import personalData

databaseDirectory = './database/'

devDB = []


with open(os.path.join(databaseDirectory, 'main_db.pkl'), 'wb') as f:
    pickle.dump(devDB, f, pickle.HIGHEST_PROTOCOL)
    print('DEV: Created the database')

print(len(personalData.getDatabase()))

personalData.writeJSON()

with open('./styleGAN2_faces/resized/used.json', 'w') as f:
    json.dump([], f)
