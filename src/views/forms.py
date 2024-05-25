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
        self.__init_datepickers()
        self.__init_buttons()
        
        self.__set_layout()
    
    def __init_labels(self) -> None:
        self.lastname_label = Label(master=self, text="*Last Name")
        self.firstname_label = Label(master=self, text="*First Name")
        self.middlename_label = Label(master=self, text="Middle Name")
        self.contactnumber_label = Label(master=self, text="Contact Number (09XXXXXXXXX)")
        self.birthdate_label = Label(master=self, text="Birth Date")
    
    def __init_entries(self) -> None:
        self.lastname_entry = Entry(master=self)
        self.firstname_entry = Entry(master=self)
        self.middlename_entry = Entry(master=self)
        self.contactnumber_entry = Entry(master=self)
    
    def __init_datepickers(self) -> None:
        self.datepick_dateentry = DateEntry(master=self)
    
    def __init_buttons(self) -> None:
        self.add_tenant_button = Button(master=self, text="Add Tenant")
    
    def __set_layout(self) -> None:
        pass

class LeaseForm(Toplevel):
    def __init__(self, parent: Tk, lease_data: dict = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.lease_data = lease_data
        
        self.__init_labels()
        self.__init_entries()
        self.__init_datepickers()
        self.__init_buttons()
        
        self.__set_layout()
        
    def __init_labels(self) -> None:
        self.start_date_label = Label(self, text="Lease Start Date:")
        self.end_date_label = Label(self, text="Lease End Date:")
        self.deposit_label = Label(self, text="Deposit Amount:")
        self.rent_label = Label(self, text="Monthly Rent Amount:")
    
    def __init_entries(self) -> None:
        self.start_date_entry = DateEntry(self, width=12, date_pattern="yyyy-mm-dd")
        self.end_date_entry = DateEntry(self, width=12, date_pattern="yyyy-mm-dd")
        self.deposit_entry = Entry(self)
        self.rent_entry = Entry(self)
        
        if self.lease_data:
            self.start_date_entry.set_date(self.lease_data.get('lease_start', ''))
            self.end_date_entry.set_date(self.lease_data.get('lease_end', ''))
            self.deposit_entry.insert(0, str(self.lease_data.get('deposit_amount', '')))
            self.rent_entry.insert(0, str(self.lease_data.get('monthly_rentAmount', '')))
    
    def __init_datepickers(self) -> None:
        pass
    
    def __init_buttons(self) -> None:
        self.save_button = Button(self, text="Save", command=self.save_lease)
        self.cancel_button = Button(self, text="Cancel", command=self.destroy)
    
    def __set_layout(self) -> None:
        self.start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.end_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.deposit_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.deposit_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.rent_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.rent_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.cancel_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
    def save_lease(self) -> None:
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        deposit_amount = float(self.deposit_entry.get())
        monthly_rentAmount = float(self.rent_entry.get())
        
        print("Lease Start Date:", start_date)
        print("Lease End Date:", end_date)
        print("Deposit Amount:", deposit_amount)
        print("Monthly Rent Amount:", monthly_rentAmount)
        
        self.destroy()

def main() -> None:
   RoomForm().mainloop()

if __name__ == "__main__":
   main()
