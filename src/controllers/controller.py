from __future__ import annotations

from typing import Optional
from datetime import date
import re

from views.forms import RoomForm, TenantForm, LeaseForm, PaymentForm
from views.rooms import RoomListWindow, RoomOpenWindow
from models.entities import Room, Tenant, Lease, Payment
from managers.manager import BoardingHouseManager

from tkinter import messagebox, StringVar

def to_uppercase(var: StringVar) -> None:
    var.set(var.get().upper())

def valid_contact_number(contact_number: str) -> bool:
    return bool(re.match(r"^09[0-9]{9}", contact_number))

class RoomListController:
    def __init__(
        self, 
        manager: BoardingHouseManager, 
        window: RoomListWindow
    ) -> None:
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
    def __init__(self, parent: RoomListController, window: RoomForm, room: Room) -> None:
        self.parent = parent
        self.window = window
        
        self.set_actions()
        self.set_validations()
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
    
    def set_validations(self) -> None:
        self.window.max_capacity_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
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
    def __init__(
        self, 
        parent: RoomListController, 
        window: RoomOpenWindow, 
        room: Room
    ) -> None:
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
    def __init__(
        self, 
        parent: RoomOpenController, 
        window: TenantForm, 
        tenant: Optional[Tenant] = None
    ) -> None:
        self.parent = parent
        self.window = window
        
        self.set_validations()
        self.set_formatters()
        self.set_actions()
        
        if tenant:
            self.tenant = tenant
            self.load_data()
    
    def set_validations(self) -> None:
        self.window.lastname_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == ""), 
                "%S"
            )
        )
        self.window.firstname_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == ""), 
                "%S"
            )
        )
        self.window.middlename_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == ""), 
                "%S"
            )
        )
        self.window.contactnumber_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
    
    def set_formatters(self) -> None:
        lname_var = StringVar()
        fname_var = StringVar()
        mname_var = StringVar()
        contc_var = StringVar()
        
        self.window.lastname_entry.configure(textvariable=lname_var)
        self.window.firstname_entry.configure(textvariable=fname_var)
        self.window.middlename_entry.configure(textvariable=mname_var)
        self.window.contactnumber_entry.configure(textvariable=contc_var)
        
        lname_var.trace_add("write", lambda *_: to_uppercase(lname_var))
        fname_var.trace_add("write", lambda *_: to_uppercase(fname_var))
        mname_var.trace_add("write", lambda *_: to_uppercase(mname_var))
        contc_var.trace_add("write", lambda *_: to_uppercase(contc_var))
    
    def set_actions(self) -> None:
        self.window.add_tenant_button.configure(command=self.add_tenant_pressed)
        
    def load_data(self) -> None:
        self.window.lastname_entry.cget("textvariable").set(self.tenant.last_name)
        self.window.firstname_entry.cget("textvariable").set(self.tenant.first_name)
        self.window.middlename_entry.cget("textvariable").set(self.tenant.middle_name)
        self.window.contactnumber_entry.cget("textvariable").set(self.tenant.contact_number)
        self.window.birthdate_dateentry.set_date(self.tenant.birth_date)
    
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
        
        if vl and vf and vm and vc:
            if self.tenant:
                self.tenant.last_name = lastname
                self.tenant.first_name = firstname
                self.tenant.middle_name = middlename
                self.tenant.birth_date = bdate
                self.tenant.contact_number = contact
                
                self.parent.parent.manager.update_tenant(self.tenant)
                
                title = "Tenant Updated"
                message = f"{self.tenant}'s information was updated successfully."
            
            else:
                tenant = self.parent.parent.manager.add_tenant(Tenant(
                    last_name=lastname,
                    first_name=firstname,
                    middle_name=middlename,
                    birth_date=bdate,
                    contact_number=contact,
                    room_number=int(self.parent.window.room_number_label["text"].split(":")[1].strip())
                ))
                
                title = "Tenant Added"
                message = f"{tenant.formatted_name} was added successfully."
            
            self.parent.load_data()
            
            self.window.destroy()
            
            messagebox.showinfo(title=title, message=message)
        
        else:
            messagebox.showerror(
                title="Error",
                message="At least one of the inputs are invalid."
            )
        
class LeaseFormController:
    def __init__(self, parent: RoomOpenController, window: LeaseForm, lease: Lease = None) -> None:
        self.parent = parent
        self.window = window
        self.lease = lease
        
        self.populate_leaser_combobox()
        self.set_actions()
        self.set_initial_values()
    
    def populate_leaser_combobox(self) -> None:
        leasers = self.parent.manager.get_all_tenants()
        leaser_names = [f"{leaser.first_name} {leaser.last_name}" for leaser in leasers]
        self.window.leaser_combobox["values"] = leaser_names
    
    def set_actions(self) -> None:
        self.window.add_lease_button.configure(command=self.add_lease_pressed)
    
    def set_initial_values(self) -> None:
        if self.lease:
            self.window.leaser_combobox.set(f"{self.lease.leaser.first_name} {self.lease.leaser.last_name}")
            self.window.startdate_entry.set_date(self.lease.lease_start)
            self.window.enddate_entry.set_date(self.lease.lease_end)
            self.window.deposit_entry.insert(0, str(self.lease.deposit_amount))
            self.window.rent_entry.insert(0, str(self.lease.monthly_rentAmount))
    
    def add_lease_pressed(self) -> None:
        leaser_name = self.window.leaser_combobox.get()
        leaser_first_name, leaser_last_name = leaser_name.split(" ", 1)
        leaser = self.parent.manager.get_tenant_by_name(leaser_first_name, leaser_last_name)
        
        if not leaser:
            messagebox.showerror(
                title="Leaser Not Found",
                message="Selected leaser not found. Please select a valid leaser."
            )
            return
        
        lease_start = self.window.startdate_entry.get_date()
        lease_end = self.window.enddate_entry.get_date()
        deposit_amount = self.window.deposit_entry.get()
        monthly_rentAmount = self.window.rent_entry.get()
        
        if not (lease_start and lease_end and deposit_amount and monthly_rentAmount):
            messagebox.showerror(
                title="Error",
                message="Fill out all the fields."
            )
            return
        
        lease_data = {
            "leaser": leaser,
            "lease_start": lease_start,
            "lease_end": lease_end,
            "deposit_amount": float(deposit_amount),
            "monthly_rentAmount": float(monthly_rentAmount)
        }
        
        if self.lease:
            lease = Lease(**lease_data, lease_id=self.lease.lease_id)
            self.parent.manager.update_lease(lease)
            messagebox.showinfo(
                title="Lease Updated",
                message=f"Lease {self.lease.lease_id} successfully updated."
            )
        else:
            lease = self.parent.manager.add_lease(Lease(**lease_data))
            messagebox.showinfo(
                title="Lease Added",
                message=f"Lease {lease.lease_id} successfully added."
            )
        
        self.window.destroy()
        self.parent.window.deiconify()
        self.parent.load_leases()
