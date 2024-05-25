from __future__ import annotations
from tkinter import Tk, Toplevel, Event
from tkinter.ttk import Treeview, Style, Combobox, Button, Label, Entry, Scrollbar

class RoomForm(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
        
    def __init_labels(self) -> None:
        self.max_capacity_label = Label(master=self, text="Max Capacity")
    
    def __init_entries(self) -> None:
        self.max_capacity_entry = Entry(master=self)
    
    def __init_buttons(self) -> None:
        self.add_room_button = Button(master=self, text="Add Room")
    
    def __set_layout(self) -> None:
        self.max_capacity_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        
        self.max_capacity_entry.grid(
            row=1, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.add_room_button.grid(
            row=2, column=1, rowspan=1, columnspan=1,
            sticky="e", padx=(7, 7), pady=(7, 7)
        )
        
        self.title("")
        self.resizable(False, False)
        
class TenantForm

def main() -> None:
   RoomForm().mainloop()

if __name__ == "__main__":
   main()