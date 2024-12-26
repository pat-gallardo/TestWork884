from celery import Celery
from .config import settings
import heapq
from .models import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize Celery
celery = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# Initialize the database engine and sessionmaker
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@celery.task
def update_statistics():
    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        if not transactions:
            return {
                "total_transactions": 0,
                "average_transaction_amount": 0.0,
                "top_transactions": [],
            }

        heap = []
        total_amount = 0
        count = 0

        for trans in transactions:
            count += 1
            total_amount += trans.amount

            if len(heap) < 3:
                heapq.heappush(heap, (trans.amount, trans.transaction_id))
            else:
                heapq.heappushpop(heap, (trans.amount, trans.transaction_id))

        top_transactions = sorted(
            [{"transaction_id": tid, "amount": amt} for amt, tid in heap],
            key=lambda x: x["amount"],
            reverse=True,
        )

        return{
            "total_transactions": count,
            "average_transaction_amount": total_amount / count if count > 0 else 0.0,
            "top_transactions": top_transactions,
        }
    finally:
        db.close()