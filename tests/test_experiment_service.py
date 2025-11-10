import pytest
from fastapi import HTTPException
from app.services.experiment_service import ExperimentService
from app.schemas import ExperimentCreate

def test_duplicate_experiment(mocker):
    service = ExperimentService()
    mock_session = mocker.patch("app.services.experiment_service.session_scope")
    mock_db = mock_session.return_value.__enter__.return_value
    mock_db.query.return_value.filter_by.return_value.first.return_value = True

    with pytest.raises(HTTPException) as exc:
        service.create_experiment(ExperimentCreate(name="TestExp"))

    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail
