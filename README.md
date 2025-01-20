# BootPyAI_25
스프링 부트와 파이썬 ai 협업모듈

개발환경 교구축

파이썬 인터프린터 : http://www.python.org/ -> 3.12버젼 설치(3.8이상 필수)

FastAPI설치  :pip install fastapi uvicorn uvicorn : ASGI(Asynchronus Server Gateway Interface) 는 파이썬에서 비동기 웹서버와 웹 에플리케이션 간의
인터페이스 표준 ASGI는 기존 WSGI(Web Server Gate Way Interface)의 비동기 비젼으로, 파이썬에서 비동기 처리를 지원하는 웹애플리케이션을 구출하기 위함 
https://veolg.io/@hwaya2828/WEGI-ASGI

ASGI특징

비동기 지원 : ASGI는 비동기코드 실행 지원하며 높은 성능과 동시성을 제공
웹 소켓이나 서버푸시와 같은 비동기 통신이 필요한 애플리캐이션에 유용
범용성 : HTTP뿐만 아니라, WebSocket, gPRC와 같은 프로토콜로 지원
유연성 : ASGI 애플리케이션은 다양한 서버 및 프래임워크와 호환되며, 모듈식으로 구성
FastAPI와 ASGI

FastAPI는 ASGI표준을 따르는 웹 프레임워크임
FastAPI 애플리케이션은 비동기 처리를 기본으로 하며, Uvicorn과같은 ASGI서버를 사용하여 높은 성능을 제공
FastAPI 서버 실행

mine.py 실행
Terminal에서 D:\phthonWorkSpace > uvicorn main:app --reload --port8001(위치확인) 

참고 도서
https://wikidocs.net/book/8531

![image](https://github.com/user-attachments/assets/70319d16-45da-4c02-a0d4-169fb4b9e2bd)
