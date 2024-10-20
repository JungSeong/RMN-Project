import requests
import cv2
import numpy as np
import time
import threading
import os

def Countdown():
    for i in range(5) :
        print(f"{5-i}초 후에 자동으로 사진이 촬영됩니다!!")
        time.sleep(1)

countdown = threading.Thread(target=Countdown)

webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not webcam.isOpened():
    print("웹캠이 인식되지 않았습니다.")
    exit()
else :
    start_time = time.time()
    countdown.start()

    while True:
        ret, frame = webcam.read()
        time_passed = time.time() - start_time

        cv2.imshow("VideoFrame", frame)

        if not ret or frame is None:
            print("Error : Frame is not captured correctly")
            break

        if cv2.waitKey(1) != -1 or time_passed > 5:
            photo_dir = os.path.join('./photos', time.strftime('%Y-%m-%d %H-%M-%S'))
            cv2.imwrite(photo_dir + '.jpg', frame)
            break

webcam.release()
cv2.destroyAllWindows()
         
#get picture data
imgfile = open(photo_dir + '.jpg', 'rb')

# Requests makes it simple to upload Multipart-encoded files 
files = {'imagefile': imgfile}

#플라스크 서버가 열릴 IP 주소를 URL에 넣기
url = 'http://localhost:3000/upload/R001'
response = requests.post(url, files=files)
imgfile.close()

print(response.text)