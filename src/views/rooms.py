from __future__ import annotations
from tkinter import Tk, Toplevel, Event
from tkinter.ttk import Treeview, Style, Combobox, Button, Label, Entry, Scrollbar

def customization_buttons(
    tree: Treeview, 
    edit_button: Button, 
    delete_button: Button
) -> None:
    """
    Customize the appearance and behavior of buttons associated with a Treeview widget.

    Args:
        tree (Treeview): The Treeview widget.
        edit_button (CTkButton): The button used for editing.
        delete_button (CTkButton): The button used for deletion.
    """
    
    def show_buttons(event: Event):
        # Get the row index under the mouse cursor
        row = tree.identify_row(event.y)
        
        # If a row is under the cursor
        if row:
            # Calculate the position for the buttons
            try:
                x, y, w, h = tree.bbox(row)  # Adjust x-coordinate as needed
            except ValueError:
                return
            
            # Show buttons
            edit_button.place(x=tree.winfo_width() - 100, y=int(y), width=50, height=int(h))
            delete_button.place(x=tree.winfo_width() - 50, y=int(y), width=50, height=int(h))
            
            
            # # Set button sizes
            # edit_button.configure(width=50)
            # delete_button.configure(width=50)
            
            tree.selection_set(row)
        
        else:
            hide_buttons(event)
    
    def hide_buttons(event: Event):
        # Check if the mouse pointer is over the buttons
        if edit_button.winfo_containing(event.x_root, event.y_root) is edit_button or \
            delete_button.winfo_containing(event.x_root, event.y_root) is delete_button:
            return  # Do nothing if the mouse is over the buttons
        
        # Hide buttons
        edit_button.place_forget()
        delete_button.place_forget()
        tree.selection_remove(tree.selection())

    # Bind events
    tree.bind("<Motion>", show_buttons)  # Show buttons on mouse hover
    tree.bind("<Leave>", hide_buttons)

class RoomListWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_entries()
        self.__init_labels()
        self.__init_treeviews()
        self.__init_scrollbars()
        self.__init_buttons()
        
        self.__set_layout()
        
    def __init_entries(self) -> None:
        self.search_room_entry = Entry(master=self)
    
    def __init_labels(self) -> None:
        self.search_room_label = Label(master=self, text="Search Room: ")
        
    def __init_treeviews(self) -> None:
        self.rooms_treeview = Treeview(
            master=self,
            columns=("room_number", "occupancy"),
            show="headings",
            selectmode="browse"
        )
        
        self.rooms_treeview.heading(column="room_number", text="Room Number", anchor="w")
        self.rooms_treeview.heading(column="occupancy", text="Occupants", anchor="w")
        
        s = Style()
        s.configure("Treeview", rowheight=25)
    
    def __init_scrollbars(self) -> None:
        self.rooms_scrollbar = Scrollbar(
            self, 
            orient="vertical", 
            command=self.rooms_treeview.yview
        )
    
    def __init_buttons(self) -> None:
        self.add_room_button = Button(master=self, text="Add Room")
        self.open_room_button = Button(master=self.rooms_treeview, text="Open")
        self.delete_room_button = Button(master=self.rooms_treeview, text="Delete")
    
    def __set_layout(self) -> None:
        self.rowconfigure(0, weight=0, minsize=15)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(4, weight=0, minsize=5)
        
        self.search_room_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="ew", padx=(7, 0), pady=(7, 7)
        )
        self.search_room_entry.grid(
            row=0, column=1, rowspan=1, columnspan=1,
            sticky="w", padx=(0, 120), pady=(7, 7)
        )
        self.add_room_button.grid(
            row=0, column=3, rowspan=1, columnspan=2,
            sticky="e", padx=(14, 7), pady=(7, 7)
        )
        
        self.rooms_treeview.grid(
            row=1, column=0, rowspan=3, columnspan=4,
            sticky="nsew", padx=(7, 0), pady=(7, 7)
        )
        self.rooms_scrollbar.grid(
            row=1, column=4, rowspan=3, columnspan=1,
            sticky="nsew", padx=(0, 7), pady=(7, 7)
        )
        
        customization_buttons(self.rooms_treeview, self.open_room_button, self.delete_room_button)
        
        self.rooms_treeview.configure(yscrollcommand=self.rooms_scrollbar.set)
        
        self.title("MARITES")
        
        self.resizable(False, False)
        
def main() -> None:
   RoomListWindow().mainloop()

if __name__ == "__main__":
   main()