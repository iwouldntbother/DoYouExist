# PIL Image to base64 string
import matplotlib.pyplot as plt
import fingerPrintGAN
import base64
from PIL import Image
import numpy as np


from io import BytesIO


def pilImageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return 'data:image/jpeg;base64,' + img_str.decode('utf-8')


def pltImageToBase64(image):
    mat = image[:, :, 0] * 127.5+127.5
    buffered = BytesIO()
    plt.axis('off')
    plt.imshow(mat, cmap='gray')
    plt.savefig(buffered, format='jpg')
    buffered.seek(0)

    return 'data:image/jpeg;base64,' + base64.b64encode(buffered.read()).decode('utf-8')


# PIL Image
# styleGAN2_faces/resized/000000.jpg
# input_image = Image.open('styleGAN2_faces/resized/000001.jpg')
input_image = fingerPrintGAN.generateFingerprints()
print(type(input_image), input_image.shape)


# Base64 String
for in_img in input_image:
    mat = in_img[:, :, 0] * 127.5+127.5
    base64_string = pltImageToBase64(mat)
    print(base64_string)

# prints[i, :, :, 0] * 127.5 + 127.5

# with open('dev_base64_image.txt', 'w') as f:
#     f.write(base64_string)

print('Done')
