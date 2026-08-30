from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    Float,
    JSON
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Roadmap(Base):

    __tablename__ = "roadmaps"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(
        String(200)
    )

    subject = Column(
        String(100)
    )

    timeline = Column(
        Integer
    )

    status = Column(
        String(50),
        default="draft"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    # Relationship with topics
    topics = relationship(
        "RoadmapTopic",
        back_populates="roadmap",
        cascade="all, delete-orphan"
    )


    # Relationship with assessments
    assessments = relationship(
        "Assessment",
        back_populates="roadmap",
        cascade="all, delete-orphan"
    )



class RoadmapTopic(Base):

    __tablename__ = "roadmap_topics"


    id = Column(
        Integer,
        primary_key=True
    )


    roadmap_id = Column(
        Integer,
        ForeignKey("roadmaps.id")
    )


    topic_name = Column(
        String(200)
    )

    # Set for mixed job-description roadmaps so assessment RAG always uses the
    # exact originating curriculum, even when two curricula share a card title.
    curriculum_subject = Column(String(100), nullable=True)


    order = Column(
        Integer
    )


    duration_weeks = Column(
        Integer
    )

    start_day = Column(Integer, nullable=False)

    end_day = Column(Integer, nullable=False)


    description = Column(
        Text
    )


    completed = Column(
        Boolean,
        default=False
    )


    completion_score = Column(
        Float,
        nullable=True
    )


    # Relationship back to roadmap
    roadmap = relationship(
        "Roadmap",
        back_populates="topics"
    )


    # Topic resources
    resources = relationship(
        "TopicResource",
        back_populates="topic",
        cascade="all, delete-orphan"
    )



    # Topic assessments
    assessments = relationship(
        "Assessment",
        back_populates="topic",
        cascade="all, delete-orphan"
    )



class TopicResource(Base):

    __tablename__ = "topic_resources"


    id = Column(
        Integer,
        primary_key=True
    )


    topic_id = Column(
        Integer,
        ForeignKey("roadmap_topics.id")
    )


    resource_type = Column(
        String(20)
    )


    title = Column(
        String(300)
    )


    url = Column(
        Text
    )


    description = Column(
        Text,
        nullable=True
    )


    topic = relationship(
        "RoadmapTopic",
        back_populates="resources"
    )



class Assessment(Base):

    __tablename__ = "assessments"


    id = Column(
        Integer,
        primary_key=True
    )


    roadmap_id = Column(
        Integer,
        ForeignKey("roadmaps.id")
    )


    topic_id = Column(
        Integer,
        ForeignKey("roadmap_topics.id")
    )


    num_mcq = Column(
        Integer
    )


    num_short = Column(
        Integer
    )


    duration_minutes = Column(
        Integer
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    roadmap = relationship(
        "Roadmap",
        back_populates="assessments"
    )


    topic = relationship(
        "RoadmapTopic",
        back_populates="assessments"
    )


    questions = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )

    attempts = relationship(
        "UserAssessmentAttempt",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )



class AssessmentQuestion(Base):

    __tablename__ = "assessment_questions"


    id = Column(
        Integer,
        primary_key=True
    )


    assessment_id = Column(
        Integer,
        ForeignKey("assessments.id")
    )


    question_text = Column(
        Text
    )


    question_type = Column(
        String(20)
    )


    options = Column(
        JSON,
        nullable=True
    )


    correct_answer = Column(
        Text
    )


    assessment = relationship(
        "Assessment",
        back_populates="questions"
    )


    answers = relationship(
        "UserAnswer",
        back_populates="question",
        cascade="all, delete-orphan"
    )



class UserAssessmentAttempt(Base):

    __tablename__ = "user_assessment_attempts"


    id = Column(
        Integer,
        primary_key=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    assessment_id = Column(
        Integer,
        ForeignKey("assessments.id")
    )


    score = Column(
        Float
    )


    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    submitted_at = Column(
        DateTime,
        nullable=True
    )


    answers = relationship(
        "UserAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )

    assessment = relationship(
        "Assessment",
        back_populates="attempts"
    )



class UserAnswer(Base):

    __tablename__ = "user_answers"


    id = Column(
        Integer,
        primary_key=True
    )


    attempt_id = Column(
        Integer,
        ForeignKey("user_assessment_attempts.id")
    )


    question_id = Column(
        Integer,
        ForeignKey("assessment_questions.id")
    )


    user_answer = Column(
        Text
    )


    is_correct = Column(
        Boolean,
        nullable=True
    )


    explanation = Column(
        Text
    )


    marks_obtained = Column(
        Float
    )


    attempt = relationship(
        "UserAssessmentAttempt",
        back_populates="answers"
    )


    question = relationship(
        "AssessmentQuestion",
        back_populates="answers"
    )
