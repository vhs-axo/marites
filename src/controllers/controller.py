
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
    
    