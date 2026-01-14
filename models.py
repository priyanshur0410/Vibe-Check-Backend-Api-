from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)

    options = relationship(
        "Option",
        back_populates="poll",
        cascade="all, delete"
    )

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    poll_id = Column(Integer, ForeignKey("polls.id"))

    poll = relationship("Poll", back_populates="options")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    option_id = Column(Integer, ForeignKey("options.id"))

    __table_args__ = (
        UniqueConstraint("user_id", "poll_id", name="one_vote_per_user"),
    )
