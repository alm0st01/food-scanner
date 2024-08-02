import cv2
from pyzbar.pyzbar import decode
import time
from tools import extratools


def photo_detect(file_path):
    img = cv2.imread(file_path)

    for code in decode(img):
        print(code.type)
        print(code.data.decode('utf-8'))

camera = False
def live_detect(num):
    global camera
    camera = False

    if num == 1:  # Prevents camera being turned on at the start of app.py
        camera = True
        vid = cv2.VideoCapture(0)
        vid.set(3, 640)
        vid.set(4, 480)


    while camera == True:
        success, frame = vid.read()

        for code in decode(frame):
            if code.type != "QRCODE":
                camera = False
                time.sleep(1)
                cv2.destroyAllWindows()
                cv2.waitKey(1)

                return code.data.decode('utf-8')
        if camera == False:
            camera = False
            time.sleep(1)
            cv2.destroyAllWindows()
            cv2.waitKey(1)

        if camera:
            cv2.imshow('Barcode Scanner', frame)
            cv2.waitKey(1)

    time.sleep(1)
