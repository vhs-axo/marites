from managers.manager import BoardingHouseManager
from models.entities import *
from services.service import SessionFactory
from views.rooms import RoomListWindow
from controllers.controller import RoomListController
from datetime import date

class App:
   def __init__(self, username: str, password: str) -> None:
      self.manager = BoardingHouseManager(SessionFactory(username, password).get_session())
      self.main_window = RoomListWindow()
      
   def start(self) -> None:
      RoomListController(self.manager, self.main_window)
      
      self.main_window.mainloop()