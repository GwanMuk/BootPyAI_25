import requests

from main import DetectionResult

url = "http://127.0.0.1:8001/detect"    # 요청을 보낼 URL
message = "Test message"                # 서버로 전송할 메세지(폼 데이터로 전송)
file_path = "test.jpg"                  # 전송할 이미지 파일 경로(py와 같은 결로에 있어야 편함)

with open(file_path,"rb") as file:
    response = requests.post(url, data={"message":message},
                            files={"file":file})
# @app.get("/detect", response_model = DetectionResult)   # http

print(response.json())