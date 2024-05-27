from __future__ import annotations

from tkinter import Tk, Event
from tkinter.ttk import Treeview, Style, Button, Label, Entry, Scrollbar, Separator, Frame

import sv_ttk

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
            edit_button.place(x=tree.winfo_width() - 156, y=int(y), width=75, height=int(h))
            delete_button.place(x=tree.winfo_width() - 81, y=int(y), width=75, height=int(h))
            
            
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
    
    style = Style(edit_button.master)
    style.configure("Delete.TButton", background="red")

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
    
    def __init_scrollbars(self) -> None:
        self.rooms_scrollbar = Scrollbar(
            self, 
            orient="vertical", 
            command=self.rooms_treeview.yview
        )
    
    def __init_buttons(self) -> None:
        self.add_room_button = Button(master=self, text="Add Room", style="Accent.TButton")
        self.open_room_button = Button(master=self.rooms_treeview, text="Open")
        self.delete_room_button = Button(master=self.rooms_treeview, text="Delete", style="Accent.TButton")
    
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
            row=4, column=0, rowspan=1, columnspan=5,
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
        self.rooms_treeview.column(0, width=125, stretch=False)
        self.rooms_treeview.column(1, width=350, stretch=False)

        sv_ttk.set_theme("light", self)
        
        style = Style(self)
        
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", padding=(5, 0, 0, 0))
        
        self.title("MARITES")
        self.eval("tk::PlaceWindow . center")
        self.resizable(False, False)

class RoomOpenWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_frames()
        self.__init_labels()
        self.__init_treeviews()
        self.__init_scrollbars()
        self.__init_buttons()
        self.__init_separators()
        
        self.__set_layout()
    
    def __init_frames(self) -> None:
        self.room_tenant_frame = Frame(master=self)
        self.lease_payment_frame = Frame(master=self)

    def __init_labels(self) -> None:
        self.room_number_label = Label(master=self.room_tenant_frame, text="Room Number: [Number]")
        self.tenant_count_label = Label(master=self.room_tenant_frame, text="Tenant Count: [Count]")
        self.max_capacity_label = Label(master=self.room_tenant_frame, text="Max Capacity: [Max]")
        
        self.lease_start_label = Label(master=self.lease_payment_frame, text="Lease Start: [Start]")
        self.lease_end_label = Label(master=self.lease_payment_frame, text="Lease End: [End]")
        self.lease_deposit_label = Label(master=self.lease_payment_frame, text="Deposit: [Amount]")
        self.lease_rent_label = Label(master=self.lease_payment_frame, text="Rent: [Amount]")
        self.leaser_label = Label(master=self.lease_payment_frame, text="Leaser: [Name]")
        
        self.filler_label = Label(master=self.room_tenant_frame, text=" ")
    
    def __init_treeviews(self) -> None:
        self.tenants_treeview = Treeview(
            master=self.room_tenant_frame,
            columns=("tenant_name", "contact_number", "birth_date"),
            show="headings",
            selectmode="browse"
        )
        
        self.tenants_treeview.heading(column="tenant_name", text="Tenant Name", anchor="w")
        self.tenants_treeview.heading(column="contact_number", text="Contact Number", anchor="w")
        self.tenants_treeview.heading(column="birth_date", text="Birth Date", anchor="w")
        
        self.payments_treeview = Treeview(
            master=self.lease_payment_frame,
            columns=("payment_date", "payment_amount", "status"),
            show="headings",
            selectmode="browse"
        )
        
        self.payments_treeview.heading(column="payment_date", text="Payment Date", anchor="w")
        self.payments_treeview.heading(column="payment_amount", text="Amount", anchor="w")
        self.payments_treeview.heading(column="status", text="Status", anchor="w")
    
    def __init_scrollbars(self) -> None:
        self.tenants_scrollbar = Scrollbar(
            master=self.room_tenant_frame, 
            orient="vertical", 
            command=self.tenants_treeview.yview
        )
        
        self.payments_scrollbar = Scrollbar(
            master=self.lease_payment_frame, 
            orient="vertical", 
            command=self.payments_treeview.yview
        )
    
    def __init_buttons(self) -> None:
        self.edit_room_button = Button(master=self.room_tenant_frame, text="Edit Room")
        self.add_tenant_button = Button(master=self.room_tenant_frame, text="Add Tenant", style="Accent.TButton")
        self.add_lease_button = Button(master=self.lease_payment_frame, text="Add Lease")
        self.add_payment_button = Button(master=self.lease_payment_frame, text="Add Payment", style="Accent.TButton")
        
        self.edit_tenant_button = Button(master=self.tenants_treeview, text="Edit")
        self.delete_tenant_button = Button(master=self.tenants_treeview, text="Delete", style="Accent.TButton")
        
        self.edit_payment_button = Button(master=self.payments_treeview, text="Edit")
        self.delete_payment_button = Button(master=self.payments_treeview, text="Delete", style="Accent.TButton")
    
    def __init_separators(self) -> None:
        self.room_tenant_separator = Separator(master=self.room_tenant_frame)
        self.lease_payment_separator = Separator(master=self.lease_payment_frame)
    
    def __set_layout(self) -> None:
        self.room_tenant_frame.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(0, 14), pady=0
        )
        self.lease_payment_frame.grid(
            row=0, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(14, 0), pady=0
        )
        
        self.room_tenant_frame.columnconfigure(1, weight=0, minsize=5)
        self.lease_payment_frame.columnconfigure(1, weight=0, minsize=5)
        
        self.room_number_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=(7, 7), pady=(7, 0)
        )
        self.tenant_count_label.grid(
            row=1, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=(7, 7), pady=(0, 0)
        )
        self.max_capacity_label.grid(
            row=2, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.filler_label.grid(
            row=3, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=(0, 7)
        )
        self.edit_room_button.grid(
            row=4, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=(0, 7)
        )
        
        self.room_tenant_separator.grid(
            row=5, column=0, rowspan=1, columnspan=2,
            sticky="ew", padx=(7, 7), pady=(0, 7)
        )
        
        self.tenants_treeview.grid(
            row=6, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 0), pady=(0, 7)
        )
        self.tenants_scrollbar.grid(
            row=6, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(0, 7), pady=(0, 7)
        )
        
        self.add_tenant_button.grid(
            row=7, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.lease_start_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=(7, 0)
        )
        self.lease_end_label.grid(
            row=1, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.lease_deposit_label.grid(
            row=2, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.leaser_label.grid(
            row=3, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=(0, 7)
        )
        self.add_lease_button.grid(
            row=4, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=(0, 7)
        )
        
        self.lease_payment_separator.grid(
            row=5, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.payments_treeview.grid(
            row=6, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 0), pady=(0, 7)
        )
        self.payments_scrollbar.grid(
            row=6, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(0, 7), pady=(0, 7)
        )
        self.add_payment_button.grid(
            row=7, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.tenants_treeview.configure(yscrollcommand=self.tenants_scrollbar.set)
        self.payments_treeview.configure(yscrollcommand=self.payments_scrollbar.set)
        
        customization_buttons(self.tenants_treeview, self.edit_tenant_button, self.delete_tenant_button)
        customization_buttons(self.payments_treeview, self.edit_payment_button, self.delete_payment_button)        

        for col, width in enumerate((245, 107, 240)):
            self.tenants_treeview.column(col, width=width, stretch=False)
            
        for col, width in enumerate((120, 230, 250)):
            self.payments_treeview.column(col, width=width, stretch=False)

        sv_ttk.set_theme("light", self)
        
        style = Style(self)
        
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", padding=(5, 0, 0, 0))

        self.title("Room [Number]")
        self.eval("tk::PlaceWindow . center")
        self.resizable(False, False)
   
def main() -> None:
   RoomListWindow().mainloop()
   RoomOpenWindow().mainloop()

if __name__ == "__main__":
   main()