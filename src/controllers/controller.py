from __future__ import annotations

from decimal import Decimal
from typing import Optional
from datetime import date
from re import match

from sqlalchemy.exc import OperationalError

from src.services.service import SessionFactory
from src.views.forms import RoomForm, TenantForm, LeaseForm, PaymentForm, LoginForm
from src.views.rooms import RoomListWindow, RoomOpenWindow
from src.models.entities import Room, Tenant, Lease, Payment
from src.managers.manager import BoardingHouseManager

from tkinter import messagebox, StringVar

def to_uppercase(var: StringVar) -> None:
    var.set(var.get().upper())

def valid_contact_number(contact_number: str) -> bool:
    return bool(match(r"^09[0-9]{9}", contact_number))

def valid_amount(amount: str) -> bool:
    try:
        float(amount)
    except:
        return False
    else:
        return True

class LoginFormController:
    def __init__(self, window: LoginForm) -> None:
        self.window = window
        
        self.__set_formatters()
        self.__set_actions()
    
    def __set_formatters(self) -> None:
        self.un_var = StringVar(master=self.window)
        self.pw_var = StringVar(master=self.window)
        
        self.window.username_entry.configure(textvariable=self.un_var)
        self.window.password_entry.configure(textvariable=self.pw_var)
    
    def __set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.login_button.configure(command=self.login_pressed)
        
    def login_pressed(self) -> None:
        username = self.un_var.get()
        password = self.pw_var.get()
        
        try:
            self.session = SessionFactory(username, password).get_session()
        
        except OperationalError as err:
            print(err)
            
            messagebox.showerror(
                title="Login Failed",
                message="Username and/or password not recognized."
            )
            
            self.un_var.set("")
            self.pw_var.set("")
        
        else:
            RoomListController(
                BoardingHouseManager(self.session),
                RoomListWindow()
            )
            
            self.window.destroy()
            
            del self
    
    def close(self) -> None:
        self.window.destroy()
        
        if hasattr(self, "session"):
            self.session.close()
        
        del self

class RoomListController:
    def __init__(
        self, 
        manager: BoardingHouseManager, 
        window: RoomListWindow
    ) -> None:
        self.manager = manager
        self.window = window
        
        self.set_formatters()
        self.set_validations()
        self.set_actions()
        
        self.load_rooms()
  
    def set_formatters(self) -> None:
        self.search_var = StringVar(master=self.window)
        
        self.window.search_room_entry.configure(textvariable=self.search_var)

    def set_validations(self) -> None:
        self.window.search_room_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
    
    def set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.add_room_button.configure(command=self.add_room_pressed)
        self.window.open_room_button.configure(command=self.open_room_pressed)
        self.window.delete_room_button.configure(command=self.delete_room_pressed)
        
        self.search_var.trace_add(
            "write", 
            lambda *_: self.load_rooms()
        )
    
    def load_rooms(self) -> None:
        self.window.rooms_treeview.delete(*self.window.rooms_treeview.get_children())
        
        for room in filter(
            lambda r: self.search_var.get() in str(r.room_number), 
            self.manager.get_all_rooms()
        ):
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
        RoomFormController(self, RoomForm(self.window))
    
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
                message=f"Are you sure you want to delete Room {room.room_number}?\nDoing so will also delete all records under this room, such as tenants, lease, and payments."
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
        
        del self

