import time
from PyQt5.QtCore import QThread, pyqtSignal

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal()
    saving_started = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.posts = []

    def run(self):
        time.sleep(3) 
        self.posts = self.db_manager.fetch_posts()

        if self.posts:
            self.saving_started.emit()
            time.sleep(3)
            self.db_manager.save_posts(self.posts)
            self.data_loaded.emit()
        else:
            self.data_loaded.emit()
