
from datetime import date
import re
from numpy import delete
from managers.manager import BoardingHouseManager
from models.entities import Room, Tenant, Lease, Payment
from services.service import SessionFactory
from views.rooms import RoomListWindow, RoomOpenWindow
from views.forms import RoomForm, TenantForm, LeaseForm, PaymentForm
from tkinter import messagebox, StringVar

def to_uppercase(var: StringVar) -> None:
    var.set(var.get().upper())

def valid_contact_number(contact_number: str) -> bool:
    return bool(re.match(r"^09[0-9]{9}", contact_number))

class RoomListController:
    def __init__(self, manager: BoardingHouseManager, window: RoomListWindow) -> None:
        self.manager = manager
        self.window = window
        
        self.set_actions()
        
        self.load_rooms()
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
        self.window.open_room_button.configure(command=self.open_room_pressed)
        self.window.delete_room_button.configure(command=self.delete_room_pressed)
        
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def load_rooms(self) -> None:
        for room in self.manager.get_all_rooms():
            self.window.rooms_treeview.insert(
                "",
                "end",
                room.room_number,
                values=(
                    f"Room {room.room_number}",
                    f"{room.tenant_count} / {room.max_capacity}"
                )
            )
    
    def add_room_pressed(self) -> None:
        RoomFormController(self, RoomForm())
    
    def open_room_pressed(self) -> None:
        if r := self.window.rooms_treeview.selection():
            room = self.manager.get_room(int(r[0]))
        else:
            return
        
        if room:
            RoomOpenController(self, RoomOpenWindow(), room)
            self.window.withdraw()
    
    def delete_room_pressed(self) -> None:
        if r := self.window.rooms_treeview.selection():
            room = self.manager.get_room(int(r[0]))
        else:
            return
        
        if room:
            messagebox.showwarning("Delete Room", message="You are about to delete a room.")
            
            if messagebox.askyesno(
                title="Delete Room",
                message=f"Are you sure you want to delete Room {room.room_number}?"
            ):
                self.manager.delete_room(room)
                messagebox.showinfo(
                    title="Room Deleted",
                    message="Room deleted successfully."
                )
                
                self.load_rooms()
    
    def close(self) -> None:
        self.window.destroy()
        self.manager.close_session()

class RoomFormController:
    def __init__(self, parent: RoomListController, window: RoomForm) -> None:
        self.parent = parent
        self.window = window
        
        self.set_actions()
        self.set_validations()
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
    
    def set_validations(self) -> None:
        self.window.max_capacity_entry.configure(
            validate='key', 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                '%S'
            )
        )
    
    def add_room_pressed(self) -> None:
        if ((max_cap := self.window.max_capacity_entry.get()).isnumeric()) and int(max_cap) > 0:
            max_cap = int(max_cap)
            
            room = self.parent.manager.add_room(Room(max_capacity=max_cap))
            
            self.window.destroy()
            
            self.parent.load_rooms()
            
            messagebox.showinfo(
                title="Room Added",
                message=f"Room {room.room_number} with max capacity {room.max_capacity} sucessfully added."
            )
        
        else:
            messagebox.showerror(
                title="Invalid Max Capacity",
                message="Max capacity entered is invalid."
            )