class RoomFormController:
    def __init__(
        self, 
        parent: RoomListController | RoomOpenController, 
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
        
        self.__set_state()
        
    def __set_state(self) -> None:
        if hasattr(self, "room") and self.room:
            self.window.add_room_button.configure(text="Save Changes")
        
        else:
            self.window.add_room_button.configure(text="Add Room")
    
    def set_validations(self) -> None:
        self.window.room_number_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
        self.window.max_capacity_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == ""), 
                "%S"
            )
        )
    
    def set_formatters(self) -> None:
        self.rmnum_var = StringVar(master=self.window)
        self.mxcap_var = StringVar(master=self.window)
        
        self.window.room_number_entry.configure(textvariable=self.rmnum_var)
        self.window.max_capacity_entry.configure(textvariable=self.mxcap_var)
    
    def set_actions(self) -> None:
        self.window.add_room_button.configure(command=self.add_room_pressed)
    
    def load_data(self) -> None:
        if self.room:
            self.rmnum_var.set(str(self.room.room_number))
            self.mxcap_var.set(str(self.room.max_capacity))
            
            self.window.room_number_entry.configure(state="disabled")
    
    def add_room_pressed(self) -> None:
        room_num = self.rmnum_var.get()
        max_cap = self.mxcap_var.get()
        
        vr = room_num.isnumeric() and int(room_num) > 0
        vm = max_cap.isnumeric() and int(max_cap) > 0
        
        if vr and vm:
            room_num = int(room_num)
            max_cap = int(max_cap)
            
            if isinstance(self.parent, RoomListController):
                existing_room = self.parent.manager.get_room(room_num)
            
            if isinstance(self.parent, RoomOpenController):
                existing_room = self.parent.parent.manager.get_room(room_num)
            
            if existing_room:
                messagebox.showerror(
                    title="Duplicate Room",
                    message=f"A room with the room number {room_num} already exists."
                )
                return
            
            if hasattr(self, "room") and self.room:
                if max_cap < self.room.tenant_count:
                    messagebox.showerror(
                        title="Error", 
                        message="Tenant count is greater than the entered max capacity. Delete tenants first before changing."
                    )
                    return

                self.room.max_capacity = max_cap
                
                if isinstance(self.parent, RoomOpenController):
                    self.parent.parent.manager.update_room(self.room)
                
                title="Room Updated"
                message=f"Room {self.room.room_number} has been updated to have a max of {self.room.max_capacity} occupants."
            
            else:
                if isinstance(self.parent, RoomListController):
                    room = self.parent.manager.add_room(Room(
                        room_number=room_num,
                        max_capacity=max_cap
                    ))
                
                title="Room Added"
                message=f"Room {room.room_number} with max capacity {room.max_capacity} sucessfully added."
            
            self.window.destroy()
            
            if isinstance(self.parent, RoomListController):
                self.parent.load_rooms()
            
            if isinstance(self.parent, RoomOpenController):
                self.parent.load_room()
            
            messagebox.showinfo(title=title, message=message)
            
            del self
        
        else:
            messagebox.showerror(
                title="Invalid Entries",
                message="At least one of the inputs entered are invalid. Room Number & Max Capacity cannot be less than 1."
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
        self.window.title(f"Room {self.room.room_number}")
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
            text=f"Rent: {self.room.lease.monthly_rent_amount}" if self.room.lease else "Rent: "
        )
        self.window.leaser_label.configure(
            text=f"Leaser: {self.room.lease.leaser.formatted_name}" if self.room.lease else "Leaser: "
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
            for payment in reversed(self.room.lease.payments):
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
            if self.room.lease and tenant == self.room.lease.leaser:
                messagebox.showerror(title="Leaser Deletion", message="You are not allowed to delete the leaser.")
                return
            
            messagebox.showwarning("Delete Tenant", message="You are about to delete a tenant.")
            
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
            tenant = self.parent.manager.get_tenant(int(s[0]))
        
        if tenant:
            TenantFormController(self, TenantForm(self.window), tenant)
    
    def edit_payment_pressed(self) -> None:
        lease = self.room.lease
        
        if (s := self.window.payments_treeview.selection()):
            payment = self.parent.manager.get_payment(int(s[0]))
            
        if lease and payment:
            PaymentFormController(self, PaymentForm(self.window), lease, payment)
    
    def add_tenant_pressed(self) -> None:
        if self.room.tenant_count < self.room.max_capacity:
            TenantFormController(self, TenantForm(self.window))
        else:
            messagebox.showinfo(
                title="Max Capacity Reached",
                message="You can no longer add a tenant. Max capacity reached."
            )
        
    def add_payment_pressed(self) -> None:
        lease = self.room.lease
        
        if lease:
            PaymentFormController(self, PaymentForm(self.window), lease)
    
    def edit_room_pressed(self) -> None:
        RoomFormController(self, RoomForm(self.window), self.room)
        
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
        self.parent.load_rooms()
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
            
        self.__set_state()
    
    def __set_state(self) -> None:
        if hasattr(self, "tenant"):
            self.window.add_tenant_button.configure(text="Save Changes")
        else:
            self.window.add_tenant_button.configure(text="Add Tenant")
    
    def set_validations(self) -> None:
        self.window.lastname_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == "" or change.isspace()), 
                "%S"
            )
        )
        self.window.firstname_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == "" or change.isspace()), 
                "%S"
            )
        )
        self.window.middlename_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isalpha() or change == "" or change.isspace()), 
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
        self.lname_var = StringVar(master=self.window)
        self.fname_var = StringVar(master=self.window)
        self.mname_var = StringVar(master=self.window)
        self.contc_var = StringVar(master=self.window)
        
        self.window.lastname_entry.configure(textvariable=self.lname_var)
        self.window.firstname_entry.configure(textvariable=self.fname_var)
        self.window.middlename_entry.configure(textvariable=self.mname_var)
        self.window.contactnumber_entry.configure(textvariable=self.contc_var)
    
    def set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.add_tenant_button.configure(command=self.add_tenant_pressed)
        
        self.lname_var.trace_add("write", lambda *_: to_uppercase(self.lname_var))
        self.fname_var.trace_add("write", lambda *_: to_uppercase(self.fname_var))
        self.mname_var.trace_add("write", lambda *_: to_uppercase(self.mname_var))
        
    def load_data(self) -> None:
        self.lname_var.set(self.tenant.last_name)
        self.fname_var.set(self.tenant.first_name)
        self.mname_var.set(self.tenant.middle_name)
        self.contc_var.set(self.tenant.contact_number)
        self.window.birthdate_dateentry.set_date(self.tenant.birth_date)
    
    def add_tenant_pressed(self) -> None:
        lastname: str = self.window.lastname_entry.get().strip().upper()
        firstname: str = self.window.firstname_entry.get().strip().upper()
        middlename: str = self.window.middlename_entry.get().strip().upper()
        contact: str = self.window.contactnumber_entry.get().strip()
        bdate: date = self.window.birthdate_dateentry.get_date()
        
        vl = bool(lastname)
        vf = bool(firstname)
        vm = bool(middlename) or middlename == ""
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
        leaser_names = [f"{leaser.tenant_id} | {leaser.formatted_name}" for leaser in leasers]
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
        ve = end_date > start_date
        
        if (vl and vd and vr and ve):
            self.parent.parent.manager.add_lease(Lease(
                leaser_id=leaser_id,
                room_number=self.parent.room.room_number,
                lease_start=start_date,
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
    def __init__(
        self, 
        parent: RoomOpenController, 
        window: PaymentForm, 
        lease: Lease,
        payment: Optional[Payment] = None
    ) -> None:
        self.parent = parent
        self.window = window
        self.lease = lease

        self.set_validations()
        self.set_formatters()
        self.set_actions()
        
        if payment:
            self.payment = payment
            self.load_data()
        
        self.__set_state()
    
    def __set_state(self) -> None:
        if hasattr(self, "payment") and self.payment:
            self.window.add_payment_button.configure(text="Save Changes")
        else:
            self.window.add_payment_button.configure(text="Add Payment")
    
    def set_formatters(self) -> None:
        self.rent_var = StringVar(master=self.window)
        
        self.window.payment_amount_entry.configure(textvariable=self.rent_var)
    
    def set_validations(self) -> None:
        self.window.payment_amount_entry.configure(
            validate="key", 
            validatecommand=(
                self.window.register(lambda change: change.isdigit() or change == "" or change == "."), 
                "%S"
            )
        )
    
    def set_actions(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.window.add_payment_button.configure(command=self.add_payment_pressed)
    
    def load_data(self) -> None:
        if self.payment:
            self.window.payment_date_entry.set_date(self.payment.payment_date)
            self.rent_var.set(str(self.payment.payment_amount))
            self.window.paid_var.set(self.payment.paid)
    
    def add_payment_pressed(self) -> None:
        payment_date: date = self.window.payment_date_entry.get_date()
        payment_amount: str = self.window.payment_amount_entry.get().strip()
        paid: bool = self.window.paid_var.get()

        if valid_amount(payment_amount):
            if hasattr(self, "payment") and self.payment:
                self.payment.payment_date = payment_date
                self.payment.payment_amount = Decimal(payment_amount)
                self.payment.paid = paid
                
                title = "Payment Update"
                message = f"Payment on {self.payment.payment_date} worth {self.payment.payment_amount} has been updated successfully."
            
            else:
                payment = self.parent.parent.manager.add_payment(Payment(
                    lease_id=self.lease.lease_id,
                    payment_amount=payment_amount,
                    payment_date=payment_date,
                    paid=paid
                ))
                
                title = "Payment Added"
                message = f"Payment for {payment.payment_date} worth {payment.payment_amount} has been added successfully."
            
            self.parent.load_payments()
            
            self.window.destroy()
            
            messagebox.showinfo(title=title, message=message)
            
            del self
            
        else:
            messagebox.showerror(
                title="Payment Error",
                message="At least on of the inputs are invalid."
            )

    def close(self) -> None:
        self.window.destroy()
        del self
