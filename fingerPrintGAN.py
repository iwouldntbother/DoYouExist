import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

reconstructed_model = keras.models.load_model('models/fingerprintGAN_model')


def generateFingerprints(no=1):
    random_latent_vectors = tf.random.normal(shape=(no, 128))
    testImages = reconstructed_model(random_latent_vectors)
    testImages *= 255
    testImages = testImages.numpy()

    return testImages


def devFingerprintGen():
    prints = generateFingerprints(9)
    print(prints.shape)

    fir = plt.figure(figsize=(3, 3))

    for i in range(prints.shape[0]):
        plt.subplot(3, 3, i+1)
        plt.imshow(prints[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        plt.axis('off')
    plt.show()


# devFingerprintGen()
