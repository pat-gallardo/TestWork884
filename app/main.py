from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, security
from .database import engine, get_db
from .tasks import update_statistics

app = FastAPI(title="Transaction Analysis Microservice")

models.Base.metadata.create_all(bind=engine)

@app.post("/transactions")
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.get_api_key),
):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=200, detail="Transaction already exists")
    
    task = update_statistics.delay()
    return {"message": "Transaction received", "task_id": task.id}
# Testing
@app.delete("/transactions")
async def delete_transactions(
    db: Session = Depends(get_db),
    api_key: str = Depends(security.get_api_key)
):
    db.query(models.Transaction).delete()
    db.commit()
    return {"message": "All transactions deleted"}

@app.get("/statistics", response_model=schemas.Statistics)
async def get_statistics(
    db: Session = Depends(get_db),
    api_key: str = Depends(security.get_api_key)
):
    stats = update_statistics()
    return stats