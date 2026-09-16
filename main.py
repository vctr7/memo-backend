from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models
import os
origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]
origins.append("https://memo-frontend-zeta.vercel.app")


Base.metadata.create_all(bind=engine)   # 앱 시작 시 테이블이 없으면 생성

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# 요청마다 DB 세션을 열고, 끝나면 반드시 닫는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MemoIn(BaseModel):
    content: str
class MemoOut(BaseModel):
    id: int
    content: str
    model_config = {"from_attributes": True}  # ORM 객체 → Pydantic 변환 허용(v2 문법)


@app.get("/memos", response_model=list[MemoOut])
def list_memos(db: Session = Depends(get_db)):
    return db.query(models.Memo).all()

@app.post("/memos", response_model=MemoOut)
def create_memo(memo: MemoIn, db: Session = Depends(get_db)):
    new = models.Memo(content=memo.content)
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Memo, memo_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Memo not found")
    db.delete(obj); db.commit()
    return {"ok": True}