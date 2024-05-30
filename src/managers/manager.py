from __future__ import annotations

from src.models.entities import Room, Tenant, Lease, Payment
from src.services.service import Session

from typing import Iterable, Optional

from sqlalchemy import asc, desc

class BoardingHouseManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_room(self, room: Room) -> Room:
        self.session.add(room)
        self.session.commit()
        return room

    def add_tenant(self, tenant: Tenant) -> Tenant:        
        self.session.add(tenant)
        self.session.commit()
        return tenant
        
    def add_lease(self, lease: Lease) -> Lease:
        self.session.add(lease)
        self.session.commit()
        return lease
        
    def add_payment(self, payment: Payment) -> Payment:
        self.session.add(payment)
        self.session.commit()
        return payment
        
    def update_room(self, room: Room) -> None:
        self.session.commit()
    
    def update_tenant(self, tenant: Tenant) -> None:
        self.session.commit()
    
    def update_lease(self, lease: Lease) -> None:
        self.session.commit()
    
    def update_payment(self, payment: Payment) -> None:
        self.session.commit()
    
    def delete_room(self, room: Room) -> None:
        if room.lease:
            self.session.delete(room.lease)
        for payment in room.payments:
            self.session.delete(payment)
        for tenant in room.tenants:
            self.session.delete(tenant)
        self.session.delete(room)
        self.session.commit()
    
    def delete_tenant(self, tenant: Tenant) -> None:
        if tenant.lease:
            self.session.delete(tenant.lease)
        for payment in tenant.payments:
            self.session.delete(payment)
        self.session.delete(tenant)
        self.session.commit()
        
    def delete_lease(self, lease: Lease) -> None:
        self.session.delete(lease)
        self.session.commit()
        
    def delete_payment(self, payment: Payment) -> None:
        self.session.delete(payment)
        self.session.commit()

    def get_room(self, room_number: int) -> Optional[Room]:
        return self.session.get(Room, room_number)
    
    def get_tenant(self, tenant_id: int) -> Optional[Tenant]:
        return self.session.get(Tenant, tenant_id)
    
    def get_lease(self, lease_id: int) -> Optional[Lease]:
        return self.session.get(Lease, lease_id)
    
    def get_payment(self, paymnet_id: int) -> Optional[Payment]:
        return self.session.get(Payment, paymnet_id)

    def get_all_rooms(self) -> Iterable[Room]:
        return self.session.query(Room).order_by(asc(Room.room_number)).all()

    def get_all_tenants(self) -> Iterable[Tenant]:
        return self.session.query(Tenant).order_by(asc(Tenant.tenant_id)).all()
    
    def get_all_leases(self) -> Iterable[Lease]:
        return self.session.query(Lease).order_by(asc(Lease.lease_id)).all()
    
    def get_all_payments(self) -> Iterable[Payment]:
        return self.session.query(Payment).order_by(desc(Payment.payment_date)).all()

    def close_session(self) -> None:
        self.session.close()
