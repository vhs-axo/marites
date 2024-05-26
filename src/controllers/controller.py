from __future__ import annotations

from decimal import Decimal
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

def valid_amount(amount: str) -> bool:
    try:
        float(amount)
    except:
        return False
    else:
        return True

class RoomListController:
    def __init__(
        self, 
        manager: BoardingHouseManager, 
        window: RoomListWindow
    ) -> None:
        self.manager = manager
        self.window = window
        
        self.set_validations()
        self.set_actions()
        
        self.load_rooms()
    
    def set_validations(self) -> None:
        self.window.search_room_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
        self.window.open_room_button.configure(command=self.open_room_pressed)
        self.window.delete_room_button.configure(command=self.delete_room_pressed)
        
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def load_rooms(self, search: str = "") -> None:
        self.window.rooms_treeview.delete(*self.window.rooms_treeview.get_children())
        
        for room in filter(lambda r: search in str(r.room_number), self.manager.get_all_rooms()):
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
    def __init__(
        self, 
        parent: RoomListController, 
        window: RoomForm, 
        room: Optional[Room] = None
    ) -> None:
        self.parent = parent
        self.window = window
        
        self.set_validations()
        self.set_formatters()
        self.set_actions()
        
        if room:
            self.room = room
            self.load_data()
    
    def set_validations(self) -> None:
        self.window.max_capacity_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
    
    def set_formatters(self) -> None:
        mxcap_var = StringVar()
        
        self.window.max_capacity_entry.configure(textvariable=mxcap_var)
        
        mxcap_var.trace_add("write", lambda *_: to_uppercase(mxcap_var))
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
        
    def load_data(self) -> None:
        if self.room:
            self.window.max_capacity_entry.cget("textvariable").set(self.room.max_capacity)
    
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
            
            del self
        
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
        
        self.window.edit_room_button.configure(command=self.edit_room_pressed)
        self.window.add_lease_button.configure(command=self.add_lease_pressed)
    
    def load_data(self) -> None:
        self.load_room()
        self.load_lease()
        self.load_tenants()        
        self.load_payments()        
    
    def load_room(self) -> None:
        self.window.room_number_label.configure(text=f"Room Number: {self.room.room_number}")
        self.window.tenant_count_label.configure(text=f"Tenant Count: {self.room.tenant_count}")
        self.window.max_capacity_label.configure(text=f"Max Capacity: {self.room.max_capacity}")
    
    def load_lease(self) -> None:
        self.window.lease_start_label.configure(
            text=f"Lease Start: {self.room.lease.lease_start}" if self.room.lease else "Lease Start: "
        )
        self.window.lease_end_label.configure(
            text=f"Lease End: {self.room.lease.lease_start}" if self.room.lease else "Lease End: "
        )
        self.window.lease_deposit_label.configure(
            text=f"Deposit: {self.room.lease.deposit_amount}" if self.room.lease else "Deposit: "
        )
        self.window.lease_rent_label.configure(
            text=f"Rent: {self.room.lease.monthly_rent_mount}" if self.room.lease else "Rent: "
        )
        
        self.window.add_lease_button.configure(text="Delete Lease" if self.room.lease else "Add Lease")
        self.window.add_payment_button.configure(state="normal" if self.room.lease else "disabled")
    
    def load_tenants(self) -> None:
        self.window.tenants_treeview.delete(*self.window.tenants_treeview.get_children())
        
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
    
    def load_payments(self) -> None:
        self.window.payments_treeview.delete(*self.window.payments_treeview.get_children())
        
        if self.room.lease:
            for payment in self.room.lease.payments:
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
        if (s := self.window.tenants_treeview.selection()):
            tenant_id = int(s[0])
        
        tenant = self.parent.manager.get_tenant(tenant_id)
        
        TenantFormController(self, TenantForm(self.window))
    
    def edit_payment_pressed(self) -> None:
        ...
    
    def add_tenant_pressed(self) -> None:
        TenantFormController(self, TenantForm(self.window))
        
    def add_payment_pressed(self) -> None:
        ...
    
    def edit_room_pressed(self) -> None:
        ...
        
    def add_lease_pressed(self) -> None:
        if self.room.lease:
            messagebox.showwarning("Delete Lease", message="You are about to delete the lease.")
            
            if messagebox.askyesno(
                title="Delete Lease",
                message=f"Are you sure you want to delete the lease?"
            ):
                self.parent.manager.delete_lease(self.room.lease)
                messagebox.showinfo(
                    title="Lease Deleted",
                    message="Lease deleted successfully."
                )
                
                self.load_lease()
                self.load_payments()
        else:
            LeaseFormController(self, LeaseForm(self.window))
        
    def close(self) -> None:
        self.window.destroy()
        self.parent.window.deiconify()
        del self
    
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
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
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
            if hasattr(self, "tenant") and self.tenant:
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
    
    def close(self) -> None:
        self.window.destroy()
        del self
    
