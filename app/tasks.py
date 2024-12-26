from celery import Celery
from .config import settings
import heapq
from .models import Transaction
from SQLAlchemy import create_engine
from SQLAlchemy.orm import sessionmaker

celery = Celery('tasks', broker=settings.REDIS_URL)

@celery.task
def update_statistics():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        if not transactions:
            return {
                "total_transactions": 0,
                "avarage_transaction_amount": 0.0,
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
            "avarage_transaction_amount": total_amount / count if count > 0 else 0,
            "top_transactions": top_transactions,
        }
    finally:
        db.close()