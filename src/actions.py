import os
import subprocess

from PyQt6.QtGui import QFontMetrics, QIcon
from PyQt6.QtWidgets import QFileDialog, QTreeWidgetItem, QToolButton, QWidget, QLabel, QHBoxLayout, QPushButton, QMessageBox, QSpacerItem, QSizePolicy



from analysis import analyze_duplicates

def select_file(main_window):
    """Opens a folder dialog and sets the text of the folder_name_input."""
    folder_name = QFileDialog.getExistingDirectory(main_window, "Select Folder")
    if folder_name:
        main_window.folder_name_input.setText(folder_name)

def update_button_style(main_window):
    """Update the button style based on input field content."""
    if main_window.folder_name_input.text().strip():  # If input is not empty
        main_window.launch_button.setProperty("active", True)
    else:  # If input is empty
        main_window.launch_button.setProperty("active", False)

    main_window.launch_button.style().unpolish(main_window.launch_button)
    main_window.launch_button.style().polish(main_window.launch_button)

def launch_analysis(main_window):
    """Performs analysis and updates the UI accordingly."""
    folder_path = main_window.folder_name_input.text()
    if not folder_path or not os.path.isdir(folder_path):
        main_window.status_label.setText("Invalid folder. Please select a valid directory.")
        return {}, {}

    folder_path = folder_path.replace("/", "\\")
    main_window.status_label.setText("Processing...")

    # duplicate_files, duplicate_folders = analyze_duplicates(folder_path)
    duplicate_files = analyze_duplicates(folder_path)
    
    main_window.folder_label.setText(f"Analyzed Folder: {folder_path}")

    # Update results table
    update_results_table(main_window, duplicate_files)
    main_window.status_label.setText("Analysis complete.")  # Update status


def create_result_item(tree, data, locations):
    """
    Creates a top-level QTreeWidgetItem for a duplicate result, with a composite widget in column 3.
    
    data: a tuple like (result_type, file_name, file_size)
    locations: a list of full paths for duplicates
    """

    # Load icons for file and folder
    file_icon = QIcon(os.path.abspath("src/img/file.png"))
    folder_icon = QIcon(os.path.abspath("src/img/folder.png"))

    icon = folder_icon if data[0].lower() == "folder" else file_icon

    # Create the top-level item with text in the first three columns.
    item = QTreeWidgetItem(["", data[1], f"{data[2]} KB", ""])
    item.setIcon(0, icon)  # Set the icon in the first column
    # Add the item to the tree.
    tree.addTopLevelItem(item)
    
    # Compute the common path among all duplicate locations.
    common_prefix = os.path.commonpath(locations) if locations else ""
    
    # Create a composite widget for the last column.
    composite = QWidget()
    # Set the composite widget in the last column (column index 3).
    tree.setItemWidget(item, 3, composite)
    layout = QHBoxLayout(composite)
    layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
    layout.setSpacing(2)  # Optional spacing between the label and button

    # Create a label that displays the common path.
    label = QLabel(common_prefix)
    layout.addWidget(label)

    # Create a chevron button.
    button = QToolButton()
    button.setIcon(QIcon(os.path.abspath("src/img/chevron_right.png")))
    button.setCheckable(True)
    button.setStyleSheet("border: none; padding: 2px;")
    
    button.clicked.connect(lambda checked, item=item, locs=locations: toggle_details(item, checked, locs, common_prefix))
    layout.addWidget(button)
    layout.button = button

    composite.setLayout(layout)
    composite.layout = layout

    # Start with children collapsed so that the chevron is visible.
    item.setExpanded(False)
    
    return item


def update_results_table(main_window, duplicate_files):
    """
    Expects duplicate_files to be a dictionary with keys: (folder_name, file_name, file_size)
    and values: list of duplicate locations.
    """
    tree = main_window.results_tree
    tree.clear()
    
    longest_name = ""
    for (folder_name, file_name, file_size), locations in duplicate_files.items():
        # In this example, we treat the result type as "File"
        create_result_item(tree, ("File", " " + file_name, file_size), locations)
        if len(file_name) > len(longest_name):
            longest_name = file_name
    
    # computing width of longest_string
    font_metrics = QFontMetrics(tree.font())
    needed_width = font_metrics.horizontalAdvance(longest_name)
    
    if tree.columnWidth(1) < needed_width:
        tree.setColumnWidth(1, needed_width)

def toggle_details(item, expanded, locations, common_prefix):
    """Toggle showing/hiding detail rows under the given item and update the chevron icon."""
    
    widget = item.treeWidget().itemWidget(item, 3)
    layout = getattr(widget, "layout", None)
    if not layout:
        print("Error, no layout found!")
    button = getattr(layout, "button", None)
    if not button:
        print("Error, no button found!")
        return  # Safety check in case the button is missing

    if expanded:
        # Change to 'chevron_down.png' when expanded
        button.setIcon(QIcon(os.path.abspath("src/img/chevron_down.png")))
        
        # Add child items for each location
        for i, loc in enumerate(locations):
            shortened_name = loc.replace(common_prefix, "")
            tree_char = "├─"
            if i == len(locations) - 1:
                tree_char = "└─"
            
            child = QTreeWidgetItem(["", "", "", tree_char + " " + shortened_name])
            item.addChild(child)

            # Create a QWidget for the last column
            composite = QWidget()
            child_layout = QHBoxLayout(composite)
            child_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
            child_layout.setSpacing(5)

            spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            child_layout.addItem(spacer)

            # Create Open Folder Button
            open_button = QPushButton()
            open_button.setIcon(QIcon(os.path.abspath("src/img/explorer_open.png")))
            open_button.setStyleSheet("border: none; padding: 2px;")
            open_button.setFixedSize(24, 24)
            open_button.clicked.connect(lambda _, path=loc: open_in_explorer(path))
            child_layout.addWidget(open_button)

            # Create Delete File Button
            delete_button = QPushButton()
            delete_button.setIcon(QIcon(os.path.abspath("src/img/delete.png")))
            delete_button.setStyleSheet("border: none; padding: 2px;")
            delete_button.setFixedSize(24, 24)
            delete_button.clicked.connect(lambda _, path=loc, item=child: delete_file(path, item))
            child_layout.addWidget(delete_button)

            composite.setLayout(child_layout)
            item.treeWidget().setItemWidget(child, 3, composite)
        item.setExpanded(True)
    else:
        # Change to 'chevron_right.png' when collapsed
        button.setIcon(QIcon(os.path.abspath("src/img/chevron_right.png")))
        
        # Remove all child items
        item.takeChildren()

def open_in_explorer(file_path):
    """Opens the file location in the OS file explorer."""
    if os.path.exists(file_path):
        folder_path = os.path.dirname(file_path)
        subprocess.run(["explorer", folder_path], check=False)
    else:
        QMessageBox.warning(None, "File Not Found", "The selected file does not exist.")

def delete_file(file_path, item):
    """Deletes the file after user confirmation."""
    if not os.path.exists(file_path):
        QMessageBox.warning(None, "File Not Found", "The selected file does not exist.")
        return

    reply = QMessageBox.question(
        None, "Confirm Deletion",
        f"Are you sure you want to delete '{file_path}'?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        try:
            os.remove(file_path)
            parent = item.parent()
            if parent:
                parent.removeChild(item)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not delete file:\n{e}")

