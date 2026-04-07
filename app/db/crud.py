from app.db.session import SessionLocal
from app.db.models import ArbitrDoc


def save_result(data: dict):
    with SessionLocal() as session:
        obj = ArbitrDoc(
            case_number=data.get("case_number"),
            last_date=data.get("last_date"),
            document_name=data.get("document_name")
        )
        session.add(obj)
        session.commit()
