import requests # Python용 HTTP 라이브러리
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
        ret, frame = webcam.read() # ret : camera 이상 여부, frame : 현재 시점의 frame 값 정보
        time_passed = time.time() - start_time

        cv2.imshow("WebCam", frame)

        if not ret or frame is None:
            print("Error : Frame is not captured correctly")
            break

        if cv2.waitKey(1) != -1 or time_passed > 5:
            photo_dir = os.path.join('./photos', time.strftime('%Y-%m-%d %H-%M-%S'))
            cv2.imwrite(photo_dir + '.jpg', frame)
            break

webcam.release()
cv2.destroyAllWindows()
         
# photo_dir에 있는 파일을 열고 파일 객체를 반환
imgfile = open(photo_dir + '.jpg', 'rb') # 이미지 데이터를 전송하기 위해 byte 형식으로 변환

# Requests makes it simple to upload Multipart-encoded files 
files = {'imagefile': imgfile}

# 플라스크 서버가 열릴 IP 주소를 URL에 넣기
url = 'http://localhost:3000/upload/R001'
response = requests.post(url, files=files) # 클라이언트에서 서버로 추가적인 데이터를 body에 포함해야 하므로 post 방식을 사용
imgfile.close()

print(response.text)