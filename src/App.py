from src.managers.manager import BoardingHouseManager
from src.services.service import SessionFactory
from src.views.rooms import RoomListWindow
from src.controllers.controller import RoomListController

class App:
   def __init__(self, username: str, password: str) -> None:
      self.manager = BoardingHouseManager(SessionFactory(username, password).get_session())
      self.main_window = RoomListWindow()
      
   def start(self) -> None:
      RoomListController(self.manager, self.main_window)
      
      self.main_window.mainloop()