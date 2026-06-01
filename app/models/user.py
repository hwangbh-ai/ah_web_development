from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.patient import Patient

from app.core.db.databases import Base
from app.core.db.models import UUIDMixin, TimestampMixin, SoftDeleteMixin


class User(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """
    시스템 관리자(의료진) 모델
    - 백오피스에 로그인하여 환자 및 판독 결과를 관리하는 사용자
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(20), nullable=False, comment="이름")
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True, comment="이메일 (로그인 ID)"
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="해시된 비밀번호")

    # Relationships
    patients: Mapped[list["Patient"]] = relationship(
        "Patient", back_populates="created_by", lazy="select"
    )
