# pip install

# fastapi  : 비동기 웹 프레임 워크, 자동 OpenAPI 문서 생성
# uvicorn : 고성능 비동기 서버, ASGI 표준지원
# pydantic : 데이터 검증, 직렬화, 타입힌팅, 설정관리
# pillow : 이미지 열기, 저장, 변환, 다양한 이미지 처리용
# numpy : 수치계산, 배열 및 행렬연산, 다양한 수학함수
# requests : 간단한 http 요청 및 응답처리
# ultralytics : YOLO8 객체탐지 모델제공
# opencv-python : 이미지 및 비디오 처리, 컴퓨터 비젼기능(roboflow 대채)
# python-multipart : 멀티파트 폼데이터를 파싱하기 위함

# uvicorn main : app --reload  로 실행

##############################################

# post 요청을 통해 이미지가 전송되면 인공지능 객체 탐지 모델을 이용해서 객체를 탐지하고
# 그 결과 이미지를 bace64 인코딩 문자열로 반환하는 서비스

from fastapi import FastAPI, UploadFile, File ,Form
# 라우팅, 파일업로드, 폼데이터 처리

from pydantic import BaseModel
# pydantic 의 데이터 모델을 정의

import io       # 파일의 입출력을 위한 모듈
import base64   # 데이터를 Base64로 인코딩 디코딩 https://ko.wikipedia.org/wiki/%EB%B2%A0%EC%9D%B4%EC%8A%A464
from PIL import Image   # pillow 이미지 처리 라이브러리
import numpy as np      # 배열및 행열 연산을 위한 라이브러리
from ultralytics import YOLO    # yolo8 모델 사용 울트라리틱스
import cv2                      # 컴뷰터 비전 작업을 위한 라이브러리



URL = f"https://detect.roboflow.com/detect_float_waste_123/2?api_key=NRW0ztrXrPYGaSXU6FAl"

app = FastAPI()
model = YOLO('yolov8n.pt')
# YOLOv8 모델 로드(yolov8n.pt 모댈의 가중치 파일)

class DetectionResult(BaseModel):   # pandatic 을 사용하여 데이터 모델을 정의(응답데이터를 구조화)
    message : str                   # 클라이언트가 보낸 메세지
    image : str                     # Base64로 인코딩된 탐지결과 이미지

#객체 탐지 함수
# 객체 탐지를 위한 함수를 정의로 모델에 이미지를 넣어 객체를 탐지하고
# 그 결과에서 바운딩박스 정보를 추출한 후 이미지에 바인딩박스와 클래스 이름, 신롸도를 표시한 후 반환

def detect_objects(image: Image):
    img = np.array(image)                           # 이미지를 numpy 배열로 변환
    results = model(img)                            # 객체 탐지
    class_names = model.names                       # 클래스이름 저장

    # 결과를 바운딩 박스, 클래스이름, 정확도로 이미지에 표시
    for result in results:
        boxes = result.boxes.xyxy                   # 바운딩 박스
        confidences = result.boxes.conf             # 신뢰도
        class_ids = result.boxes.cls                # 클래스 이름

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)          # 좌표를 정수로 변환
            label = class_names[int(class_ids)]     # 클래스 이름
            cv2.rectangle(img, (x1,y1), (x2, y2), (255,0,0),2)
            cv2.putText(img, f'{label} {confidences:.2f}',(x1,y1),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200,15,60), 2)

    result_image = Image.fromarray(img)             # 결과 이미지를 PIL로 변환
    return result_image
# 결론 : YOLO 모델로 객체 탐지 수행
# -> 탐지된 객체에 대해 바운딩 박스를 그리고 정확도 점수를 이미지에 표시
# -> 결과 이미지를 PIL 이미지로 변환하여 반환

@app.get("/")
async def read_root():
    return {"message" : "Hello FastAPI"}

@app.post("/detect",response_model=DetectionResult)
async def detect_service(message : str = Form(...), file: UploadFile = File(...)):
    # 이미지를 읽어서 PIL이미지로 변환
    image = Image.open(io.BytesIO(await file.read()))
    # 알파채널이 있으면 알파채널 제거하고 RGB로 변환
    if image.mode =='RGBA':
        image = image.convert('RGB')
    elif image.mode !='RGB':
        image = image.convert('RGB')
    # 객체 탐지를 수행
    result_image = detect_objects(image)

    # 이미지결과를 base64로 인코딩
    bufferd = io.BytesIO()
    result_image.save(bufferd,format="JPEG")
    img_str = base64.b64encode(bufferd.getvalue()).decode("utf-8")

    return DetectionResult(message=message,image=img_str)
# 결론 :http://localhost:8001/detect 경로에 post 요청처리
# 클라이언트로 업로드된 이미지를 읽고 PIL이밎로 변환하고 , 알파체널이 있으면 알파체널 제거
# https://developer.mozilla.org/ko/docs/Glossary/Alpha
# 객체탐지 함수를 호출하여 탐지결과를 이미지로 얻는다
# 탐지결과 이미지를 BAse64 문자열로 인코딩
# DetectionResult 모델을 사용하여 메세지와 인코딩된 이미지 json응답으로 반환


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8001)