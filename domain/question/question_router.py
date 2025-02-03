from fastapi import APIRouter

from database import SessionLocal
from models import Question

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list")
def question_list():
    db = SessionLocal()
    _question_list = db.query(Question).order_by()