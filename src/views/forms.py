from __future__ import annotations
from tkinter import Tk, Toplevel, Event
from tkinter.ttk import Treeview, Style, Combobox, Button, Label, Entry, Scrollbar
from tkcalendar import DateEntry

class RoomForm(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
        
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
        
class TenantForm(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_labels()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
    
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

class LeaseForm(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.__init_labels()
        self.__init_entries()
        self.__init_comboboxes()
        self.__init_buttons()
        
        self.__set_layout()
    
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
    def __init__(self, parent: Tk, payment_data: dict = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.payment_data = payment_data
        
        self.__init_labels()
        self.__init_datepickers()
        self.__init_entries()
        self.__init_buttons()
        
        self.__set_layout()
        
    def __init_labels(self) -> None:
        self.payment_date_label = Label(self, text="Lease Start Date:")
        self.payment_amount_label = Label(self, text="Deposit Amount:")
    
    def __init_entries(self) -> None:
        self.payment_date_entry = DateEntry(self, width=12, date_pattern="yyyy-mm-dd")
        self.payment_amount_entry = Entry(self)
        
        if self.payment_data:
            self.payment_date_entry.set_date(self.payment_date.get('payment_date', ''))
            self.payment_amount_entry.insert(0, str(self.lease_data.get('payment_amount', '')))

    
    def __init_datepickers(self) -> None:
        pass
    
    def __init_buttons(self) -> None:
        self.save_button = Button(self, text="Save", command=self.save_payment)
        self.cancel_button = Button(self, text="Cancel", command=self.destroy)
    
    def __set_layout(self) -> None:
        self.payment_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.payment_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.payment_amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.payment_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.cancel_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
    def save_payment(self) -> None:
        payment_date = self.payment_date_entry.get_date()
        payment_amount = float(self.payment_amount_entry.get())
        
        print("Payment Date:", payment_date)
        print("Payment Amount:", payment_amount)
        self.destroy()


def main() -> None:
   LeaseForm().mainloop()

if __name__ == "__main__":
   main()
