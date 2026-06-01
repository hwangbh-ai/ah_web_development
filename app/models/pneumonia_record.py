from __future__ import annotations

import enum
import uuid as uuid_pkg
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import CHAR

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.patient import Patient

from app.core.db.databases import Base
from app.core.db.models import UUIDMixin, TimestampMixin


class DiagnosisResultEnum(str, enum.Enum):
    NORMAL = "normal"          # 정상
    PNEUMONIA = "pneumonia"    # 폐렴
    UNCERTAIN = "uncertain"    # 불확실


class PneumoniaRecord(UUIDMixin, TimestampMixin, Base):
    """
    폐렴 판독 기록 모델
    - 흉부 X-Ray 이미지에 대한 AI 모델 판독 결과를 저장
    - 의료진의 최종 확인 소견도 함께 기록
    """
    __tablename__ = "pneumonia_records"

    # FK: 환자
    patient_uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        CHAR(36),
        ForeignKey("patients.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="환자 UUID",
    )

    # X-Ray 이미지 경로 (media/ 디렉터리 기준 상대경로)
    xray_image_path: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="X-Ray 이미지 파일 경로"
    )

    # AI 모델 판독 결과
    ai_result: Mapped[DiagnosisResultEnum] = mapped_column(
        SAEnum(DiagnosisResultEnum), nullable=False, comment="AI 판독 결과"
    )
    ai_confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="AI 판독 신뢰도 (0.0 ~ 1.0)"
    )
    ai_memo: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI 판독 부가 정보"
    )

    # 의료진 최종 확인 소견
    doctor_result: Mapped[DiagnosisResultEnum | None] = mapped_column(
        SAEnum(DiagnosisResultEnum), nullable=True, comment="의료진 최종 판독 결과"
    )
    doctor_memo: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="의료진 소견 메모"
    )

    # FK: 판독 확인 의료진 (User)
    reviewed_by_uuid: Mapped[uuid_pkg.UUID | None] = mapped_column(
        CHAR(36),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        comment="판독 확인 의료진 UUID",
    )

    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient", back_populates="pneumonia_records", lazy="select"
    )
    reviewed_by: Mapped["User | None"] = relationship(
        "User", lazy="select", foreign_keys=[reviewed_by_uuid]
    )
