from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class CompanyExam(Base):
    __tablename__ = "company_exams"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_slug = Column(String(100), nullable=False)
    company_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    questions = relationship(
        "CompanyExamQuestion", back_populates="exam", cascade="all, delete-orphan"
    )
    attempts = relationship(
        "CompanyExamAttempt", back_populates="exam", cascade="all, delete-orphan"
    )


class CompanyExamQuestion(Base):
    __tablename__ = "company_exam_questions"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("company_exams.id"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    reference_answer = Column(Text, nullable=True)
    position = Column(Integer, nullable=False)

    exam = relationship("CompanyExam", back_populates="questions")
    answers = relationship(
        "CompanyExamAnswer", back_populates="question", cascade="all, delete-orphan"
    )


class CompanyExamAttempt(Base):
    __tablename__ = "company_exam_attempts"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("company_exams.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    exam = relationship("CompanyExam", back_populates="attempts")
    answers = relationship(
        "CompanyExamAnswer", back_populates="attempt", cascade="all, delete-orphan"
    )


class CompanyExamAnswer(Base):
    __tablename__ = "company_exam_answers"

    id = Column(Integer, primary_key=True)
    attempt_id = Column(
        Integer, ForeignKey("company_exam_attempts.id"), nullable=False, index=True
    )
    question_id = Column(
        Integer, ForeignKey("company_exam_questions.id"), nullable=False, index=True
    )
    user_answer = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    status = Column(String(30), nullable=False)
    feedback = Column(Text, nullable=False)
    suggested_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    attempt = relationship("CompanyExamAttempt", back_populates="answers")
    question = relationship("CompanyExamQuestion", back_populates="answers")
