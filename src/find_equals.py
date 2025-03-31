import os
import time

def find_duplicates(base_path):
    file_dict = {}
    duplicates = {}

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            folder_name = os.path.basename(root)
            file_size = os.path.getsize(file_path)

            key = (file, folder_name, file_size)

            if key in file_dict:
                if key not in duplicates:
                    duplicates[key] = [file_dict[key]]
                duplicates[key].append(file_path)
            else:
                file_dict[key] = file_path

    for key, paths in duplicates.items():
        file_name, folder_name, file_size = key
        print(f"{folder_name}/{file_name} is present in: {', '.join(paths)}")

start_time = time.perf_counter()
# find_duplicates('folder_A')
# find_duplicates('C:\\Users\\pasca')
find_duplicates('E:\\')

end_time = time.perf_counter()
total_time = end_time - start_time
print(f"The function took {total_time:.6f} seconds to execute.")