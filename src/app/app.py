from src.views.forms import LoginForm
from src.controllers.controller import LoginFormController

class App:
   def __init__(self) -> None:
      self.main_window = LoginForm()
      
   def start(self) -> None:
      LoginFormController(self.main_window)
      
      self.main_window.eval("tk::PlaceWindow . center")
      self.main_window.mainloop()