from tkinter import messagebox
from tkinter import Tk
from managers.manager import BoardingHouseManager
from views.rooms import RoomListWindow, RoomOpenWindow
from views.forms import RoomForm, TenantForm, LeaseForm, PaymentForm

class RoomListController:
    def __init__(self, manager: BoardingHouseManager, window: RoomListWindow) -> None:
        self.manager = manager
        self.window = window
    
    def load_rooms(self):
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
class RoomFormController:
    def __init__(self, manager: BoardingHouseManager, parent_window: Tk) -> None:
        self.manager = manager
        self.parent_window = parent_window
        self.window = RoomForm()
        self.window.add_room_button.config(command=self.add_room)
    
    def add_room(self) -> None:
        max_capacity = int(self.window.max_capacity_entry.get())
        
        if max_capacity <= 0:
            messagebox.showerror("Error", "Max capacity must be a positive integer.")
            return
        
        success = self.manager.add_room(max_capacity)
        if success:
            self.window.destroy()
            messagebox.showinfo("Success", "Room added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add room.")

class LeaseFormController:
    def __init__(self, manager: BoardingHouseManager, parent_window: Tk, lease_data: dict = None) -> None:
        self.manager = manager
        self.parent_window = parent_window
        self.lease_data = lease_data
        self.window = LeaseForm(self.parent_window, lease_data=self.lease_data)
        self.window.save_button.config(command=self.save_lease)
    
    def save_lease(self) -> None:
        start_date = self.window.start_date_entry.get_date()
        end_date = self.window.end_date_entry.get_date()
        deposit_amount = float(self.window.deposit_entry.get())
        monthly_rent_amount = float(self.window.rent_entry.get())
        
        success = self.manager.add_lease(start_date, end_date, deposit_amount, monthly_rent_amount)
        if success:
            self.window.destroy()
            messagebox.showinfo("Success", "Lease saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to save lease.")
            
class PaymentFormController:
    def __init__(self, manager: BoardingHouseManager, parent_window: Tk, payment_data: dict = None) -> None:
        self.manager = manager
        self.parent_window = parent_window
        self.payment_data = payment_data
        self.window = PaymentForm(self.parent_window, payment_data=self.payment_data)
        self.window.save_button.config(command=self.save_payment)
    
    def save_payment(self) -> None:
        payment_date = self.window.payment_date_entry.get_date()
        payment_amount = float(self.window.payment_amount_entry.get())
        
        success = self.manager.add_payment(payment_date, payment_amount)
        if success:
            self.window.destroy()
            messagebox.showinfo("Success", "Payment saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to save payment.")

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
