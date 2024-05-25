
from managers.manager import BoardingHouseManager
from models.entities import Room, Tenant, Lease, Payment
from services.service import SessionFactory
from views.rooms import RoomListWindow, RoomOpenWindow
from views.forms import RoomForm, TenantForm, LeaseForm, PaymentForm
from tkinter import messagebox

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
        self.window.withdraw()
    
    def open_room_pressed(self) -> None:
        if r := self.window.rooms_treeview.selection():
            room = self.manager.get_room(int(r[0]))
        else:
            return
        
        if room:
            RoomOpenController(self, RoomOpenWindow(), room)
    
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
            self.parent.window.deiconify()
            
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
        ...
    
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
            tenant = self.parent.manager.get_room(int(t[0]))
        else:
            return
        
        if tenant:
            if tenant 
            
            messagebox.showwarning("Delete Tenant", message="You are about to delete a room.")
            
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
    
class TenantFormController:
    def __init__(self, manager: BoardingHouseManager, parent_window: Tk) -> None:
        self.manager = manager
        self.parent_window = parent_window
        self.window = TenantForm(parent_window)
        self.window.add_tenant_button.config(command=self.add_tenant)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        last_name = self.window.lastname_entry.get()
        first_name = self.window.firstname_entry.get()
        middle_name = self.window.middlename_entry.get()
        contact_number = self.window.contactnumber_entry.get()
        birth_date = self.window.birthdate_dateentry.get_date()
        
        tenant_data = {
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'contact_number': contact_number,
            'birth_date': birth_date
        }
        result = self.manager.add_tenant(tenant_data) 
        
        if result:
            messagebox.showinfo("Success", "Tenant added successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Failed to add tenant!")

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
        self.window.leaser_combobox['values'] = leaser_names
    
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
            'leaser': leaser,
            'lease_start': lease_start,
            'lease_end': lease_end,
            'deposit_amount': float(deposit_amount),
            'monthly_rentAmount': float(monthly_rentAmount)
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
