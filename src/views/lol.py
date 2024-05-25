import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt

class RoomDetailsDialog(QDialog):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.setWindowTitle(f'Room {room_data["room_number"]} Details')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Room Details
        room_details_label = QLabel(f'Room Number: {self.room_data["room_number"]}\n'
                                    f'Tenant Count: {self.room_data["tenant_count"]}\n'
                                    f'Max Capacity: {self.room_data["capacity"]}')
        layout.addWidget(room_details_label)

        # List of Tenants
        tenants_label = QLabel('Tenants:')
        self.tenants_table = QTableWidget()
        self.tenants_table.setColumnCount(3)
        self.tenants_table.setHorizontalHeaderLabels(['Tenant Name', 'Contact', 'Actions'])
        self.populate_tenants_table()
        layout.addWidget(tenants_label)
        layout.addWidget(self.tenants_table)

        # Add Tenant button
        add_tenant_button = QPushButton('Add Tenant')
        layout.addWidget(add_tenant_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Lease Information
        lease_info_label = QLabel('Lease Information:')
        self.lease_info_label = QLabel('Lease Start: [Start Date]\n'
                                       'Lease End: [End Date]\n'
                                       'Leaser: [Leaser Name]\n')
        layout.addWidget(lease_info_label)
        layout.addWidget(self.lease_info_label)

        # Payment History
        payment_history_label = QLabel('Payment History:')
        self.payment_history_table = QTableWidget()
        self.payment_history_table.setColumnCount(3)
        self.payment_history_table.setHorizontalHeaderLabels(['Date', 'Amount', 'Status'])
        self.populate_payment_history_table()
        layout.addWidget(payment_history_label)
        layout.addWidget(self.payment_history_table)

        # Buttons for actions
        add_payment_button = QPushButton('Add Payment')
        edit_payment_button = QPushButton('Edit Payment')
        layout.addWidget(add_payment_button)
        layout.addWidget(edit_payment_button)

        self.setLayout(layout)

    def populate_tenants_table(self):
        # Populate the tenants table with data
        tenants = self.room_data.get('tenants', [])
        self.tenants_table.setRowCount(len(tenants))
        for row, tenant in enumerate(tenants):
            name_item = QTableWidgetItem(tenant['name'])
            contact_item = QTableWidgetItem(tenant['contact'])
            edit_button = QPushButton('Edit')
            delete_button = QPushButton('Delete')
            self.tenants_table.setItem(row, 0, name_item)
            self.tenants_table.setItem(row, 1, contact_item)
            self.tenants_table.setCellWidget(row, 2, QWidget())
            action_layout = QHBoxLayout(self.tenants_table.cellWidget(row, 2))
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

    def populate_payment_history_table(self):
        # Populate the payment history table with data
        payments = self.room_data.get('payments', [])
        self.payment_history_table.setRowCount(len(payments))
        for row, payment in enumerate(payments):
            self.payment_history_table.setItem(row, 0, QTableWidgetItem(payment['date']))
            self.payment_history_table.setItem(row, 1, QTableWidgetItem(str(payment['amount'])))
            self.payment_history_table.setItem(row, 2, QTableWidgetItem(payment['status']))

app = QApplication(sys.argv)

# Usage example:
room_data = {
    "room_number": "101",
    "tenant_count": 2,
    "capacity": 4,
    "tenants": [
        {"name": "John Doe", "contact": "123-456-7890"},
        {"name": "Jane Smith", "contact": "987-654-3210"}
    ],
    "lease_info": {"start_date": "2024-01-01", "end_date": "2025-01-01", "leaser": "XYZ Realty"},
    "payments": [
        {"date": "2024-02-01", "amount": 500, "status": "Paid"},
        {"date": "2024-03-01", "amount": 500, "status": "Paid"}
    ]
}

dialog = RoomDetailsDialog(room_data)
dialog.exec()

# Start the event loop
sys.exit(app.exec())
