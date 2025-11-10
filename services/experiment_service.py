from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db import session_scope
from app.models import Experiment
from app.schemas import ExperimentCreate

class ExperimentService:
    """Service layer for experiment management."""

    def create_experiment(self, payload: ExperimentCreate):
        try:
            with session_scope() as db:
                existing = db.query(Experiment).filter_by(name=payload.name).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Experiment '{payload.name}' already exists",
                    )

                experiment = Experiment(name=payload.name)
                db.add(experiment)
                db.commit()
                db.refresh(experiment)
                return {"id": experiment.id, "name": experiment.name}

        except IntegrityError:
            raise HTTPException(status_code=409, detail="Database constraint violation")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal database error")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