class LeaseFormController:
    def __init__(
        self, 
        parent: RoomOpenController, 
        window: LeaseForm
    ) -> None:
        self.parent = parent
        self.window = window
        
        self.set_validations()
        self.set_actions()
        
        self.populate_leaser_combobox()
    
    def set_validations(self) -> None:
        self.window.deposit_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == "" or change == "."), 
                "%S"
            )
        )
        self.window.rent_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == "" or change == "."), 
                "%S"
            )
        )
    
    def set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.add_lease_button.configure(command=self.add_lease_pressed)
    
    def populate_leaser_combobox(self) -> None:
        leasers = self.parent.room.tenants
        leaser_names = (f"{leaser.tenant_id} {leaser.formatted_name}" for leaser in leasers)
        self.window.leaser_combobox["values"] = leaser_names
    
    def add_lease_pressed(self) -> None:
        leaser_id: str = self.window.leaser_combobox.get().split("|")[0].strip()
        start_date: date = self.window.startdate_entry.get_date()
        end_date: date = self.window.enddate_entry.get_date()
        deposit: str = self.window.deposit_entry.get().strip()
        rent: str = self.window.rent_entry.get().strip()
        
        vl = leaser_id.isnumeric()
        vd = valid_amount(deposit)
        vr = valid_amount(rent)
        ve = end_date < start_date
        
        if (vl and vd and vr and ve):
            self.parent.parent.manager.add_lease(Lease(
                leaser_id=leaser_id,
                room_number=self.parent.room.room_number,
                lese_start=start_date,
                lease_end=end_date,
                deposit_amount=Decimal(deposit),
                monthly_rent_amount=Decimal(rent)
            ))
            
            self.parent.load_lease()
            
            self.window.destroy()
            
            messagebox.showinfo(title="Lease Added", message="Lease added successfully.")
            
            del self
        
        else:
            messagebox.showerror(
                title="Lease Adding Error", 
                message="At least one of the inputs are invalid."
            )

    def close(self) -> None:
        self.window.destroy()
        del self

class PaymentFormController:
    def __init__(self, parent: SomeParentController, window: PaymentForm, payment: Payment = None) -> None:
        self.parent = parent
        self.window = window
        self.payment = payment
        
        self.set_actions()
        self.set_initial_values()
    
    def set_actions(self) -> None:
        self.window.add_payment_button.configure(command=self.add_payment_pressed)
    
    def set_initial_values(self) -> None:
        if self.payment:
            self.window.payment_date_entry.set_date(self.payment.payment_date)
            self.window.payment_amount_entry.insert(0, str(self.payment.amount))
            self.window.paid_checkbutton.select() if self.payment.paid else self.window.paid_checkbutton.deselect()
    
    def add_payment_pressed(self) -> None:
        payment_date = self.window.payment_date_entry.get_date()
        payment_amount = self.window.payment_amount_entry.get()
        paid = self.window.paid_checkbutton.instate(['selected'])

        if not payment_date or not payment_amount:
            messagebox.showerror(
                title="Error",
                message="Please fill out all the required fields."
            )
            return

        try:
            amount = float(payment_amount)
        except ValueError:
            messagebox.showerror(
                title="Invalid Amount",
                message="The amount entered is not a valid number."
            )
            return

        payment_data = {
            'payment_date': payment_date,
            'amount': amount,
            'paid': paid
        }

        if self.payment:
            payment = Payment(**payment_data, payment_id=self.payment.payment_id)
            self.parent.manager.update_payment(payment)
            messagebox.showinfo(
                title="Payment Updated",
                message=f"Payment {self.payment.payment_id} successfully updated."
            )
        else:
            payment = self.parent.manager.add_payment(Payment(**payment_data))
            messagebox.showinfo(
                title="Payment Added",
                message=f"Payment {payment.payment_id} successfully added."
            )

        self.window.destroy()
        self.parent.window.deiconify()
        self.parent.load_payments()
