import os


def create_structure(base, tree):
    for key, value in tree.items():
        path = os.path.join(base, key)
        os.makedirs(path, exist_ok=True)
        if isinstance(value, dict):
            create_structure(path, value)
        elif isinstance(value, list):
            for file in value:
                open(os.path.join(path, file), 'w').close()

def create_file_tree():

    # Define the folder and file structure
    structure0 = {
        'folder_A': {
            'folder_B': {
                'folder_C': {
                    'folder_G': ['file_3.txt']
                }
            },
            'folder_C': ['file_1.txt', 'file_2.txt'],
            'folder_E': {
                'folder_F': {
                    'folder_G': ['file_3.txt']
                }
            }
        }
    }

    create_structure('.', structure0)

    structure1 = {
        'folder_A': {
            'folder_B': {
                'folder_C': 
                    ['file_1.txt', 'file_2.txt']
            }
        }
    }


    create_structure('.', structure1)

# Run the function to create the file tree
create_file_tree()

print("File tree created successfully!")