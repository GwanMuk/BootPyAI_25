import requests
import roboflow

API_KEY = "your_roboflow_api_key"
UPLOAD_URL = "https://app.roboflow.com/mbc-0qsuq/detect_float_waste_1234/upload"

with open("best.pt", "rb") as file:
    response = requests.post(
        UPLOAD_URL,
        files={"file": file},
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

print(response.json())