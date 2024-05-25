import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QScrollArea

from PyQt6.QtCore import Qt

class RoomWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def __init_layouts(self) -> None:
        self.main_layout = QGridLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        
    
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(480, 540)
        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Create a QVBoxLayout to hold the search box and button
        search_layout = QVBoxLayout()

        # Create the search box and button
        search_box = QLineEdit(self)
        search_box.setPlaceholderText('Search...')
        button = QPushButton('Button', self)

        # Add the search box and button to the search layout
        search_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)
        search_layout.addWidget(search_box, alignment=Qt.AlignmentFlag.AlignRight)

        # Add the search layout to the main layout
        main_layout.addLayout(search_layout)

        # Create a QScrollArea to hold the square panes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a QWidget to hold the panes
        panes_widget = QWidget()

        # Create a QGridLayout to hold the square panes
        self.grid_layout = QGridLayout(panes_widget)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align panes to the top

        # Add some example square panes (buttons) to the QGridLayout
        self.panes = []
        for i in range(20):
            pane = QPushButton(f'Pane {i + 1}', self)
            pane.setFixedSize(100, 100)  # Set fixed size to make them square
            pane.clicked.connect(lambda _, x=i: self.on_pane_clicked(x))  # Connect click event
            self.panes.append(pane)
            self.grid_layout.addWidget(pane, i // 4, i % 4)  # Adjust the column count dynamically

        # Set the panes_widget as the widget for the scroll_area
        scroll_area.setWidget(panes_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setWindowTitle('Search Box and Scrollable Grid of Panes Example')
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grid_layout()
        print(f'Current window size: {self.size()}')

    def update_grid_layout(self):
        # Calculate the number of columns based on the available width and the pane size
        available_width = self.width() - 20  # Subtract some margin
        pane_size = 100
        columns = max(1, available_width // pane_size)

        # Clear the existing layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # Re-add the panes to the grid layout with the new column count
        for index, pane in enumerate(self.panes):
            row = index // columns
            col = index % columns
            self.grid_layout.addWidget(pane, row, col)

    def on_pane_clicked(self, index):
        print(f'Pane {index + 1} clicked')
        

def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
