from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vibe Check Polling API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/polls")
def create_poll(poll: schemas.PollCreate, db: Session = Depends(get_db)):
    new_poll = models.Poll(question=poll.question)
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)

    for option in poll.options:
        db.add(models.Option(text=option, poll_id=new_poll.id))

    db.commit()
    return {"poll_id": new_poll.id}

@app.get("/polls/{poll_id}")
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    results = {}
    for option in poll.options:
        vote_count = db.query(models.Vote).filter(
            models.Vote.option_id == option.id
        ).count()
        results[option.text] = vote_count

    return {
        "id": poll.id,
        "question": poll.question,
        "results": results
    }

@app.post("/polls/{poll_id}/vote")
def vote(poll_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    already_voted = db.query(models.Vote).filter(
        models.Vote.user_id == vote.user_id,
        models.Vote.poll_id == poll_id
    ).first()

    if already_voted:
        raise HTTPException(
            status_code=400,
            detail="User already voted on this poll"
        )

    new_vote = models.Vote(
        user_id=vote.user_id,
        poll_id=poll_id,
        option_id=vote.option_id
    )

    db.add(new_vote)
    db.commit()

    return {"message": "Vote recorded successfully"}
