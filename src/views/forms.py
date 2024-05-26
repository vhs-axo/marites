from __future__ import annotations

from tkinter import BooleanVar, Toplevel
from tkinter.ttk import Style, Combobox, Button, Label, Entry, Checkbutton
from tkcalendar import DateEntry

class RoomForm(Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
        
        self.grab_set()
        
    def __init_labels(self) -> None:
        self.max_capacity_label = Label(master=self, text="*Max Capacity")
    
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
        
class TenantForm(Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
        
        self.grab_set()
    
    def __init_labels(self) -> None:
        self.lastname_label = Label(master=self, text="*Last Name")
        self.firstname_label = Label(master=self, text="*First Name")
        self.middlename_label = Label(master=self, text="Middle Name")
        self.contactnumber_label = Label(master=self, text="*Contact Number (09XXXXXXXXX)")
        self.birthdate_label = Label(master=self, text="*Birth Date")
    
    def __init_entries(self) -> None:
        self.lastname_entry = Entry(master=self)
        self.firstname_entry = Entry(master=self)
        self.middlename_entry = Entry(master=self)
        self.contactnumber_entry = Entry(master=self)
        
        self.birthdate_dateentry = DateEntry(master=self, date_pattern="yyyy-mm-dd")
    
    def __init_buttons(self) -> None:
        self.add_tenant_button = Button(master=self, text="Add Tenant")
    
    def __set_layout(self) -> None:
        self.lastname_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        self.firstname_label.grid(
            row=0, column=2, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        self.middlename_label.grid(
            row=0, column=4, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        
        self.lastname_entry.grid(
            row=1, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        self.firstname_entry.grid(
            row=1, column=2, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        self.middlename_entry.grid(
            row=1, column=4, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.contactnumber_label.grid(
            row=2, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        self.birthdate_label.grid(
            row=2, column=2, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        
        self.contactnumber_entry.grid(
            row=3, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        self.birthdate_dateentry.grid(
            row=3, column=2, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.add_tenant_button.grid(
            row=4, column=5, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.title("Add Tenant")
        self.resizable(False, False)

class LeaseForm(Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        
        self.__init_labels()
        self.__init_entries()
        self.__init_comboboxes()
        self.__init_buttons()
        
        self.__set_layout()
        
        self.grab_set()
    
    def __init_labels(self) -> None:
        self.leaser_label = Label(master=self, text="*Leaser")
        self.startdate_label = Label(master=self, text="*Lease Start Date")
        self.enddate_label = Label(master=self, text="*Lease End Date")
        self.deposit_label = Label(master=self, text="*Deposit Amount")
        self.rent_label = Label(master=self, text="*Monthly Rent Amount")
    
    def __init_entries(self) -> None:
        self.deposit_entry = Entry(master=self)
        self.rent_entry = Entry(master=self)
        
        self.startdate_entry = DateEntry(master=self, date_pattern="yyyy-mm-dd")
        self.enddate_entry = DateEntry(master=self, date_pattern="yyyy-mm-dd")
    
    def __init_comboboxes(self) -> None:
        self.leaser_combobox = Combobox(master=self)
    
    def __init_buttons(self) -> None:
        self.add_lease_button = Button(self, text="Add Lease")
    
    def __set_layout(self) -> None:
        self.leaser_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=7, pady=(7, 0)
        )
        
        self.leaser_combobox.grid(
            row=1, column=0, rowspan=1, columnspan=2,
            sticky="nsew", padx=7, pady=(0, 7)
        )        
        
        self.startdate_label.grid(
            row=2, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        self.enddate_label.grid(
            row=2, column=1, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        
        self.startdate_entry.grid(
            row=3, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        self.enddate_entry.grid(
            row=3, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.deposit_label.grid(
            row=4, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        self.rent_label.grid(
            row=4, column=1, rowspan=1, columnspan=1,
            sticky="sw", padx=(7, 7), pady=(7, 0)
        )
        
        self.deposit_entry.grid(
            row=5, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        self.rent_entry.grid(
            row=5, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=(7, 7), pady=(0, 7)
        )
        
        self.add_lease_button.grid(
            row=6, column=1, rowspan=1, columnspan=1,
            sticky="nse", padx=7, pady=(7, 7)
        )
        
        self.title("Add Lease")
        self.resizable(False, False)

class PaymentForm(Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        self.__init_checkbuttons()
        
        self.__set_layout()
        
        self.grab_set()
        
    def __init_labels(self) -> None:
        self.payment_date_label = Label(master=self, text="*Payment Date")
        self.payment_amount_label = Label(master=self, text="*Amount:")
    
    def __init_entries(self) -> None:
        self.payment_amount_entry = Entry(master=self)
        self.payment_date_entry = DateEntry(master=self, date_pattern="yyyy-mm-dd")
    
    def __init_buttons(self) -> None:
        self.add_payment_button = Button(master=self, text="Add Payment")

    def __init_checkbuttons(self) -> None:
        self.paid_var = BooleanVar(master=self)
        self.paid_checkbutton = Checkbutton(master=self, text="Paid", onvalue=True, offvalue=False, variable=self.paid_var)
    
    def __set_layout(self) -> None:
        self.payment_date_label.grid(
            row=0, column=0, rowspan=1, columnspan=1,
            sticky="sw", padx=7, pady=(7, 0)
        )
        self.payment_amount_label.grid(
            row=0, column=1, rowspan=1, columnspan=1,
            sticky="sw", padx=7, pady=(7, 0)
        )
        
        self.payment_date_entry.grid(
            row=1, column=0, rowspan=1, columnspan=1,
            sticky="nsew", padx=7, pady=(0, 7)
        )
        self.payment_amount_entry.grid(
            row=1, column=1, rowspan=1, columnspan=1,
            sticky="nsew", padx=7, pady=(0, 7)
        )
        self.paid_checkbutton.grid(
            row=1, column=2, rowspan=1, columnspan=1,
            sticky="nsw", padx=7, pady=(0, 7)
        )
        
        self.add_payment_button.grid(
            row=2, column=2, rowspan=1, columnspan=1,
            sticky="nse", padx=7, pady=7
        )
        
        self.title("Add Payment")
        self.resizable(False, False)

def main() -> None:
    RoomForm(None).mainloop()
    TenantForm(None).mainloop()
    LeaseForm(None).mainloop()
    PaymentForm(None).mainloop()

if __name__ == "__main__":
   main()
