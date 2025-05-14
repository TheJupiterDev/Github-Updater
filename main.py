from PySide6.QtWidgets import QApplication
from ui.updater_ui import UpdaterWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdaterWindow()
    window.show()
    sys.exit(app.exec())
