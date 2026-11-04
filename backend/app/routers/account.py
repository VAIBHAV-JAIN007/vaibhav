from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import JournalEntry, Position, User
from ..schemas import JournalIn, PositionIn

router = APIRouter(tags=["portfolio-and-journal"])

@router.get("/portfolio")
def list_positions(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.scalars(select(Position).where(Position.user_id == user.id)).all()
    return [{"id":p.id,"symbol":p.symbol,"quantity":p.quantity,"average_price":p.average_price,"market":p.market} for p in rows]

@router.post("/portfolio", status_code=201)
def add_position(data: PositionIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    row = Position(user_id=user.id, **data.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"symbol":row.symbol}

@router.get("/journal")
def list_journal(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.scalars(select(JournalEntry).where(JournalEntry.user_id == user.id).order_by(JournalEntry.created_at.desc())).all()
    return [{"id":r.id,"symbol":r.symbol,"side":r.side,"entry_price":r.entry_price,"exit_price":r.exit_price,"quantity":r.quantity,"notes":r.notes,"created_at":r.created_at} for r in rows]

@router.post("/journal", status_code=201)
def add_journal(data: JournalIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    row = JournalEntry(user_id=user.id, **data.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"symbol":row.symbol}
