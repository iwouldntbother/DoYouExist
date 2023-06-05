import os
import numpy as np

from PIL import Image

original_image_dir = 'C:/Users/Will_/OneDrive - University of the Arts London/University/CCI/Final Show/completeWorkflows/workflow_0/styleGAN2_faces/original/'
resized_image_dir = 'C:/Users/Will_/OneDrive - University of the Arts London/University/CCI/Final Show/completeWorkflows/workflow_0/styleGAN2_faces/resized/'

for i in range(5000):
    image = Image.open(original_image_dir+f'{i:06}'+'.png')
    print('Loading: '+f'{i:06}'+'.png', end='\r')
    image = image.resize((512, 512), resample=Image.LANCZOS)
    print('Resized image: '+f'{i:06}', end='\r')
    image.save(resized_image_dir+f'{i:06}'+'.jpg')
    print('Saving image: '+f'{i:06}'+'.jpg')

print('5000 images resized')
