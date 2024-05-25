from __future__ import annotations
from tkinter import Tk, Toplevel, Event
from tkinter.ttk import Treeview, Style, Combobox, Button, Label, Entry, Scrollbar, Separator, Frame

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
    
    def __init_treeviews(self) -> None:
        self.tenants_treeview = Treeview(
            master=self,
            columns=("tenant_name", "contact_number", "birth_date"),
            show="headings",
            selectmode="browse"
        )
        
        self.tenants_treeview.heading(column="tenant_name", text="Tenant Name", anchor="w")
        self.tenants_treeview.heading(column="contact_number", text="Contact Number", anchor="w")
        self.tenants_treeview.heading(column="birth_date", text="Birth Date", anchor="w")
        
        self.payments_treeview = Treeview(
            master=self,
            columns=("payment_date", "payment_amount", "status"),
            show="headings",
            selectmode="browse"
        )
        
        self.payments_treeview.heading(column="payment_date", text="Payment Date", anchor="w")
        self.payments_treeview.heading(column="payment_amount", text="Amount", anchor="w")
        self.payments_treeview.heading(column="status", text="Status", anchor="w")
        
        s = Style()
        s.configure("Treeview", rowheight=25)
    
    def __init_scrollbars(self) -> None:
        self.tenants_scrollbar = Scrollbar(
            self, 
            orient="vertical", 
            command=self.tenants_treeview.yview
        )
        
        self.payments_scrollbar = Scrollbar(
            self, 
            orient="vertical", 
            command=self.payments_treeview.yview
        )
    
    def __init_buttons(self) -> None:
        self.edit_room_button = Button(master=self, text="Edit Room")
        self.add_tenant_button = Button(master=self, text="Add Tenant")
        self.add_lease_button = Button(master=self, text="Add Lease")
        self.add_payment_button = Button(master=self, text="Add Payment")
        
        self.edit_tenant_button = Button(master=self.tenants_treeview, text="Edit")
        self.delete_tenant_button = Button(master=self.tenants_treeview, text="Delete")
        
        self.edit_payment_button = Button(master=self.payments_treeview, text="Edit")
        self.delete_payment_button = Button(master=self.payments_treeview, text="Delete")
    
    def __init_separators(self) -> None:
        self.room_tenant_separator = Separator(master=self)
        self.tenant_lease_separator = Separator(master=self)
        self.lease_payment_separator = Separator(master=self)
    
    def __set_layout(self) -> None:
        self.columnconfigure(1, weight=0, minsize=5)
        
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
            sticky="w", padx=(7, 7), pady=(0, 7)
        )
        self.edit_room_button.grid(
            row=3, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=(7, 7), pady=(0, 7)
        )
        
        self.room_tenant_separator.grid(
            row=4, column=0, rowspan=1, columnspan=2,
            sticky="ew", padx=(7, 7), pady=(0, 7)
        )
        
        self.tenants_treeview.grid(
            row=5, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 0), pady=(0, 7)
        )
        self.tenants_scrollbar.grid(
            row=5, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(0, 7), pady=(0, 7)
        )
        self.add_tenant_button.grid(
            row=6, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.tenant_lease_separator.grid(
            row=7, column=0, rowspan=1, columnspan=2,
            sticky="ew", padx=(7, 7), pady=(0, 7)
        )
        
        self.lease_start_label.grid(
            row=8, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.lease_end_label.grid(
            row=9, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.lease_deposit_label.grid(
            row=10, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.leaser_label.grid(
            row=11, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )
        self.lease_start_label.grid(
            row=12, column=0, rowspan=1, columnspan=1,
            sticky="w", padx=7, pady=0
        )

def main() -> None:
   RoomOpenWindow().mainloop()

if __name__ == "__main__":
   main()