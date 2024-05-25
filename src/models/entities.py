from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.sql.schema import Index, ForeignKey, CheckConstraint, UniqueConstraint, ddl
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, DECIMAL, BOOLEAN
from sqlalchemy.orm import relationship, mapped_column, Mapped, Session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, inspect

from models.base import Base

class Room(Base):
    __tablename__ = "rooms"
    
    room_number: Mapped[int] = mapped_column("roomNumber", INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    max_capacity: Mapped[int] = mapped_column("maxCapacity", INTEGER(unsigned=True), nullable=False)
    tenant_count: Mapped[int] = mapped_column("tenantCount", INTEGER(unsigned=True), nullable=False, default=0)
    
    __table_args__ = (
        CheckConstraint('tenantCount <= maxCapacity', name='chk_tenantCount'),
    )
    
    tenants: Mapped[list[Tenant]] = relationship("Tenant", back_populates="room")
    lease: Mapped[Lease] = relationship("Lease", back_populates="room")

    def __str__(self) -> str:
        return f"Room: {self.room_number} | Occupancy {self.tenant_count} / {self.max_capacity}"
    
    def __repr__(self) -> str:
        return f"Room(room_number={self.room_number}, tenant_count={self.tenant_count}, max_capacity={self.max_capacity})"
        


class Tenant(Base):
    __tablename__ = 'tenants'
    
    tenant_id: Mapped[int] = mapped_column("tenantId", INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column("lastName", VARCHAR(255), nullable=False)
    first_name: Mapped[str] = mapped_column("firstName", VARCHAR(255), nullable=False)
    middle_name: Mapped[str] = mapped_column("middleName", VARCHAR(127), nullable=False, default="")
    birth_date: Mapped[date] = mapped_column("birthDate", DATE, nullable=False)
    contact_number: Mapped[str] = mapped_column("contactNumber", VARCHAR(11), nullable=False)
    room_number: Mapped[int] = mapped_column("roomNumber", INTEGER(unsigned=True), ForeignKey('rooms.roomNumber', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
    @hybrid_property
    def formatted_name(self) -> str:
        return f"{self.last_name}, {self.first_name} {self.middle_name}".strip()
    
    __table_args__ = (
        CheckConstraint("REGEXP_LIKE(contactNumber, '^09[0-9]{9}$')", name='chk_contactNumber'),
        Index('ix_roomNumber', 'roomNumber'),
        Index('ix_lastName_firstName', 'lastName', 'firstName'),
    )
    
    room: Mapped[Room] = relationship("Room", back_populates="tenants")
    lease: Mapped[Lease] = relationship("Lease", back_populates="leaser")

    def __str__(self) -> str:
        return f"Tenant: {self.tenant_id} in Room {self.room_number} | {self.formatted_name} | {self.birth_date} | {self.contact_number}"
    
    def __repr__(self) -> str:
        return f"Tenant(tenant_id={self.room_number}, last_name={self.last_name!r}, first_name={self.first_name!r}, middle_name={self.middle_name!r}, birth_date={self.birth_date!r}, contact_number={self.contact_number!r}, room_number={self.room_number})"
        


class Lease(Base):
    __tablename__ = 'leases'
    
    lease_id: Mapped[int] = mapped_column("leaseId", INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    leaser_id: Mapped[int] = mapped_column("leaserId", INTEGER(unsigned=True), ForeignKey('tenants.tenantId', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    room_number: Mapped[int] = mapped_column("roomNumber", INTEGER(unsigned=True), ForeignKey('rooms.roomNumber', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    lease_start: Mapped[date] = mapped_column("leaseStart", DATE, nullable=False)
    lease_end: Mapped[date] = mapped_column("leaseEnd", DATE, nullable=False)
    deposit_amount: Mapped[Decimal] = mapped_column("depositAmount", DECIMAL(10, 2), nullable=False)
    monthly_rentAmount: Mapped[Decimal] = mapped_column("monthlyRentAmount", DECIMAL(10, 2), nullable=False)
    
    __table_args__ = (
        CheckConstraint('leaseStart < leaseEnd', name='leases_chk_leaseEnd'),
        UniqueConstraint('leaserId', name='uq_leaserId'),
        UniqueConstraint('roomNumber', name='uq_roomNumber'),
        Index('ix_leaserId', 'leaserId'),
        Index('ix_roomNumber', 'roomNumber'),
    )
    
    leaser: Mapped[Tenant] = relationship("Tenant", back_populates="lease")
    room: Mapped[Room] = relationship("Room", back_populates="lease")
    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="lease")



class Payment(Base):
    __tablename__ = 'payments'
    
    payment_id: Mapped[int] = mapped_column("paymentId", INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    lease_id: Mapped[int] = mapped_column("leaseId", INTEGER(unsigned=True), ForeignKey('leases.leaseId', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    payment_amount: Mapped[Decimal] = mapped_column("paymentAmount", DECIMAL(10, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column("paymentDate", DATE, nullable=False)
    paid: Mapped[bool] = mapped_column("paid", BOOLEAN, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('leaseId', 'paymentDate', name='uq_paymentDate_leaseId'),
        Index('ix_leaseId', 'leaseId'),
    )
    
    lease: Mapped[Lease] = relationship("Lease", back_populates="payments")

@event.listens_for(Tenant, "after_insert")
def uppercase_names(mapper, connection, target):
    target.last_name = target.last_name.upper()
    target.first_name = target.first_name.upper()
    target.middle_name = target.middle_name.upper()