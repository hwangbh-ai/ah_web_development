# Alembic autogenerate를 위해 모든 ORM 모델을 여기서 import합니다.
# Base.metadata에 모델이 등록되어야 마이그레이션 파일이 올바르게 생성됩니다.
from app.models.user import User  # noqa: F401
from app.models.patient import Patient  # noqa: F401
from app.models.pneumonia_record import PneumoniaRecord  # noqa: F401
