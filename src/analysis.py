from collections import defaultdict
import os

def analyze_duplicates(folder_path):
    """
    Analyze the folder and return a dictionary with keys:
      (result_type, name, size)
    and values: list of duplicate locations.
    result_type can be "File" or "Folder".
    """
    file_records = defaultdict(list)
    folder_signatures = defaultdict(list)
    duplicate_results = defaultdict(list)

    # First pass: record all files and folder signatures
    for root, dirs, files in os.walk(folder_path, topdown=False):
        folder_name = os.path.basename(root)

        # Record files for duplicate file detection
        for file in files:
            file_path = os.path.join(root, file)
            key = (folder_name, file)
            file_records[key].append(file_path)

        # Build folder signature: a tuple of sorted filenames + subfolder names
        file_list = sorted(files)
        subfolder_list = sorted(dirs)
        signature = (tuple(file_list), tuple(subfolder_list))

        folder_signatures[signature].append(root)

    # Identify duplicate files
    for (folder, file_name), paths in file_records.items():
        if len(paths) > 1:
            try:
                size = os.path.getsize(paths[0]) // 1024  # in KB
            except Exception:
                size = 0
            duplicate_results[("File", file_name, size)] = paths

    # Identify duplicate folders based on identical structure
    for signature, paths in folder_signatures.items():
        if len(paths) > 1:
            folder_name = os.path.basename(paths[0])
            # Estimate folder size by summing file sizes
            try:
                total_size = sum(
                    os.path.getsize(os.path.join(dp, f))
                    for path in paths
                    for dp, _, filenames in os.walk(path)
                    for f in filenames
                ) // 1024  # in KB
            except Exception:
                total_size = 0
            duplicate_results[("Folder", folder_name, total_size)] = paths

    return duplicate_results