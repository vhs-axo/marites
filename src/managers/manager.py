from datetime import date
from typing import Iterable, Optional
from models.entities import Room, Tenant, Lease, Payment
from services.service import Session

class BoardingHouseManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_room(self, room: Room) -> None:
        self.session.add(room)
        self.session.commit()

    def add_tenant(self, tenant: Tenant) -> None:        
        self.session.add(tenant)
        self.session.commit()
        
    def add_lease(self, lease: Lease) -> None:
        self.session.add(lease)
        self.session.commit()
        
    def add_payment(self, payment: Payment) -> None:
        self.session.add(payment)
        self.session.commit()
        
    def update_room(self, room: Room) -> None:
        self.session.commit()
    
    def update_tenant(self, tenant: Tenant) -> None:
        self.session.commit()
    
    def update_lease(self, lease: Lease) -> None:
        self.session.commit()
    
    def update_payment(self, payment: Payment) -> None:
        self.session.commit()
    
    def delete_room(self, room: Room) -> None:
        self.session.delete(room)
        self.session.commit()
    
    def delete_tenant(self, tenant: Tenant) -> None:
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
        return self.session.query(Room).all()

    def get_all_tenants(self) -> Iterable[Tenant]:
        return self.session.query(Tenant).all()
    
    def get_all_leases(self) -> Iterable[Lease]:
        return self.session.query(Lease).all()
    
    def get_all_payments(self) -> Iterable[Payment]:
        return self.session.query(Payment).all()

    def close_session(self) -> None:
        self.session.close()
