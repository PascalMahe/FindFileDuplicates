from collections import defaultdict
import os

# def analyze_duplicates(folder_path):
#     file_records = defaultdict(list)  # (folder_name, file_name) -> [(size, last_modified, full_path)]
#     duplicate_files = defaultdict(list)  # (folder_name, file_name, size) -> [full_paths]
#     folder_signatures = {}  # (parent_folder, folder_name) -> (tuple_of_files, tuple_of_subfolders)
#     duplicate_folders = {}  # (parent_folder, folder_name) -> full_path

#     # Step 1: Traverse the directory and record files
#     for root, dirs, files in os.walk(folder_path):
#         parent_folder = os.path.basename(os.path.dirname(root))
#         current_folder = os.path.basename(root)

#         # Track files in the folder
#         file_set = set()
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_size = os.path.getsize(file_path)
#             file_set.add((file, file_size))
#             key = (current_folder, file)
#             file_records[key].append((file_size, file_path))

#         # Store folder signature: sorted file names and subfolder names
#         folder_signatures[(parent_folder, current_folder)] = (tuple(sorted(file_set)), tuple(sorted(dirs)))

#     # Step 2: Identify duplicate files
#     for key, entries in file_records.items():
#         file_groups = defaultdict(list)  # Group by size
#         for size, path in entries:
#             file_groups[size].append(path)

#         for size, paths in file_groups.items():
#             if len(paths) > 1:
#                 duplicate_files[(key[0], key[1], size)] = paths

#     # Step 3: Identify duplicate folders using folder signatures
#     seen_signatures = {}
#     for folder_key, signature in folder_signatures.items():
#         if signature in seen_signatures:
#             duplicate_folders[folder_key] = folder_signatures[folder_key]
#         else:
#             seen_signatures[signature] = folder_key

    
#     print(f"duplicate_files: {duplicate_files}")
#     print(f"duplicate_folders: {duplicate_folders}")
#     return duplicate_files, duplicate_folders

def analyze_duplicates(folder_path):
    """
    Analyze the folder and return a dictionary with keys:
      (result_type, name, size)
    and values: list of duplicate locations.
    result_type can be "File" or "Folder".
    
    For simplicity, this example only handles duplicate files.
    You can extend it to also analyze folders.
    """
    file_records = defaultdict(list)
    duplicate_results = defaultdict(list)

    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        for file in files:
            file_path = os.path.join(root, file)
            key = (folder_name, file)
            file_records[key].append(file_path)

    # Identify duplicates and mark them as "File" results.
    for (folder, file_name), paths in file_records.items():
        if len(paths) > 1:
            # Here, key is a tuple: ("File", name, size)
            try:
                size = os.path.getsize(paths[0]) // 1024  # get size from first instance
            except Exception:
                size = 0
            duplicate_results[("File", file_name, size)] = paths

    return duplicate_results