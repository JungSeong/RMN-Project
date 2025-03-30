from flask import Flask, render_template, request, jsonify # 필요한 모듈 가져오기
import uuid, cv2  # 이미지 처리를 위한 OpenCV 라이브러리 가져오기
import pymysql
from rmn import RMN  # 감정 감지를 위한 RMN 모델 가져오기

app = Flask(__name__)  # Flask 애플리케이션 인스턴스 생성
m = RMN()  # 감정 감지를 위해 RMN 모델 인스턴스화

@app.route('/upload/<agentid>', methods=['POST'])  # 루트 URL에 대한 POST 요청을 처리하기 위한 라우트 정의
def predict(agentid):
    imagefile = request.files['imagefile']  # 요청에서 업로드된 이미지 파일 가져오기
    # 파일명을 해시하여 중복되지 않도록 해야 함!
    image_path = "/uploadimg/" + str(uuid.uuid4().hex) + "_" + imagefile.filename  # 업로드된 이미지를 저장할 파일 경로 생성
    imagefile.save("./static"+image_path)  # 업로드된 이미지를 지정된 파일 경로에 저장

    image = cv2.imread("./static"+image_path)  # OpenCV를 사용하여 저장된 이미지 읽기
    assert image is not None  # 이미지가 성공적으로 읽혔는지 확인

    results = m.detect_emotion_for_single_frame(image)  # RMN 모델을 사용하여 이미지에서 감정 감지 수행

    # 결과 처리
    max_emotion = None  # 최고 확률 감정 초기화
    max_score = -1  # 최고 확률 초기화
    for result in results:  # 결과에서 감지된 감정 반복
        emotion = result['emo_label']  # 결과에서 감정 레이블 가져오기
        score = result['emo_proba'] * 100  # 감정 확률을 백분율로 변환
        if score > max_score:  # 현재 감정의 확률이 최고 확률보다 높은지 확인
            max_emotion = emotion  # 최고 확률 감정 업데이트
            max_score = score  # 최고 확률 업데이트

    # 결과 문자열 생성
    result_str = f"{max_emotion}: {max_score:.2f}%\n" if max_emotion else "감정이 감지되지 않았습니다"

    # DB 에 저장
    # 'prompt'라는 이름을 가진 DB에 user='root', host=localhost, password='{password}'를 가진 사람이 접속
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='{password}', db='prompt', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute("INSERT INTO tbl_emotion (agentid, emotion, score, imgfile, regdate) VALUES ('"+agentid+"', '"+max_emotion+"', "+str(max_score)+", '"+image_path+"', sysdate() )")
    conn.commit()
    conn.close()

    # return render_template('index.html', prediction=result_str)  # 예측 결과와 함께 HTML 템플릿 렌더링
    rtnData = {'emotion':max_emotion, 'score':max_score, 'file':image_path}
    return jsonify(rtnData)  # 예측 결과와 함께 HTML 템플릿 렌더링
    #return jsonify(results)  # 예측 결과와 함께 HTML 템플릿 렌더링

@app.route('/uploadList', methods=['GET'])
def image_view():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='{password}', db='prompt', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    SQL = "SELECT RANK() OVER(ORDER BY score DESC) ord, emotion, score, imgfile, regdate, agentid FROM tbl_emotion LIMIT 10"
    cur.execute(SQL)
    data = cur.fetchall()
    
    listData= []
    for obj in data:
        data_dic = {
            'ord' : obj[0],
            'emotion' : obj[1],
            'score' : obj[2],
            'imgfile' : obj[3],
            'regdate' : obj[4],
            'agentid' : obj[5]
        }
        listData.append(data_dic)
    
    cur.close()
    conn.close()

    return render_template('uploadList.html', datas=listData)

# http://localhost:3000/uploadList에서 디버깅 화면 확인 가능
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True) 