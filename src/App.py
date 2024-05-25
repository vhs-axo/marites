from managers.manager import BoardingHouseManager
from models.entities import *
from services.service import SessionFactory
from views.rooms import RoomListWindow
from controllers.controller import RoomListController
from datetime import date

def main() -> None:
   x = RoomListWindow()
   b = BoardingHouseManager(SessionFactory("root", "ax+vh$_jk&kr1").get_session())
   
   RoomListController(b, x)
   
   x.mainloop()

if __name__ == '__main__':
   main()