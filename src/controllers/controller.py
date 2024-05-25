
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
