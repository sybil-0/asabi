
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                               QTableView, QHeaderView)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtCore import Qt, QSortFilterProxyModel
import sys

class FileTableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Line edit for user input
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter search or filter term...")
        self.line_edit.textChanged.connect(self.filter_table)
        layout.addWidget(self.line_edit)
        
        # Table view
        self.table_view = QTableView(self)
        layout.addWidget(self.table_view)
        
        self.setLayout(layout)
        self.setWindowTitle("File Table Viewer")
        self.resize(600, 400)
        
        self.setup_database()
        self.setup_model()

    def setup_database(self):
        """Sets up the database connection."""
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("file_data.db")
        if not self.db.open():
            print("Error: Unable to open database")

    def setup_model(self):
        """Initializes the table model and filter model."""
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("files")
        self.model.select()
        
        # Hide the ID column
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.table_view.setModel(self.model)
        self.table_view.hideColumn(0)  # Hide the ID column
        
        # Filtering and sorting model
        self.filter_model = QSortFilterProxyModel(self)
        self.filter_model.setSourceModel(self.model)
        self.filter_model.setFilterKeyColumn(1)  # Filtering by filename column
        self.filter_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        
        self.table_view.setModel(self.filter_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.filter_model.sort(1, Qt.AscendingOrder)  # Sort by filename column

    def filter_table(self):
        """Applies filter based on the text in the line edit."""
        filter_text = self.line_edit.text()
        self.filter_model.setFilterFixedString(filter_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileTableApp()
    window.show()
    sys.exit(app.exec())
