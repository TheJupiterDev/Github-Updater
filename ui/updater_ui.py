from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from updater import get_latest_release_info, download_asset, extract_zip, get_local_version, update_local_version
import json
import os

class UpdaterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Updater")
        self.setFixedSize(300, 200)

        with open("config.json") as f:
            self.config = json.load(f)

        self.label = QLabel("Press update to check for updates.")
        self.button = QPushButton("Check for Updates")
        self.button.clicked.connect(self.check_for_updates)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_for_updates(self):
        repo = self.config["repo"]
        asset_name = self.config["asset_name"]
        version_file = self.config["local_version_file"]

        try:
            release = get_latest_release_info(repo)
            latest_version = release["tag_name"]
            local_version = get_local_version(version_file)

            if latest_version != local_version:
                for asset in release["assets"]:
                    name = asset["name"].lower()
                    if name.endswith(".zip") and "source code" not in name:
                        download_asset(asset["browser_download_url"], "downloaded.zip")
                        extract_zip("downloaded.zip", ".")
                        update_local_version(version_file, latest_version)
                        os.remove("downloaded.zip")
                        QMessageBox.information(self, "Update", f"Updated to version {latest_version}!")
                        return

                QMessageBox.warning(self, "Asset Not Found", "No suitable .zip asset found in release.")
            else:
                QMessageBox.information(self, "Up to Date", "You're already on the latest version.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
