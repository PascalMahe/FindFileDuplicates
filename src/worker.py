from collections import defaultdict
import os
import time

from PyQt6.QtCore import QObject, pyqtSignal

class AnalysisWorker(QObject):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self._should_stop = False

    def stop(self):
        self._should_stop = True

    def run(self):
        duplicate_results = defaultdict(list)
        file_records = defaultdict(list)
        folder_signatures = defaultdict(list)


        time.sleep(5.5)

        for root, dirs, files in os.walk(self.folder_path, topdown=False):
            if self._should_stop:
                return  # Exit early

            folder_name = os.path.basename(root)

            for file in files:
                if self._should_stop:
                    return
                file_path = os.path.join(root, file)
                key = (folder_name, file)
                file_records[key].append(file_path)

            file_list = sorted(files)
            subfolder_list = sorted(dirs)
            signature = (tuple(file_list), tuple(subfolder_list))
            folder_signatures[signature].append(root)

        for (folder, file_name), paths in file_records.items():
            if self._should_stop:
                return
            if len(paths) > 1:
                try:
                    size = os.path.getsize(paths[0]) // 1024
                except Exception:
                    size = 0
                duplicate_results[("File", file_name, size)] = paths

        for signature, paths in folder_signatures.items():
            if self._should_stop:
                return
            if len(paths) > 1:
                folder_name = os.path.basename(paths[0])
                try:
                    total_size = sum(
                        os.path.getsize(os.path.join(dp, f))
                        for path in paths
                        for dp, _, filenames in os.walk(path)
                        for f in filenames
                    ) // 1024
                except Exception:
                    total_size = 0
                duplicate_results[("Folder", folder_name, total_size)] = paths

        self.finished.emit(dict(duplicate_results))
