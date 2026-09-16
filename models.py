from sqlalchemy import Column, Integer, String
from database import Base

class Memo(Base):
    __tablename__ = "memos"          # 실제 테이블 이름
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)


class VisitorCount(Base):
    __tablename__ = "visitor_counts"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False, default=0)