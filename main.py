# from fastapi import FastAPI     # 파이썬 웹 개발 API  서버 열 때 : uvicorn main:app --reload --port 8001 시작 할 때
# from pydantic import BaseModel  # 유효성 검사용 판다틱   끌 때:  ctrl+ c
# from starlette.middleware.base import BaseHTTPMiddleware
# # 요청(request)과 응답(responce) 사이에 특정 작업을 수행
# # 미들웨어는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정작업을 수행 할 수 있음
# # 예를들어 로깅, 인증, cors처리, 압축등...
# import logging # 로그 출력용
#
#
# app = FastAPI(  # 생성자를 통해서 postman을 대체하는 문서와 툴이 내장되어 있다
#     title = "MBC AI Project Test",
#     desciption = "파이썬과 자바부트를 연동한 ai앱",
#     version="1.0.0",
#     doce_url=None,    # http://localhost:8001/docs 연습후에는 닫을 것 (해킹의 위험/ 보안상 None처리 한다)
#     redoc_url = None  # http://localhost:8001/redoc
# )                 # FastAPI() 객체 생성해서 app 변수에 넣음
#
#
# class LoggingMiddleware(BaseHTTPMiddleware):    # 로그를 콘솔에 출력하는 용도
#     logging.basicConfig(level=logging.INFO)     # 로그 출력 추가
#     async def dispatch(self,request,call_next):
#         logging.info(f"req{request.method}{request.url}")
#         response = await call_next(request)
#         logging.info(f"status Code : {response.status_code}")
#         return response
# app.add_middleware(LoggingMiddleware)   # 모든 요청에 대해 로그를 남기는 미들웨어 클래스를 사용함
#
#
# class Item(BaseModel):          # 아이템 객체 생성(BaseModel : 객체연결 - 상속개념)
#     name : str                  # 필드 1 :상품명
#     description : str = None    # 상품설명 : 문자열(기본값: Null)
#     price : float               # 가격 : 실수형
#     tax : float = None          # 세금 : 실수형(기본값: Null)
#
# # 컨트롤러 검증은 포스트 맨(postman)으로 활용해 보았는데 내장된 백검증 툴도 있음
#
# @app.get("/")    # http://ip주소 : 포트/(루트컨텍스트)
# async def read_root():
#     return {"HELLO":"WORLD"}
#
# @app.post("/items/")    # post매서드용 응답
# async def create_item(item : Item):     # BaseModel 은 데이터 모델링을 쉽게 도와주고 유효성 검사도 실행해준다
#     # 잘못된 데이터가 들어올 경우 422 오류코드를 반환한다
#     return item
#
# @app.get("/items/{item_id}")    # http://ip주소:포트/items/1
# async def read_item(item_id : int, q: str=None):
#     return {"item_id" : item_id, "q" : q}
#     # item_id : 상품의 번호 -> 경로 매개변수
#     # q : 쿼리 매개변수 (기본값 None)

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins =[
    "http://127.0.0.1:8001"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_mothods=["*"],
    allow_headers=["*"],
)

@app.get("/hi")
def hello():
    return{"message":"안녕?하세요"}