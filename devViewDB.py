import pickle
import os
import personalData

databaseDirectory = './database/'

devDB = []


with open(os.path.join(databaseDirectory, 'main_db.pkl'), 'rb') as f:
    data = pickle.load(f)
    for dataPoint in data:
        print(vars(dataPoint))
