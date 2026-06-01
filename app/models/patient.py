from __future__ import annotations

import enum
import uuid as uuid_pkg
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import CHAR

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.pneumonia_record import PneumoniaRecord

from app.core.db.databases import Base
from app.core.db.models import UUIDMixin, TimestampMixin, SoftDeleteMixin


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Patient(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """
    환자 정보 모델
    - 폐렴 판독 대상 환자의 기본 정보를 저장
    """
    __tablename__ = "patients"

    name: Mapped[str] = mapped_column(String(20), nullable=False, comment="환자 이름")
    patient_code: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True, comment="환자 등록 번호"
    )
    age: Mapped[int] = mapped_column(Integer, nullable=False, comment="나이")
    gender: Mapped[GenderEnum] = mapped_column(
        SAEnum(GenderEnum), nullable=False, comment="성별"
    )
    contact: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="연락처"
    )
    address: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="주소"
    )
    memo: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="환자 특이사항 메모"
    )

    # FK: 담당 관리자 (User)
    created_by_uuid: Mapped[uuid_pkg.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("users.uuid", ondelete="SET NULL"), nullable=True, comment="등록한 관리자 UUID"
    )

    # Relationships
    created_by: Mapped["User | None"] = relationship(
        "User", back_populates="patients", lazy="select"
    )
    pneumonia_records: Mapped[list["PneumoniaRecord"]] = relationship(
        "PneumoniaRecord", back_populates="patient", lazy="select"
    )