class RoomOpenController:
    def __init__(self, parent: RoomListController, window: RoomOpenWindow, room: Room) -> None:
        self.parent = parent
        self.window = window
        self.room = room
        
        self.set_actions()
        
        self.load_data()
    
    def set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.delete_tenant_button.configure(command=self.delete_tenant_pressed)
        self.window.delete_payment_button.configure(command=self.delete_payment_pressed)
        self.window.edit_tenant_button.configure(command=self.edit_tenant_pressed)
        self.window.edit_payment_button.configure(command=self.edit_payment_pressed)
        
        self.window.add_tenant_button.configure(command=self.add_tenant_pressed)
        self.window.add_payment_button.configure(command=self.add_payment_pressed)
        
        self.window.edit_room_button.configure(command=self.edit_payment_pressed)
        self.window.add_lease_button.configure(command=self.add_lease_pressed)
    
    def load_data(self) -> None:
        self.window.room_number_label.configure(text=f"Room Number: {self.room.room_number}")
        self.window.tenant_count_label.configure(text=f"Tenant Count: {self.room.tenant_count}")
        self.window.max_capacity_label.configure(text=f"Max Capacity: {self.room.max_capacity}")
        
        lease = self.room.lease
        
        self.window.lease_start_label.configure(
            text=f"Lease Start: {lease.lease_start}" if lease else "Lease Start: "
        )
        self.window.lease_end_label.configure(
            text=f"Lease End: {lease.lease_start}" if lease else "Lease End: "
        )
        self.window.lease_deposit_label.configure(
            text=f"Deposit: {lease.deposit_amount}" if lease else "Deposit: "
        )
        self.window.lease_rent_label.configure(
            text=f"Rent: {lease.monthly_rent_mount}" if lease else "Rent: "
        )
        
        self.window.add_lease_button.configure(text="Delete Lease" if lease else "Add Lease")
        
        if self.room.tenants:
            for tenant in self.room.tenants:
                self.window.tenants_treeview.insert(
                    "",
                    "end",
                    tenant.tenant_id,
                    values=(
                        tenant.formatted_name,
                        tenant.contact_number,
                        tenant.birth_date
                    )
                )
        else:
            self.window.tenants_treeview.delete(*self.window.tenants_treeview.get_children())
        
        if lease:
            for payment in lease.payments:
                self.window.payments_treeview.insert(
                    "",
                    "end",
                    payment.payment_id,
                    values=(
                        payment.payment_date,
                        payment.payment_amount,
                        "Paid" if payment.paid else "Unpaid"
                    )
                )
        else:
            self.window.payments_treeview.delete(*self.window.payments_treeview.get_children())
    
    def delete_tenant_pressed(self) -> None:
        if t := self.window.tenants_treeview.selection():
            tenant = self.parent.manager.get_tenant(int(t[0]))
        else:
            return
        
        if tenant:
            if tenant == self.room.lease.leaser:
                messagebox.showerror(title="Leaser Deletion", message="You are not allowed to delete the leaser.")
                return
            
            messagebox.showwarning("Delete Tenant", message="You are about to delete a room.")
            
            if messagebox.askyesno(
                title="Delete Tenant",
                message=f"Are you sure you want to delete {tenant.formatted_name}?"
            ):
                self.parent.manager.delete_tenant(tenant)
                messagebox.showinfo(
                    title="Tenant Deleted",
                    message="Tenant deleted successfully."
                )
                
                self.load_data()
    
    def delete_payment_pressed(self) -> None:
        if p := self.window.payments_treeview.selection():
            payment = self.parent.manager.get_payment(int(p[0]))
        else:
            return

        messagebox.showwarning("Delete Payment", message="You are about to delete a payment record.")
        
        if payment:
            if messagebox.askyesno(
                title="Delete Payment",
                message=f"Are you sure you want to delete {payment}?"
            ):
                self.parent.manager.delete_tenant(payment)
                messagebox.showinfo(
                    title="Payment Deleted",
                    message="Payment Record deleted successfully."
                )
                
                self.load_data()
    
    def edit_tenant_pressed(self) -> None:
        ...
    
    def edit_payment_pressed(self) -> None:
        ...
    
    def add_tenant_pressed(self) -> None:
        ...
        
    def add_payment_pressed(self) -> None:
        ...
    
    def edit_room_pressed(self) -> None:
        ...
        
    def add_lease_pressed(self) -> None:
        ...
        
    def close(self) -> None:
        self.window.destroy()
        self.parent.window.deiconify()
        
    
class TenantFormController:
    def __init__(self, parent: RoomOpenController, window: TenantForm, tenant: Tenant) -> None:
        self.parent = parent
        self.window = window
        self.tenant = tenant
    
    def set_validations(self) -> None:
        ...
    
    def set_formatters(self) -> None:
        ...
    
    def set_actions(self) -> None:
        self.window.add_tenant_button.configure(command=self.add_tenant_pressed)
    
    def add_tenant_pressed(self) -> None:
        lastname: str = self.window.lastname_entry.get().strip().upper()
        firstname: str = self.window.firstname_entry.get().strip().upper()
        middlename: str = self.window.middlename_entry.get().strip().upper()
        contact: str = self.window.contactnumber_entry.get().strip()
        bdate: date = self.window.birthdate_dateentry.get_date()
        
        vl = lastname.isalpha()
        vf = firstname.isalpha()
        vm = middlename.isalpha() or middlename == ""
        vc = valid_contact_number(contact)
        
        room_number = int(self.parent.window.room_number_label["text"].split(":")[1].strip())
        
        if vl and vf and vm and vc:
            tenant = self.parent.parent.manager.add_tenant(Tenant(
                last_name=lastname,
                first_name=firstname,
                middle_name=middlename,
                birth_date=bdate,
                contact_number=contact,
                room_number=room_number
            ))
            
            self.parent.load_data()
            
            self.window.destroy()
            
            messagebox.showinfo(
                title="Tenant Added",
                message=f"Tenant {tenant.formatted_name} added successfully."
            )
        
        else:
            messagebox.showerror(
                title="Error",
                message="Error in adding tenant. At least one of the inputs are invalid."
            )
        
