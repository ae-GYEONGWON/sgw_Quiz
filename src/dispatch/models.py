import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.dispatch.db.session import Base

# ✅ 퀴즈(시험지) 테이블
class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)  # 퀴즈 제목
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 관계 설정
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")


# ✅ 문제(Question) 테이블
class Question(Base):
    __tablename__ = "question"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)  # 문제 내용
    order = Column(Integer, nullable=False)  # 문제 순서

    # 관계 설정
    quiz = relationship("Quiz", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")


# ✅ 선택지(Choice) 테이블
class Choice(Base):
    __tablename__ = "choice"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)  # 선택지 내용
    is_correct = Column(Boolean, nullable=False, default=False)  # 정답 여부

    # 관계 설정
    question = relationship("Question", back_populates="choices")


# ✅ 사용자 응시(UserAttempt) 테이블
class UserAttempt(Base):
    __tablename__ = "user_attempt"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # 사용자의 ID
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=True)  # 최종 점수
    completed_at = Column(TIMESTAMP, nullable=True)  # 응시 완료 시간

    # 관계 설정
    quiz = relationship("Quiz")
    answers = relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")


# ✅ 사용자 답안(UserAnswer) 테이블
class UserAnswer(Base):
    __tablename__ = "user_answer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("user_attempt.id", ondelete="CASCADE"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id", ondelete="CASCADE"))
    choice_id = Column(UUID(as_uuid=True), ForeignKey("choice.id", ondelete="CASCADE"))  # 사용자가 선택한 답안

    # 관계 설정
    attempt = relationship("UserAttempt", back_populates="answers")
    question = relationship("Question")
    choice = relationship("Choice")
