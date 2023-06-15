import personalData
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from escpos.printer import Serial
import sys


def getFigure(userData):
    axd = plt.figure(layout='constrained', figsize=(6, 4), dpi=88).subplot_mosaic(
        '''
        AAAABC
        AAAADE
        AAAAFG
        AAAAHI
        '''
    )

    face_image = userData.face_image
    face_image.thumbnail((352, 352), Image.Resampling.LANCZOS)
    # face_image_crop = face_image.crop(
    #     (8, 0, face_image.size[0]-8, face_image.size[1]))

    axd['A'].imshow(face_image)
    axd['A'].axis('off')

    fingerprintIDs = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    for i in range(userData.fingerprints.shape[0]):
        axd[fingerprintIDs[i]].imshow(
            userData.fingerprints[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        axd[fingerprintIDs[i]].axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    final_image = Image.open(buffer)
    final_image.thumbnail((512, 352), Image.Resampling.LANCZOS)
    return final_image


def printProfileDev(userData):
    print('______ _____  __   _______ _   _   _______   _______ _____ _____ ___          ')
    print('|  _  \\  _  | \\ \\ / /  _  | | | | |  ___\\ \\ / /_   _/  ___|_   _|__ \\   ')
    print('| | | | | | |  \\ V /| | | | | | | | |__  \\ V /  | | \\ `--.  | |    ) |     ')
    print('| | | | | | |   \\ / | | | | | | | |  __| /   \\  | |  `--. \\ | |   / /      ')
    print('| |/ /\\ \\_/ /   | | \\ \\_/ / |_| | | |___/ /^\\ \\_| |_/\\__/ / | |  |_|   ')
    print('|___/  \\___/    \\_/  \\___/ \\___/  \\____/\\/   \\/\\___/\\____/  \\_/  (_)')
    print('')
    print('------------------------------------------')
    print('')
    print('UUID:')
    print('    '+userData.uuid)
    print('Name:')
    print('    '+userData.name)
    print('Phone number:')
    print('    '+userData.phone_number)
    print('Occupation:')
    print('    '+userData.occupation)
    print('Date of Birth:')
    print('    '+userData.date_of_birth)
    print('Address:')
    print('    '+userData.address.split('\n')[0])
    print('    '+userData.address.split('\n')[1])
    print('    '+userData.address.split('\n')[2])
    print('Bank Details:')
    print('    '+userData.bank_card[0])
    print('    '+userData.bank_card[2])
    print('    '+userData.bank_card[3])
    print('Last Known Location:')
    print('    ' +
          userData.last_location[0]+', '+userData.last_location[1])
    print('    ' +
          userData.last_location[2]+', '+userData.last_location[3])
    print('    '+userData.last_location[4])
    print('')
    print('------------------------------------------')
    print('')
    print('This data was generated.')
    print('Will Westwood | 2023')
    print('')


def printProfile(userData):

    image = getFigure(userData)

    p = Serial(devfile='COM3',
               baudrate=38400,
               bytesize=8,
               parity='N',
               stopbits=1,
               timeout=1.00,
               dsrdtr=True)

    p.text('------------------------------------------\n')
    p.text('\n')
    p.image('./print_docs/logo.png')
    p.text('\n')
    p.text('------------------------------------------\n')
    p.text('\n')
    p.image(image)
    p.text('\n')
    p.text('------------------------------------------\n')
    p.text('\n')
    p.set(bold=True)
    p.text('UUID:\n')
    p.set(bold=False)
    p.text('    '+userData.uuid+'\n')
    p.set(bold=True)
    p.text('Name:\n')
    p.set(bold=False)
    p.text('    '+userData.name+'\n')
    p.set(bold=True)
    p.text('Phone number:\n')
    p.set(bold=False)
    p.text('    '+userData.phone_number+'\n')
    p.set(bold=True)
    p.text('Occupation:\n')
    p.set(bold=False)
    p.text('    '+userData.occupation+'\n')
    p.set(bold=True)
    p.text('Date of Birth:\n')
    p.set(bold=False)
    p.text('    '+userData.date_of_birth+'\n')
    p.set(bold=True)
    p.text('Address:\n')
    p.set(bold=False)
    p.text('    '+userData.address.split('\n')[0]+'\n')
    p.text('    '+userData.address.split('\n')[1]+'\n')
    p.text('    '+userData.address.split('\n')[2]+'\n')
    p.set(bold=True)
    p.text('Bank Details:\n')
    p.set(bold=False)
    p.text('    '+userData.bank_card[0]+'\n')
    p.text('    '+userData.bank_card[2]+'\n')
    p.text('    '+userData.bank_card[3]+'\n')
    p.set(bold=True)
    p.text('Last Known Location:\n')
    p.set(bold=False)
    p.text('    ' +
           userData.last_location[0]+', '+userData.last_location[1]+'\n')
    p.text('    ' +
           userData.last_location[2]+', '+userData.last_location[3]+'\n')
    p.text('    '+userData.last_location[4]+'\n')
    p.text('\n')
    p.text('------------------------------------------\n')
    p.text('This data was generated.\n')
    p.text('------------------------------------------\n')
    p.set(bold=True)
    p.text('Will Westwood')
    p.set(bold=False)
    p.text(' | ')
    p.set(bold=True)
    p.text('2023\n')
    p.qr('https://willwestwood.me/', size=3)
    p.text('------------------------------------------\n')

    p.cut()


def getDataAndPrint(uuid):
    profileData = personalData.getPersonData(uuid)
    printProfile(profileData)

# Test UUID: b82d32de-69c2-4a97-8899-08e1cfee82d9
# userData = personalData.getPersonData('b82d32de-69c2-4a97-8899-08e1cfee82d9')
# printProfile(userData=userData)


if len(sys.argv) > 1:
    uuidToPrint = sys.argv[1]
    getDataAndPrint(uuidToPrint)
