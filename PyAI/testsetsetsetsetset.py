# pip install requests opencv-python
import requests
import cv2
import os

# Roboflow API 정보
URL = f"https://detect.roboflow.com/detect_float_waste_123/2?api_key=NRW0ztrXrPYGaSXU6FAl"
#
# # 이미지 파일 경로
# image_path = ""
#
# # 이미지 파일 존재 확인
# if not os.path.exists(image_path):
#     print(f"File not found: {image_path}")
# else:
#     # 이미지 로드 및 전처리
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Failed to load image. Please check the file format and path.")
#     else:
#         # 이미지를 API에 맞는 형식으로 변환
#         _, encoded_image = cv2.imencode('.jpg', image)
#
#         # API 요청
#         response = requests.post(URL, files={"file": encoded_image.tobytes()})
#
#         if response.status_code == 200:
#             predictions = response.json()
#             detections = predictions.get('predictions', [])
#
#             # 바운딩 박스 그리기
#             for detection in detections:
#                 x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
#                 class_name = detection['class']
#                 confidence = detection['confidence']
#
#                 # 좌표 계산
#                 x1 = int(x - w / 2)  # 바운딩 박스의 왼쪽 위 x
#                 y1 = int(y - h / 2)  # 바운딩 박스의 왼쪽 위 y
#                 x2 = int(x + w / 2)  # 바운딩 박스의 오른쪽 아래 x
#                 y2 = int(y + h / 2)  # 바운딩 박스의 오른쪽 아래 y
#
#                 # 바운딩 박스 그리기
#                 color = (0, 255, 0)  # 초록색
#                 cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
#
#                 # 클래스 이름과 신뢰도 표시
#                 label = f"{class_name} ({confidence:.2f})"
#                 cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#             # 결과 이미지 보기
#             cv2.imshow("Predictions", image)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#
#             # 결과 이미지 저장 (옵션)
#             output_path = "output.jpg"
#             cv2.imwrite(output_path, image)
#             print(f"Output saved to {output_path}")
#         else:
#             print("Error:", response.status_code, response.text)


video_path = "test_yolo.mp4"  # 비디오 파일 경로 (웹캠은 0으로 설정)

# 비디오 캡처 초기화
cap = cv2.VideoCapture(video_path)

# 비디오 파일이 열리지 않을 경우 확인
if not cap.isOpened():
    print(f"Error: Unable to open video file: {video_path}")
    exit()

# 동영상 저장 옵션 설정 (옵션)
output_path = ".mp4"
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 형식 저장
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 프레임 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # 영상의 끝에 도달하면 루프 종료

    # 프레임 전처리 및 API 요청
    _, encoded_frame = cv2.imencode('.jpg', frame)
    response = requests.post(URL, files={"file": encoded_frame.tobytes()})

    if response.status_code == 200:
        predictions = response.json().get('predictions', [])

        # 바운딩 박스 그리기
        for detection in predictions:
            x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
            class_name = detection['class']
            confidence = detection['confidence']

            # 좌표 계산
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)

            # 바운딩 박스 및 텍스트 그리기
            color = (0, 255, 0)  # 초록색
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{class_name} ({confidence:.2f})"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    else:
        print(f"API Error: {response.status_code}, {response.text}")

    # 프레임을 화면에 표시
    cv2.imshow("Video", frame)

    # 프레임 저장 (옵션)
    out.write(frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Processed video saved to: {output_path}")


